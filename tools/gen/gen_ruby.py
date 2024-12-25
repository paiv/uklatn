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

    def _emit_testdata(kind, data, table):
        spl = '''\
        [
            &cyr,
            &lat
        ],
        '''
        for cyr, lat in data:
            yield template.format(spl, cyr=_j(cyr), lat=_j(lat)+'\n')

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'q = @tr.encode(cyr, {table!r})\n'
            yield 'assert_equal(lat, q, cyr)\n'
        else:
            yield f'q = @tr.decode(lat, {table!r})\n'
            yield 'assert_equal(cyr, q, lat)\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f't = @tr.decode(lat, {table!r})\n'
                yield 'assert_equal(cyr, t, lat)\n'
            else:
                yield f't = @tr.encode(cyr, {table!r})\n'
                yield 'assert_equal(lat, t, cyr)\n'

    def _emit_tests_default(kind):
        if kind[0] == 'c':
            yield 'q = @tr.encode(cyr)\n'
            yield 'assert_equal(lat, q, cyr)\n'
        else:
            yield 'q = @tr.decode(lat)\n'
            yield 'assert_equal(cyr, q, lat)\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield 't = @tr.decode(lat)\n'
                yield 'assert_equal(cyr, t, lat)\n'
            else:
                yield 't = @tr.encode(cyr)\n'
                yield 'assert_equal(lat, t, cyr)\n'

    def _emit_testset(data, table):
        def _data():
            tpl = '''
            data_&kind = [
            &data
            ]
            '''
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                ctx = dict(kind=kind)
                ctx['data'] = _emit_testdata(kind, xs, table)
                yield template.format(tpl, ctx)

        def _tests():
            tpl = '''
            data_&kind.each do |cyr,lat|
                &tests
                &dtests
            end

            puts "&table: &kind #{data_&kind.length} tests passed"
            '''
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                ctx = dict(table=table, kind=kind)
                ctx['tests'] = _emit_tests(kind, table)
                ctx['dtests'] = iter('')
                if table == default_table:
                    ctx['dtests'] = _emit_tests_default(kind)
                yield template.format(tpl, ctx)

        tpl = '''
        def test_&table()
            &data
            &tests
        end
        '''
        yield template.format(tpl, table=table, data=_data, tests=_tests)

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
    require_relative '../../lib/uklatn.rb'

    class TestUkrainianLatin # :nodoc:

        def initialize
            @tr = UkrainianLatin.new
        end

        def assert_equal(expect, actual, input)
            if expect != actual
                s = actual.chars
                arr = expect.chars.map {|c| c == s.shift ? ' ' : '^'}.join
                raise "failed\\n input: #{input}\\nexpect: #{expect}\\nactual: #{actual}\\n        #{arr}"
            end
        end
        &{test_cases}
    end

    test = TestUkrainianLatin.new
    spec = TestUkrainianLatin.instance_methods(false).grep(/^test_/)
    spec.each do |name|
        test.send(name)
    end
    '''
    text = template.format(tpl, context)
    return text


def gen_transforms(fns, default_table=None):
    def table_name(s):
        s, = re.findall(r'uk_Latn_(.*?)(?:-uk)?\s*$', s, flags=re.I)
        return s.replace('-', '_')
    def class_name(s):
        return 'Uklatn_' + s.replace('-', '_')
    def _isdec(s):
        return s.startswith('uk_Latn_')
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s),
            [r['map'] for r in s]
        ] for s in data]

    def _emit_trrules(rules):
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                so = f'@rx{sid} = /{rx}/\n'
                so += f'@maps{sid} = [\n'
                for d in maps:
                    m = ','.join((_j(k) + '=>' + _j(v)) for k,v in d.items())
                    so += f'    {{{m}}},\n'
                so += ']\n'
                yield so

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'text = text.unicode_normalize(:{section.lower()})\n'
            else:
                rx, maps = section
                gn = len(maps)
                so = f'text = text.gsub(@rx{sid}) do |m|\n'
                for mid in reversed(range(1, gn+1)):
                    so += f'    next @maps{sid}[{mid-1}].fetch(${mid}, ${mid}) unless ${mid}.nil?\n'
                so += '    m\n'
                so += 'end\n'
                yield so

    def _emit_tr(cname, rules):
        ctx = dict(cname=cname)
        ctx['trrules'] = _emit_trrules(rules)
        ctx['trbody'] = _emit_trbody(rules)
        tpl = '''
        class &cname # :nodoc:
            def initialize()
                &trrules
            end

            def transform(text)
                &trbody
            end
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
        cname = class_name(name)
        if table not in tables:
            tables[table] = [None, None]
        tables[table][_isdec(name)] = (cname, rules)

    def _emit_tables():
        for ar in [0,1]:
            for table, codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    yield _emit_tr(cname, rules)

        def _entries():
            for table, codec in tables.items():
                dasht = table.replace('_', '-')
                enc,dec = codec
                enc = f'{enc[0]}.new()' if enc else 'nil'
                dec = f'{dec[0]}.new()' if dec else 'nil'
                yield f'TABLES[{table!r}] = [{enc}, {dec}]\n'
                yield f'TABLES[{dasht!r}] = TABLES[{table!r}]\n'
        tpl = '''
        TABLES = Hash.new([nil, nil]) # :nodoc:
        &entries
        '''
        yield template.format(tpl, entries=_entries)

    context = dict()
    context['global_tables'] = _emit_tables
    context['default_table'] = repr(default_table)

    tpl = '''\
# Ukrainian Cyrillic transliteration to and from Latin script.
#
# Tables:
# - 'DSTU_9112_A': DSTU 9112:2021 System A
# - 'DSTU_9112_B': DSTU 9112:2021 System B
# - 'KMU_55': KMU 55:2010, not reversible
#
# Usage:
#     tr = UkrainianLatin.new
#     tr.encode('Доброго вечора!')
#     tr.decode('Paljanycja')
#
# Set the transliteration scheme:
#     tr.encode('Борщ', 'DSTU_9112_B')
#     tr.encode('Шевченко', 'KMU_55')
#
class UkrainianLatin

    # Transliterates a string of Ukrainian Cyrillic to Latin script.
    def encode(text, table = &{default_table})
        tr = TABLES[table][0]
        return tr.transform(text) if tr
        raise ArgumentError.new("invalid table #{table}")
    end

    # Re-transliterates a string of Ukrainian Latin to Cyrillic script.
    def decode(text, table = &{default_table})
        tr = TABLES[table][1]
        return tr.transform(text) if tr
        raise ArgumentError.new("invalid table #{table}")
    end
    &{global_tables}
end
'''
    text = template.format(tpl, context)
    return text

