import json
import logging
import re
from pathlib import Path
import template


logger = logging.getLogger(Path(__file__).stem)


def gen_tests(fns, default_table):
    def _parse_tests(fn):
        def parse_kind(s):
            match s.lower().split():
                case ['cyr', '<>', 'lat']: return 'c2lr'
                case ['lat', '<>', 'cyr']: return 'l2cr'
                case ['cyr', '>', 'lat']: return 'c2l'
                case ['lat', '>', 'cyr']: return 'l2c'
                case _:
                    raise Exception(f'unknown test kind: {s!r}')
        with fn.open() as fp:
            data = json.load(fp)
        return [[parse_kind(obj['test']), obj['cyr'], obj['lat']] for obj in data]

    def table_name(s):
        return re.sub(r'test_', '', s)
    def _j(s):
        return json.dumps(s, ensure_ascii=False)

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'assert Paiv.UkrainianLatin.encode(cyr, :{table}) == lat\n'
        else:
            yield f'assert Paiv.UkrainianLatin.decode(lat, :{table}) == cyr\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'assert Paiv.UkrainianLatin.decode(lat, :{table}) == cyr\n'
            else:
                yield f'assert Paiv.UkrainianLatin.encode(cyr, :{table}) == lat\n'

    def _emit_tests_default(kind):
        if kind[0] == 'c':
            yield f'assert Paiv.UkrainianLatin.encode(cyr) == lat\n'
        else:
            yield f'assert Paiv.UkrainianLatin.decode(lat) == cyr\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'assert Paiv.UkrainianLatin.decode(lat) == cyr\n'
            else:
                yield f'assert Paiv.UkrainianLatin.encode(cyr) == lat\n'

    def _emit_testset(data, table):
        tpl = '''
        test "&table #&tid" do
          cyr = &cyr
          lat = &lat
          &tests
          &dtests
        end
        '''
        for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
            xs = [(i,cyr,lat) for i,(k,cyr,lat) in enumerate(data, 1) if k == kind]
            if not xs: continue
            ctx = dict(table=table, kind=kind)
            for tid, cyr, lat in xs:
                ctx['tid'] = tid
                ctx['cyr'] = _j(cyr)
                ctx['lat'] = _j(lat)
                ctx['tests'] = _emit_tests(kind, table)
                ctx['dtests'] = iter('')
                if table == default_table:
                    ctx['dtests'] = _emit_tests_default(kind)
                yield template.format(tpl, ctx)

    def _test_cases():
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            data = _parse_tests(fn)
            yield from _emit_testset(data, table)

    context = dict()
    context['test_cases'] = _test_cases

    tpl = '''\
    defmodule Paiv.UkrainianLatinTest do
      use ExUnit.Case
      doctest Paiv.UkrainianLatin
      &{test_cases}
    end
    '''
    text = template.format(tpl, context)
    return text


