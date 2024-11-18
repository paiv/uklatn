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

    def _emit_testdata(kind, data, table):
        spl = '''\
{
    &cyr,
    &lat
},
'''
        for cyr, lat in data:
            yield template.format(spl, cyr=_j(cyr), lat=_j(lat)+'\n')

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'String q = tr.encode(pair[0], UKLatnTable.{table});\n'
            yield 'assertEquals(pair[1], q);\n'
        else:
            yield f'String q = tr.decode(pair[1], UKLatnTable.{table});\n'
            yield 'assertEquals(pair[0], q);\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'String t = tr.decode(pair[1], UKLatnTable.{table});\n'
                yield 'assertEquals(pair[0], t);\n'
            else:
                yield f'String t = tr.encode(pair[0], UKLatnTable.{table});\n'
                yield 'assertEquals(pair[1], t);\n'

    def _emit_testset(data, table):
        tpl = '''
private String[][] data_&{table}_&{kind} = {
&data
};
'''
        for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
            xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
            if not xs: continue
            ctx = dict(table=table, kind=kind)
            ctx['data'] = _emit_testdata(kind, xs, table)
            yield template.format(tpl, ctx)

        def _tests():
            tpl = '''\
for (String[] pair : data_&{table}_&{kind}) {
    &tests
}
'''
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                ctx = dict(table=table, kind=kind)
                ctx['tests'] = _emit_tests(kind, table)
                yield template.format(tpl, ctx)

        tpl = '''
@Test
void test_&table() {
    &tests
}
'''
        yield template.format(tpl, table=table, tests=_tests)

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
package io.github.paiv.uklatn;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static io.github.paiv.uklatn.UkrainianLatin.UKLatnTable;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import io.github.paiv.uklatn.UkrainianLatin;

class UkrainianLatinTest {
    private UkrainianLatin tr;

    @BeforeEach
    void setUp() {
        tr = new UkrainianLatin();
    }
    &test_cases
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
                yield f'private Pattern _rx{sid};\n'
                yield f'private Function<MatchResult,String> _tr{sid};\n'

    def _emit_trrules(rules):
        tpl = '''\
this._rx&sid = Pattern.compile(&rx);
List<Map<String,String>> _maps&sid = List.of(
    &mappings
);
this._tr&sid = (match) -> {
    for (int i = match.groupCount(); i > 0; i -= 1) {
        String value = match.group(i);
        if (value != null) {
            return _maps&sid.get(i-1).getOrDefault(value, value);
        }
    }
    return match.group();
};
'''
        mpl = '''\
Map.ofEntries(
    &entries
)'''
        def _ds(data):
            return ','.join(f'entry({_j(k)},{_j(v)})' for k,v in data.items()) + '\n'

        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                data = ',\n'.join(template.format(mpl, entries=_ds(d)) for d in maps) + '\n'
                yield template.format(tpl, sid=sid, rx=_j(rx), mappings=data)

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'text = Normalizer.normalize(text, Normalizer.Form.{section});\n'
            else:
                yield f'text = this._rx{sid}.matcher(text).replaceAll(this._tr{sid});\n'

    def _emit_tr(cname, rules):
        context = dict(cname=cname)
        context['trdefs'] = _emit_trdefs(rules)
        context['trrules'] = _emit_trrules(rules)
        context['trbody'] = _emit_trbody(rules)
        tpl = '''
private static class &cname implements _UKLatnTransformer {
    &trdefs

    &cname() {
        &trrules
    }

    @Override
    public String transform(String text) {
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
                enc,dec = codec
                enc = f'new {enc[0]}()' if enc else 'null'
                dec = f'new {dec[0]}()' if dec else 'null'
                yield f'{{{enc}, {dec}}},\n'

        tpl = '''
private static _UKLatnTransformer[][] _UklatnTables = {
    {null, null},
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
                doc = f'/** {doc} */\n'
            yield f'\n{doc}public static final int {t} = {i};\n'

    context = dict()
    context['table_enum'] = _emit_tenum
    context['global_tables'] = _emit_tables
    context['default_table'] = default_table

    tpl = '''\
package io.github.paiv.uklatn;

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
public final class UkrainianLatin {

    /**
    * Transliteration system
    */
    public static final class UKLatnTable {
        &{table_enum}
    }

    /**
    * Transliterates a string of Ukrainian Cyrillic to Latin script,
    * using {@link UKLatnTable#&{default_table}}.
    *
    * @param text the text to transliterate
    * @return transliterated text
    */
    public String encode(String text) {
        return encode(text, UKLatnTable.&{default_table});
    }

    /**
    * Transliterates a string of Ukrainian Cyrillic to Latin script.
    *
    * @param text the text to transliterate
    * @param table transliteration system, see {@link UKLatnTable}
    * @return transliterated text
    */
    public String encode(String text, int table) {
        _UKLatnTransformer tr = null;
        if (table >= 0 && table < _UklatnTables.length) {
            _UKLatnTransformer[] codecs = _UklatnTables[table];
            if (codecs != null) { tr = codecs[0]; }
        }
        if (tr == null) { throw new IllegalArgumentException("invalid table " + String.valueOf(table)); }
        return tr.transform(text);
    }

    /**
    * Re-transliterates a string of Ukrainian Latin to Cyrillic script,
    * using {@link UKLatnTable#&{default_table}}.
    *
    * @param text the text to transliterate
    * @return transliterated text
    */
    public String decode(String text) {
        return decode(text, UKLatnTable.&{default_table});
    }

    /**
    * Re-transliterates a string of Ukrainian Latin to Cyrillic script.
    *
    * @param text the text to transliterate
    * @param table transliteration system, see {@link UKLatnTable}
    * @return transliterated text
    */
    public String decode(String text, int table) {
        _UKLatnTransformer tr = null;
        if (table >= 0 && table < _UklatnTables.length) {
            _UKLatnTransformer[] codecs = _UklatnTables[table];
            if (codecs != null) { tr = codecs[1]; }
        }
        if (tr == null) { throw new IllegalArgumentException("invalid table " + String.valueOf(table)); }
        return tr.transform(text);
    }

    private static interface _UKLatnTransformer {
        String transform(String text);
    }
    &{global_tables}
}
'''
    text = template.format(tpl, context)
    return text

