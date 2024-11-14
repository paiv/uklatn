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
        dump = ''.join(f'\n{{\n    {_j(cyr)},\n    {_j(lat)}\n}},' for cyr,lat in data)
        so = f'\nprivate String[][] data_{table}_{kind} = {{{dump}\n}};'
        so = textwrap.indent(so, ' ' * 4)
        print(so, file=file)

    def _emit_tests(kind, data, table, file):
        data = [(cyr,lat) for k,cyr,lat in data if k == kind]
        if not data: return
        print(f'        for (String[] pair : data_{table}_{kind}) {{', file=file)
        if kind[0] == 'c':
            print(f'            String q = tr.encode(pair[0], UKLatnTable.{table});', file=file)
            print(f'            assertEquals(pair[1], q);', file=file)
        else:
            print(f'            String q = tr.decode(pair[1], UKLatnTable.{table});', file=file)
            print(f'            assertEquals(pair[0], q);', file=file)
        if kind[-1] == 'r':
            if kind[0] == 'c':
                print(f'            String t = tr.decode(pair[1], UKLatnTable.{table});', file=file)
                print(f'            assertEquals(pair[0], t);', file=file)
            else:
                print(f'            String t = tr.encode(pair[0], UKLatnTable.{table});', file=file)
                print(f'            assertEquals(pair[1], t);', file=file)
        print('        }', file=file)

    def _emit_testset(data, table, file):
        _emit_testdata('c2lr', data, table, file=file)
        _emit_testdata('l2cr', data, table, file=file)
        _emit_testdata('c2l', data, table, file=file)
        _emit_testdata('l2c', data, table, file=file)
        print('\n    @Test', file=file)
        print(f'    void test_{table}() {{', file=file)
        _emit_tests('c2lr', data, table, file=file)
        _emit_tests('l2cr', data, table, file=file)
        _emit_tests('c2l', data, table, file=file)
        _emit_tests('l2c', data, table, file=file)
        print('    }', file=file)

    context = dict()
    with io.StringIO() as so:
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            data = _parse_tests(fn)
            _emit_testset(data, table, file=so)
        context['test_cases'] = so.getvalue()

    template = '''package paiv.uklatn;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import paiv.uklatn.UkrainianLatin;
import paiv.uklatn.UkrainianLatin.UKLatnTable;

class UkrainianLatinTest {{
    private UkrainianLatin tr;

    @BeforeEach
    void setUp() {{
        tr = new UkrainianLatin();
    }}
{test_cases}
}}
'''
    text = template.format(**context)
    return text