def gen_transforms(fns, default_table=None):
    def table_name(s):
        s, = re.findall(r'uk_Latn_(.*?)(?:-uk)?\s*$', s, flags=re.I)
        return s.replace('-', '_')
    def _isdec(s):
        return s.startswith('uk_Latn_')
    def _srx(s):
        s = re.sub(r'\\u([0-9A-Fa-f]{4})', r'\\x{\1}', s)
        return f"~r/{s}/u"
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s),
            [r['map'] for r in s]
        ] for s in data]

    def _emit_trrules(rules):
        def _maps(maps):
            for mid, d in enumerate(maps, 1):
                if len(d) < 6:
                    kvs = ', '.join((_j(k) + ' => ' + _j(v)) for k,v in d.items())
                    yield f'maps{sid}{mid} = %{{{kvs}}}\n'
                else:
                    kvs = ',\n'.join(('  ' + _j(k) + ' => ' + _j(v)) for k,v in d.items())
                    yield f'maps{sid}{mid} = %{{\n{kvs}\n}}\n'
        def _tr(maps):
            tpl = '''
            tr&sid = fn &args ->
              &body
            end
            '''
            body1 = '''\
            maps&{sid}1[g1] || g1
            '''
            body = '''\
            cond do
              &capts
              true -> s
            end
            '''
            gn = len(maps)
            def _body1():
                return template.format(body1, sid=sid)
            def _body():
                def _gs():
                    for mid in range(1, gn+1):
                        yield f'g{mid} != "" -> maps{sid}{mid}[g{mid}] || g{mid}\n'
                return template.format(body, capts=_gs)

            ps = 's_'[gn == 1] + ''.join(f', g{i+1}' for i in range(gn))
            if gn == 1:
                yield template.format(tpl, sid=sid, args=ps, body=_body1)
            else:
                yield template.format(tpl, sid=sid, args=ps, body=_body)

        tpl = '''\
        rx&sid = &rx
        &mappings
        &tr
        '''
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                yield template.format(tpl, sid=sid, rx=_srx(rx), mappings=_maps(maps), tr=_tr(maps))

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'|> String.normalize(:{section.lower()})\n'
            else:
                yield f'|> then(&Regex.replace(rx{sid}, &1, tr{sid}))\n'

    def _emit_tr(cname, verb, rules):
        ctx = dict(cname=cname, verb=verb)
        ctx['trrules'] = _emit_trrules(rules)
        ctx['trbody'] = _emit_trbody(rules)
        tpl = '''
        defp &{verb}_&cname(text) do
          &trrules

          text
          &trbody
        end
        '''
        return template.format(tpl, ctx)

    tables = dict()
    for fn in fns:
        logger.info(f'processing {fn!s}')
        with fn.open() as fp:
            rules = json.load(fp)
            rules = _load_rules(rules)
        name = fn.stem
        table = table_name(name)
        cname = table.lower()
        if table not in tables:
            tables[table] = [None, None]
        tables[table][_isdec(name)] = (cname, rules)

    def _emit_tables():
        for ar, verb in zip([0,1], ['encode', 'decode']):
            for table, codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    yield _emit_tr(cname, verb, rules)

    def _emit_encoders():
        tpl = r'''
        def encode(text, :&{table}) when is_binary(text) do
          encode_&{ltable}(text)
        end
        '''
        for table, codec in tables.items():
            enc,dec = codec
            if enc:
                yield template.format(tpl, table=table, ltable=table.lower())

    def _emit_decoders():
        tpl = r'''
        def decode(text, :&{table}) when is_binary(text) do
          decode_&{ltable}(text)
        end
        '''
        for table, codec in tables.items():
            enc,dec = codec
            if dec:
                yield template.format(tpl, table=table, ltable=table.lower())

    context = dict()
    context['global_tables'] = _emit_tables
    context['default_table'] = default_table
    context['def_encoders'] = _emit_encoders
    context['def_decoders'] = _emit_decoders

    tpl = r'''defmodule Paiv.UkrainianLatin do
  @moduledoc """
  Ukrainian Cyrillic transliteration to and from Latin script.

  Tables:
  - `:DSTU_9112_A` DSTU 9112:2021 System A
  - `:DSTU_9112_B` DSTU 9112:2021 System B
  - `:KMU_55` KMU 55:2010, not reversible

  ## Examples
      iex> Paiv.UkrainianLatin.encode("Доброго вечора!")
      "Dobroğo večora!"
      iex> Paiv.UkrainianLatin.decode("Paljanycja")
      "Паляниця"

  Set the transliteration scheme:
      iex> Paiv.UkrainianLatin.encode("Борщ", :DSTU_9112_B)
      "Borshch"
      iex> Paiv.UkrainianLatin.encode("Шевченко", :KMU_55)
      "Shevchenko"
  """

  @doc """
  Transliterates a string of Ukrainian Cyrillic to Latin script.
  """
  def encode(text, table \\ :&{default_table})
  &{def_encoders}

  @doc """
  Re-transliterates a string of Ukrainian Latin to Cyrillic script.
  """
  def decode(text, table \\ :&{default_table})
  &{def_decoders}
  &{global_tables}
end
'''
    text = template.format(tpl, context)
    return text

