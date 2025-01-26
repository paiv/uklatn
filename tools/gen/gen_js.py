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
            yield f'const q = uklatn.encode(cyr, {table!r});\n'
            yield 'assert.equal(q, lat);\n'
        else:
            yield f'const q = uklatn.decode(lat, {table!r});\n'
            yield 'assert.equal(q, cyr);\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'const t = uklatn.decode(lat, {table!r});\n'
                yield 'assert.equal(t, cyr);\n'
            else:
                yield f'const t = uklatn.encode(cyr, {table!r});\n'
                yield 'assert.equal(t, lat);\n'

    def _emit_tests_default(kind):
        if kind[0] == 'c':
            yield 'const q = uklatn.encode(cyr);\n'
            yield 'assert.equal(q, lat);\n'
        else:
            yield 'const q = uklatn.decode(lat);\n'
            yield 'assert.equal(q, cyr);\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield 'const t = uklatn.decode(lat);\n'
                yield 'assert.equal(t, cyr);\n'
            else:
                yield 'const t = uklatn.encode(cyr);\n'
                yield 'assert.equal(t, lat);\n'

    def _emit_testset(data, table):
        def _data():
            spl = '''
            const data_&kind = [
            &data
            ];
            '''
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                ctx = dict(table=table, kind=kind)
                ctx['data'] = _emit_testdata(kind, xs, table)
                yield template.format(spl, ctx)

        def _tests():
            tpl = '''
            await t.test(&skind, () => {
                for (const [cyr,lat] of data_&kind) {
                    &tests
                }
            });
            '''
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                ctx = dict(table=table, kind=kind, skind=repr(kind))
                ctx['tests'] = _emit_tests(kind, table)
                yield template.format(tpl, ctx)
                if table == default_table:
                    ctx['tests'] = _emit_tests_default(kind)
                    yield template.format(tpl, ctx)

        tpl = '''

        test(&table, async (t) => {
            &data
            &tests
        });
        '''
        yield template.format(tpl, table=repr(table), data=_data, tests=_tests)

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
    import assert from "node:assert/strict";
    import test from "node:test";
    import * as uklatn from "./uklatn.js";
    &{test_cases}
    '''
    text = template.format(tpl, context)
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
    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s),
            [r['map'] for r in s]
        ] for s in data]

    def _emit_trrules(rules):
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                gn = len(maps)
                rx = patch_word_boundary(rx)
                gargs = ', '.join(f'g{i}' for i in range(1, gn+1))

                def _mappings():
                    for d in maps:
                        ds = [[k,v] for k,v in d.items()]
                        ds = json.dumps(ds, separators=',;', ensure_ascii=False)
                        yield f'new Map({ds}),\n'
                def _queries():
                    epl = '''\
                    else if (g&gi !== undefined) {
                        value = _maps&sid[&gi1].get(g&gi);
                    }
                    '''
                    for i in reversed(range(1, gn)):
                        yield template.format(epl, sid=sid, gi=i, gi1=i-1)

                ctx = dict(sid=sid, gn=gn, gn1=gn-1, gargs=gargs, rx=rx)
                ctx['mappings'] = _mappings
                ctx['queries'] = _queries

                tpl = '''\
                this._rx&sid = /&rx/gu;
                const _maps&sid = [
                    &mappings
                ];
                this._tr&sid = (match, &gargs) => {
                    let value = undefined;
                    if (g&gn !== undefined) {
                        value = _maps&sid[&gn1].get(g&gn);
                    }
                    &queries
                    return (value !== undefined) ? value : match;
                }
                '''
                yield template.format(tpl, ctx)

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'text = text.normalize({section!r});\n'
            else:
                yield f'text = text.replaceAll(this._rx{sid}, this._tr{sid});\n'

    def _emit_tr(cname, rules):
        ctx = dict(cname=cname)
        ctx['trrules'] = _emit_trrules(rules)
        ctx['trbody'] = _emit_trbody(rules)
        tpl = '''
        class &cname {
            constructor() {
                &trrules
            }

            transform(text) {
                &trbody
                return text;
            }
        }

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
            for tid, (table, (enc, dec)) in enumerate(tables.items(), 1):
                enc = f'new {enc[0]}()' if enc else 'undefined'
                dec = f'new {dec[0]}()' if dec else 'undefined'
                yield f'[{table!r}, [{enc}, {dec}]],\n'
        tpl = '''
        const _UklatnTables = new Map([
            &entries
        ]);
        '''
        yield template.format(tpl, entries=_entries)

    context = dict()
    context['global_tables'] = _emit_tables
    context['default_table'] = repr(default_table)

    tpl = '''/* uklatn.js - https://github.com/paiv/uklatn */

// @ts-self-types="./uklatn.d.ts"

&{global_tables}


/**
* Transliterates a string of Ukrainian Cyrillic to Latin script.
*
* @param {string} text - the text to transliterate
* @param {string} [table] - transliteration system, one of:
*  - "DSTU_9112_A": DSTU 9112:2021 System A
*  - "DSTU_9112_B": DSTU 9112:2021 System B
*  - "KMU_55": KMU 55:2010
* @returns {string} transliterated text
*/
export function encode(text, table) {
    if (table === undefined) { table = &{default_table}; }
    const codecs = _UklatnTables.get(table);
    let tr = undefined;
    if (codecs) { tr = codecs[0]; }
    if (tr === undefined) { throw new Error("unknown table " + JSON.stringify(table)); }
    return tr.transform(text);
}


/**
* Re-transliterates a string of Ukrainian Latin to Cyrillic script.
*
* @param {string} text - the text to transliterate
* @param {string} [table] - transliteration system, one of:
*  - "DSTU_9112_A": DSTU 9112:2021 System A
*  - "DSTU_9112_B": DSTU 9112:2021 System B
* @returns {string} transliterated text
*/
export function decode(text, table) {
    if (table === undefined) { table = &{default_table}; }
    const codecs = _UklatnTables.get(table);
    let tr = undefined;
    if (codecs) { tr = codecs[1]; }
    if (tr === undefined) { throw new Error("unknown table " + JSON.stringify(table)); }
    return tr.transform(text);
}


export default { encode, decode };
'''
    text = template.format(tpl, context)
    return text

