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

    def _emit_tests(kind, table, file):
        if kind[0] == 'c':
            print(f'        string q = tr.Encode(cyr, UkrainianLatin.Table.{table});', file=file)
            print(f'        Assert.Equal(lat, q);', file=file)
        else:
            print(f'        string q = tr.Decode(lat, UkrainianLatin.Table.{table});', file=file)
            print(f'        Assert.Equal(cyr, q);', file=file)
        if kind[-1] == 'r':
            if kind[0] == 'c':
                print(f'        string t = tr.Decode(lat, UkrainianLatin.Table.{table});', file=file)
                print(f'        Assert.Equal(cyr, t);', file=file)
            else:
                print(f'        string t = tr.Encode(cyr, UkrainianLatin.Table.{table});', file=file)
                print(f'        Assert.Equal(lat, t);', file=file)

    def _emit_testset(data, table, file):
        for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
            xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
            if not xs: continue
            print('', file=file)
            print('    [Theory]', file=file)
            for cyr,lat in xs:
                print(f'    [InlineData({_j(cyr)}, {_j(lat)})]', file=file)
            print(f'    public void test_{kind}_{table}(string cyr, string lat) {{', file=file)
            _emit_tests(kind, table, file=file)
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

    template = '''namespace paiv.uklatn.tests;

/// <exclude/>
public class UkrainianLatinTest {{
    private UkrainianLatin tr;

    public UkrainianLatinTest() {{
        tr = new UkrainianLatin();
    }}
{test_cases}
}}
'''
    text = template.format(**context)
    return text


def gen_transforms(fns, default_table=None):
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
                so += f'private Regex _rx{sid};\n';
                so += f'private MatchEvaluator _tr{sid};\n';
        print(textwrap.indent(so, ' ' * 4), file=file)

    def _emit_trrules(rules, file):
        so = ''
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                gn = len(maps)
                so += f'this._rx{sid} = new Regex(@"{rx}",\n'
                so += '    RegexOptions.Compiled | RegexOptions.CultureInvariant);\n'
                so += f'var _maps{sid} = new List<Dictionary<string,string>> {{\n'
                sm = ''
                for d in maps:
                    sm += '    new Dictionary<string,string> {\n        '
                    sm += ','.join(f'{{{_j(k)},{_j(v)}}}' for k,v in d.items())
                    sm += '\n    },\n'
                so += sm[:-2] + '\n};\n'
                so += f'this._tr{sid} = (Match match) => {{\n'
                so += '    for (int i = match.Groups.Count; i > 0; i -= 1) {\n'
                so += '        Group group = match.Groups[i];\n'
                so += '        if (!group.Success) { continue; }\n'
                so += '        string key = group.Value;\n'
                so +=f'        if (_maps{sid}[i-1].TryGetValue(key, out string? value)) {{\n'
                so += '            return value;\n'
                so += '        }\n'
                so += '        return key;\n'
                so += '    }\n'
                so += '    return match.Groups[0].Value;\n'
                so += '};\n'
        print(textwrap.indent(so, ' ' * 8), end='', file=file)

    def _emit_trbody(rules, file):
        so = ''
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                so += f'text = text.Normalize(NormalizationForm.Form{section[2:]});\n'
            else:
                so += f'text = this._rx{sid}.Replace(text, this._tr{sid});\n'
        so += 'return text;'
        print(textwrap.indent(so, ' ' * 8), file=file)

    def _emit_tr(cname, rules, file):
        rules = _load_rules(rules)
        print(f'private sealed class {cname} : _UKLatnTransformer {{', file=file)
        _emit_trdefs(rules, file=file)
        print(f'    internal {cname}() {{', file=file)
        _emit_trrules(rules, file=file)
        print('    }\n', file=file)
        print('    public string Transform(string text) {', file=file)
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
        'DSTU_9112_A': '\n/// <summary>DSTU 9112:2021 System A</summary>',
        'DSTU_9112_B': '\n/// <summary>DSTU 9112:2021 System B</summary>',
        'KMU_55': '\n/// <summary>KMU 55:2010, not reversible</summary>',
    }
    tenum = [(t, i+1, tdoc.get(t,'')) for i,t in enumerate(tables)]
    tenum = '\n'.join(f'{s}\n{t} = {i},' for t,i,s in tenum)
    context['table_enum'] = textwrap.indent(tenum, ' ' * 8)

    with io.StringIO() as so:
        print('private static readonly _UKLatnTransformer?[][] _UklatnTables = {', file=so)
        print('    new _UKLatnTransformer?[2] {null, null},', file=so)
        for tid, (table, (enc, dec)) in enumerate(tables.items(), 1):
            enc = f'new {enc}()' if enc else 'null'
            dec = f'new {dec}()' if dec else 'null'
            print(f'    new _UKLatnTransformer?[2] {{{enc}, {dec}}},', file=so)
        print('};', end='', file=so)
        tabledef = textwrap.indent(so.getvalue(), ' ' * 4)

    context['global_tables'] = classdefs_tables + tabledef
    context['default_table'] = default_table

    template = '''namespace paiv.uklatn;

using System.Text;
using System.Text.RegularExpressions;

/// <summary>
/// Ukrainian Cyrillic transliteration to and from Latin script.
/// </summary>
public sealed class UkrainianLatin {{

    /// Transliteration system
    public enum Table {{
{table_enum}
    }}

    /// <summary>
    /// Transliterates a string of Ukrainian Cyrillic to Latin script.
    /// </summary>
    /// <param name="text">The text to transliterate.</param>
    /// <param name="table">The transliteration system.</param>
    /// <returns>The transliterated text.</returns>
    public string Encode(string text, Table table = Table.{default_table}) {{
        _UKLatnTransformer? ntr = null;
        int ti = (int) table;
        if (ti >= 0 && ti < _UklatnTables.Length) {{
            ntr = _UklatnTables[ti][0];
        }}
        if (ntr is _UKLatnTransformer tr) {{
            return tr.Transform(text);
        }}
        throw new ArgumentException(String.Format("invalid table {{0}}", table), "table");
    }}

    /// <summary>
    /// Re-transliterates a string of Ukrainian Latin to Cyrillic script.
    /// </summary>
    /// <param name="text">The text to transliterate.</param>
    /// <param name="table">The transliteration system.</param>
    /// <returns>The transliterated text.</returns>
    public string Decode(string text, Table table = Table.{default_table}) {{
        _UKLatnTransformer? ntr = null;
        int ti = (int) table;
        if (ti >= 0 && ti < _UklatnTables.Length) {{
            ntr = _UklatnTables[ti][1];
        }}
        if (ntr is _UKLatnTransformer tr) {{
            return tr.Transform(text);
        }}
        throw new ArgumentException(String.Format("invalid table {{0}}", table), "table");
    }}

    private interface _UKLatnTransformer {{
        string Transform(string text);
    }}

{global_tables}
}}
'''
    text = template.format(**context)
    return text