def gen_transforms(fns, default_table=None):
    def patch_word_boundary(srx):
        return srx.replace(r'\b', r'(?<=^|[^\p{L}\p{M}\p{N}])')
    def table_name(s):
        s, = re.findall(r'uk_Latn_(.*?)(?:-uk)?\s*$', s, flags=re.I)
        return s.replace('-', '_')
    def class_name(s):
        return '_Uklatn_' + s.replace('-', '_')
    def _isdec(s):
        return s.startswith('uk_Latn_')
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s),
            [r['map'] for r in s]
        ] for s in data]

    def _emit_trdefs(rules, file):
        so = ''
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                so += f'private Pattern _rx{sid};\n';
                so += f'private Function<MatchResult,String> _tr{sid};\n';
        print(textwrap.indent(so, ' ' * 4), file=file)

    def _emit_trrules(rules, file):
        so = ''
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                gn = len(maps)
#                rx = patch_word_boundary(rx)
                so += f'this._rx{sid} = Pattern.compile({_j(rx)});\n'
                so += f'List<Map<String,String>> _maps{sid} = List.of(\n'
                sm = ''
                for d in maps:
                    sm += f'    Map.ofEntries(\n        '
                    sm += ','.join(f'entry({_j(k)},{_j(v)})' for k,v in d.items())
                    sm += f'\n    ),\n'
                so += sm[:-2] + '\n);\n'
                so += f'this._tr{sid} = (match) -> {{\n'
                so += '    for (int i = match.groupCount(); i > 0; i -= 1) {\n'
                so += '        String value = match.group(i);\n'
                so += '        if (value != null) {\n'
                so += f'            return _maps{sid}.get(i-1).getOrDefault(value, value);\n'
                so += '        }\n'
                so += '    }\n'
                so += '    return match.group();\n'
                so += '};\n'
        print(textwrap.indent(so, ' ' * 8), end='', file=file)

    def _emit_trbody(rules, file):
        so = ''
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                so += f'text = Normalizer.normalize(text, Normalizer.Form.{section});\n'
            else:
                so += f'text = this._rx{sid}.matcher(text).replaceAll(this._tr{sid});\n'
        so += 'return text;'
        print(textwrap.indent(so, ' ' * 8), file=file)

    def _emit_tr(cname, rules, file):
        rules = _load_rules(rules)
        print(f'private static class {cname} implements _UKLatnTransformer {{', file=file)
        _emit_trdefs(rules, file=file)
        print(f'    {cname}() {{', file=file)
        _emit_trrules(rules, file=file)
        print('    }\n', file=file)
        print('    @Override', file=file)
        print('    public String transform(String text) {', file=file)
        _emit_trbody(rules, file=file)
        print('    }', file=file)
        print('}\n', file=file)

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

    tdoc = {
        'DSTU_9112_A': '\n/** DSTU 9112:2021 System A */',
        'DSTU_9112_B': '\n/** DSTU 9112:2021 System B */',
        'KMU_55': '\n/** KMU 55:2010, not reversible */',
    }
    tenum = [(t, i+1, tdoc.get(t,'')) for i,t in enumerate(tables)]
    tenum = '\n'.join(f'{s}\npublic static final int {t} = {i};' for t,i,s in tenum)
    context['table_enum'] = textwrap.indent(tenum, ' ' * 8)

    with io.StringIO() as so:
        print('private static _UKLatnTransformer[][] _UklatnTables = {', file=so)
        print('    {null, null},', file=so)
        for tid, (table, (enc, dec)) in enumerate(tables.items(), 1):
            enc = f'new {enc}()' if enc else 'null'
            dec = f'new {dec}()' if dec else 'null'
            print(f'    {{{enc}, {dec}}},', file=so)
        print('};', end='', file=so)
        tabledef = textwrap.indent(so.getvalue(), ' ' * 4)

    context['global_tables'] = classdefs_tables + tabledef
    context['default_table'] = default_table

    template = '''package paiv.uklatn;

import static java.util.Map.entry;

import java.text.Normalizer;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.regex.MatchResult;
import java.util.regex.Pattern;

/**
* Ukrainian Cyrillic transliteration to and from Latin script.
*/
public final class UkrainianLatin {{

    /**
    * Transliteration system
    */
    public static final class UKLatnTable {{
{table_enum}
    }}

    /**
    * Transliterates a string of Ukrainian Cyrillic to Latin script,
    * using {{@link UKLatnTable#{default_table}}}.
    *
    * @param text the text to transliterate
    * @return transliterated text
    */
    public String encode(String text) {{
        return encode(text, UKLatnTable.{default_table});
    }}

    /**
    * Transliterates a string of Ukrainian Cyrillic to Latin script.
    *
    * @param text the text to transliterate
    * @param table transliteration system, see {{@link UKLatnTable}}
    * @return transliterated text
    */
    public String encode(String text, int table) {{
        _UKLatnTransformer tr = null;
        if (table >= 0 && table < _UklatnTables.length) {{
            _UKLatnTransformer[] codecs = _UklatnTables[table];
            if (codecs != null) {{ tr = codecs[0]; }}
        }}
        if (tr == null) {{ throw new IllegalArgumentException("invalid table " + String.valueOf(table)); }}
        return tr.transform(text);
    }}

    /**
    * Re-transliterates a string of Ukrainian Latin to Cyrillic script,
    * using {{@link UKLatnTable#{default_table}}}.
    *
    * @param text the text to transliterate
    * @return transliterated text
    */
    public String decode(String text) {{
        return decode(text, UKLatnTable.{default_table});
    }}

    /**
    * Re-transliterates a string of Ukrainian Latin to Cyrillic script.
    *
    * @param text the text to transliterate
    * @param table transliteration system, see {{@link UKLatnTable}}
    * @return transliterated text
    */
    public String decode(String text, int table) {{
        _UKLatnTransformer tr = null;
        if (table >= 0 && table < _UklatnTables.length) {{
            _UKLatnTransformer[] codecs = _UklatnTables[table];
            if (codecs != null) {{ tr = codecs[1]; }}
        }}
        if (tr == null) {{ throw new IllegalArgumentException("invalid table " + String.valueOf(table)); }}
        return tr.transform(text);
    }}

    private static interface _UKLatnTransformer {{
        String transform(String text);
    }}

{global_tables}
}}
'''
    text = template.format(**context)
    return text

