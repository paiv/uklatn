import io
import json
import logging
import re
import textwrap
from pathlib import Path


logger = logging.getLogger(Path(__file__).stem)


def gen_tests(fns):
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

    def _emit_testdata(kind, data, table, file):
        data = [(cyr,lat) for k,cyr,lat in data if k == kind]
        if not data: return
        dump = ''.join(f'\n[\n    {_j(cyr)},\n    {_j(lat)}\n],' for cyr,lat in data)
        so = f'\ndata_{kind} = [{dump}\n]'
        so = textwrap.indent(so, ' ' * 8)
        print(so, file=file)

    def _emit_tests(kind, data, table, file):
        data = [(cyr,lat) for k,cyr,lat in data if k == kind]
        if not data: return
        print(f'        data_{kind}.each do |cyr,lat|', file=file)
        if kind[0] == 'c':
            print(f'            q = @tr.encode(cyr, {table!r})', file=file)
            print(f'            assert_equal(lat, q, cyr)', file=file)
        else:
            print(f'            q = @tr.decode(lat, {table!r})', file=file)
            print(f'            assert_equal(cyr, q, lat);', file=file)
        if kind[-1] == 'r':
            if kind[0] == 'c':
                print(f'            t = @tr.decode(lat, {table!r})', file=file)
                print(f'            assert_equal(cyr, t, lat);', file=file)
            else:
                print(f'            t = @tr.encode(cyr, {table!r})', file=file)
                print(f'            assert_equal(lat, t, cyr)', file=file)
        print('        end', file=file)
        print(f'        puts "{table}: {kind} #{{data_{kind}.length}} tests passed"', file=file)

    def _emit_testset(data, table, file):
        print(f'\n    def test_{table}()', file=file)
        _emit_testdata('c2lr', data, table, file=file)
        _emit_testdata('l2cr', data, table, file=file)
        _emit_testdata('c2l', data, table, file=file)
        _emit_testdata('l2c', data, table, file=file)
        _emit_tests('c2lr', data, table, file=file)
        _emit_tests('l2cr', data, table, file=file)
        _emit_tests('c2l', data, table, file=file)
        _emit_tests('l2c', data, table, file=file)
        print('    end', file=file)

    context = dict()
    with io.StringIO() as so:
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            data = _parse_tests(fn)
            _emit_testset(data, table, file=so)
        context['test_cases'] = so.getvalue()

    context['test_raise'] =  '"failed\\n input: #{input}\\nexpect: #{expect}\\nactual: #{actual}\\n        #{arr}"'

    template = '''require_relative '../../lib/uklatn.rb'

class TestUkrainianLatin # :nodoc:

    def initialize
        @tr = UkrainianLatin.new
    end

    def assert_equal(expect, actual, input)
        if expect != actual
            s = actual.chars
            arr = expect.chars.map {{|c| c == s.shift ? ' ' : '^'}}.join
            raise {test_raise}
        end
    end
{test_cases}
end

test = TestUkrainianLatin.new
spec = TestUkrainianLatin.instance_methods(false).grep(/^test_/)
spec.each do |name|
    test.send(name)
end
'''
    text = template.format(**context)
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

    def _emit_trrules(rules, file):
        so = ''
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                gn = len(maps)
                so += f'@rx{sid} = /{rx}/\n'
                so += f'@maps{sid} = [\n'
                for d in maps:
                    m = ','.join((_j(k) + '=>' + _j(v)) for k,v in d.items())
                    so += f'    {{{m}}},\n'
                so += ']\n'
        print(textwrap.indent(so, ' ' * 8), end='', file=file)

    def _emit_trbody(rules, file):
        so = ''
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                so += f'text = text.unicode_normalize(:{section.lower()})\n'
            else:
                rx, maps = section
                gn = len(maps)
                so += f'text = text.gsub(@rx{sid}) do |m|\n'
                for mid in reversed(range(1, gn+1)):
                    so += f'    next @maps{sid}[{mid-1}].fetch(${mid}, ${mid}) unless ${mid}.nil?\n'
                so += '    m\n'
                so += 'end\n'
        print(textwrap.indent(so, ' ' * 8), end='', file=file)

    def _emit_tr(cname, rules, file):
        rules = _load_rules(rules)
        print(f'class {cname} # :nodoc:', file=file)
        print('    def initialize()', file=file)
        _emit_trrules(rules, file=file)
        print('    end\n', file=file)
        print('    def transform(text)', file=file)
        _emit_trbody(rules, file=file)
        print('    end', file=file)
        print('end\n', file=file)

    context = dict()
    tables = dict()
    with io.StringIO() as so:
        for fn in fns:
            logger.info(f'processing {fn!s}')
            with fn.open() as fp:
                rules = json.load(fp)
            name = fn.stem
            table = table_name(name)
            cname = class_name(name)
            if table not in tables:
                tables[table] = [None, None]
            tables[table][_isdec(name)] = cname
            _emit_tr(cname, rules, so)
        classdefs_tables = textwrap.indent(so.getvalue(), ' ' * 4)

    def _emit_tabledef(tables):
        so = ''
        so += 'TABLES = Hash.new([nil, nil]) # :nodoc:'
        for tid, (table, (enc, dec)) in enumerate(tables.items(), 1):
            dasht = table.replace('_', '-')
            enc = f'{enc}.new()' if enc else 'nil'
            dec = f'{dec}.new()' if dec else 'nil'
            so += f'\nTABLES[{table!r}] = [{enc}, {dec}]'
            so += f'\nTABLES[{dasht!r}] = TABLES[{table!r}]'
        so = textwrap.indent(so, ' ' * 4)
        return so

    tabledef = _emit_tabledef(tables)

    context['global_tables'] = classdefs_tables + tabledef
    context['default_table'] = default_table

    template = '''\
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
# Select a transliteration scheme:
#     tr.encode('Борщ', 'DSTU_9112_A')
#
class UkrainianLatin

    # Transliterates a string of Ukrainian Cyrillic to Latin script.
    def encode(text, table = {default_table!r})
        tr = TABLES[table][0]
        return tr.transform(text) if tr
        raise ArgumentError.new("invalid table #{{table}}")
    end

    # Re-transliterates a string of Ukrainian Latin to Cyrillic script.
    def decode(text, table = {default_table!r})
        tr = TABLES[table][1]
        return tr.transform(text) if tr
        raise ArgumentError.new("invalid table #{{table}}")
    end

{global_tables}
end
'''
    text = template.format(**context)
    return text

