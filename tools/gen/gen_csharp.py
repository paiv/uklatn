import json
import logging
import re
from pathlib import Path
import template


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

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'string q = tr.Encode(cyr, UkrainianLatin.Table.{table});\n'
            yield f'Assert.Equal(lat, q);\n'
        else:
            yield f'string q = tr.Decode(lat, UkrainianLatin.Table.{table});\n'
            yield f'Assert.Equal(cyr, q);\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'string t = tr.Decode(lat, UkrainianLatin.Table.{table});\n'
                yield f'Assert.Equal(cyr, t);\n'
            else:
                yield f'string t = tr.Encode(cyr, UkrainianLatin.Table.{table});\n'
                yield f'Assert.Equal(lat, t);\n'

    def _emit_testset(data, table):
        tpl = '''
        [Theory]
        &data
        public void test_&{kind}_&{table}(string cyr, string lat) {
            &tests
        }
        '''
        ctx = dict(table=table)
        for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
            xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
            if not xs: continue
            ctx['kind'] = kind
            ctx['data'] = (f'[InlineData({_j(cyr)}, {_j(lat)})]\n' for cyr, lat in xs)
            ctx['tests'] = lambda: _emit_tests(kind, table)
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
    namespace paiv.uklatn.tests;

    /// <exclude/>
    public class UkrainianLatinTest {
        private UkrainianLatin tr;

        public UkrainianLatinTest() {
            tr = new UkrainianLatin();
        }
        &{test_cases}
    }
    '''
    text = template.format(tpl, context)
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

    def _emit_trdefs(rules):
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                yield f'private Regex _rx{sid};\n';
                yield f'private MatchEvaluator _tr{sid};\n';

    def _emit_trrules(rules):
        tpl = '''\
        this._rx&sid = new Regex(@"&rx",
            RegexOptions.Compiled | RegexOptions.CultureInvariant);
        var _maps&sid = new List<Dictionary<string,string>> {
            &mappings
        };
        this._tr&sid = (Match match) => {
            for (int i = match.Groups.Count; i > 0; i -= 1) {
                Group group = match.Groups[i];
                if (!group.Success) { continue; }
                string key = group.Value;
                if (_maps&sid[i-1].TryGetValue(key, out string? value)) {
                    return value;
                }
                return key;
            }
            return match.Groups[0].Value;
        };
        '''

        mpl = '''\
        new Dictionary<string,string> {
            &entries
        }'''

        def _ds(data):
            return ','.join(f'{{{_j(k)},{_j(v)}}}' for k,v in data.items()) + '\n'

        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                data = ',\n'.join(template.format(mpl, entries=_ds(d)) for d in maps) + '\n'
                yield template.format(tpl, sid=sid, rx=rx, mappings=data)

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'text = text.Normalize(NormalizationForm.Form{section[2:]});\n'
            else:
                yield f'text = this._rx{sid}.Replace(text, this._tr{sid});\n'

    def _emit_tr(cname, rules):
        context = dict(cname=cname)
        context['trdefs'] = _emit_trdefs(rules)
        context['trrules'] = _emit_trrules(rules)
        context['trbody'] = _emit_trbody(rules)
        tpl = '''
        private sealed class &cname : _UKLatnTransformer {
            &trdefs

            internal &cname() {
                &trrules
            }

            public string Transform(string text) {
                &trbody
                return text;
            }
        }
        '''
        return template.format(tpl, context)

    tables = dict()
    for fn in fns:
        logger.info(f'processing {fn!s}')
        with fn.open() as fp:
            data = json.load(fp)
            rules = _load_rules(data)
        name = fn.stem
        table = table_name(name)
        cname = class_name(name)
        if table not in tables:
            tables[table] = [None, None]
        tables[table][_isdec(name)] = (cname, rules)

    def _emit_tables():
        for ar in [0,1]:
            for table,codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    yield _emit_tr(cname, rules)

        def _entries():
            for table,codec in tables.items():
                enc,dec = codec
                enc = f'new {enc[0]}()' if enc else 'null'
                dec = f'new {dec[0]}()' if dec else 'null'
                yield f'new _UKLatnTransformer?[2] {{{enc}, {dec}}},\n'

        tpl = '''
        private static readonly _UKLatnTransformer?[][] _UklatnTables = {
            new _UKLatnTransformer?[2] {null, null},
            &entries
        };
        '''
        yield template.format(tpl, entries=_entries)

    tdoc = {
        'DSTU_9112_A': 'DSTU 9112:2021 System A',
        'DSTU_9112_B': 'DSTU 9112:2021 System B',
        'KMU_55': 'KMU 55:2010, not reversible',
    }
    def _emit_tenum():
        for i, t in enumerate(tables, 1):
            if (doc := tdoc.get(t, '')):
                doc = f'/// <summary>{doc}</summary>\n'
            yield f'\n{doc}{t} = {i},\n'

    context = dict()
    context['table_enum'] = _emit_tenum
    context['global_tables'] = _emit_tables
    context['default_table'] = default_table

    tpl = '''\
namespace paiv.uklatn;

using System.Text;
using System.Text.RegularExpressions;

/// <summary>
/// Ukrainian Cyrillic transliteration to and from Latin script.
/// </summary>
public sealed class UkrainianLatin {

    /// Transliteration system
    public enum Table {
        &{table_enum}
    }

    /// <summary>
    /// Transliterates a string of Ukrainian Cyrillic to Latin script.
    /// </summary>
    /// <param name="text">The text to transliterate.</param>
    /// <param name="table">The transliteration system.</param>
    /// <returns>The transliterated text.</returns>
    public string Encode(string text, Table table = Table.&{default_table}) {
        _UKLatnTransformer? ntr = null;
        int ti = (int) table;
        if (ti >= 0 && ti < _UklatnTables.Length) {
            ntr = _UklatnTables[ti][0];
        }
        if (ntr is _UKLatnTransformer tr) {
            return tr.Transform(text);
        }
        throw new ArgumentException(String.Format("invalid table {0}", table), "table");
    }

    /// <summary>
    /// Re-transliterates a string of Ukrainian Latin to Cyrillic script.
    /// </summary>
    /// <param name="text">The text to transliterate.</param>
    /// <param name="table">The transliteration system.</param>
    /// <returns>The transliterated text.</returns>
    public string Decode(string text, Table table = Table.&{default_table}) {
        _UKLatnTransformer? ntr = null;
        int ti = (int) table;
        if (ti >= 0 && ti < _UklatnTables.Length) {
            ntr = _UklatnTables[ti][1];
        }
        if (ntr is _UKLatnTransformer tr) {
            return tr.Transform(text);
        }
        throw new ArgumentException(String.Format("invalid table {0}", table), "table");
    }

    private interface _UKLatnTransformer {
        string Transform(string text);
    }
    &{global_tables}
}
'''
    text = template.format(tpl, context)
    return text

