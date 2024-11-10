import io
import json
import logging
import re
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
    def _emit_tests(kind, data, table, file):
        data = [(cyr,lat) for k,cyr,lat in data if k == kind]
        if not data: return
        print(f'    await t.test({kind!r}, () => {{', file=so)
        dump = json.dumps(data, indent=4, ensure_ascii=False)
        print(f'       const data = {dump};', file=so)
        print('        for (const [cyr,lat] of data) {', file=so)
        if kind[0] == 'c':
            print(f'            const q = uklatn.encode(cyr, {table!r});', file=so)
            print(f'            assert.equal(q, lat);', file=so)
        else:
            print(f'            const q = uklatn.decode(lat, {table!r});', file=so)
            print(f'            assert.equal(q, cyr);', file=so)
        if kind[-1] == 'r':
            if kind[0] == 'c':
                print(f'            const t = uklatn.decode(lat, {table!r});', file=so)
                print(f'            assert.equal(t, cyr);', file=so)
            else:
                print(f'            const t = uklatn.encode(cyr, {table!r});', file=so)
                print(f'            assert.equal(t, lat);', file=so)
        print('        }', file=so)
        print('    });\n', file=so)

    with io.StringIO() as so:
        print('import assert from "node:assert/strict";', file=so)
        print('import test from "node:test";', file=so)
        print('import * as uklatn from "./uklatn.js";\n', file=so)
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            data = _parse_tests(fn)
            print(f'test({table!r}, async (t) => {{', file=so)
            _emit_tests('c2lr', data, table, file=so)
            _emit_tests('l2cr', data, table, file=so)
            _emit_tests('c2l', data, table, file=so)
            _emit_tests('l2c', data, table, file=so)
            print('});\n', file=so)

        return so.getvalue()


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

    def _emit_tr(cname, rules, file):
        rules = _load_rules(rules)
        print(f'class {cname} {{', file=file)
        print('    constructor() {', file=file)
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                gn = len(maps)
                rx = patch_word_boundary(rx)
                print(f'        this._rx{sid} = /{rx}/gu;', file=file)
                print(f'        const _maps{sid} = [undefined, ', file=file)
                for d in maps:
                    ds = [[k,v] for k,v in d.items()]
                    ds = json.dumps(ds, separators=',;', ensure_ascii=False)
                    print(f'            new Map({ds}),', file=file)
                print(f'        ];', file=file)
                print(f'        this._tr{sid} = (match', end='', file=file)
                for i in range(1, gn+1):
                    print(f', g{i}', end='', file=file)
                print(') => {', file=file)
                print(f'            let value = undefined;', file=file)
                print(f'            if (g{gn} !== undefined) {{', file=file)
                print(f'                value = _maps{sid}[{gn}].get(g{gn});', file=file)
                print(f'            }}', file=file)
                for i in reversed(range(1, gn)):
                    print(f'            else if (g{i} !== undefined) {{', file=file)
                    print(f'                value = _maps{sid}[{i}].get(g{i});', file=file)
                    print(f'            }}', file=file)
                print(f'            return (value !== undefined) ? value : match;', file=file)
                print(f'        }}', file=file)
        print('    }\n', file=file)
        print('    transform(text) {', file=file)
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                print(f'        text = text.normalize({section!r});', file=file)
            else:
                print(f'        text = text.replaceAll(this._rx{sid}, this._tr{sid});', file=file)
        print(f'        return text;', file=file)
        print('    }', file=file)
        print('}\n\n', file=file)

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
        classdefs_tables = so.getvalue()

    with io.StringIO() as so:
        print('const _UklatnTables = new Map([', file=so)
        for tid, (table, (enc, dec)) in enumerate(tables.items(), 1):
            enc = f'new {enc}()' if enc else 'undefined'
            dec = f'new {dec}()' if dec else 'undefined'
            print(f'    [{table!r}, [{enc}, {dec}]],', file=so)
        print(']);', end='', file=so)
        tabledef = so.getvalue()

    context['global_tables'] = classdefs_tables + tabledef
    context['default_table'] = default_table

    template = '''/* uklatn.js - https://github.com/paiv/uklatn */

{global_tables}


/**
* Transliterates a string of Ukrainian Cyrillic to Latin script.
*
* @param {{string}} text - the text to transliterate
* @param {{string}} table - transliteration system, one of:
*  - "DSTU_9112_A": DSTU 9112:2021 System A
*  - "DSTU_9112_B": DSTU 9112:2021 System B
*  - "KMU_55": KMU 55:2010
*/
export function encode(text, table) {{
    if (table === undefined) {{ table = {default_table!r}; }}
    const codecs = _UklatnTables.get(table);
    let tr = undefined;
    if (codecs) {{ tr = codecs[0]; }}
    if (tr === undefined) {{ throw new Error("unknown table " + JSON.stringify(table)); }}
    return tr.transform(text);
}}


/**
* Re-transliterates a string of Ukrainian Latin to Cyrillic script.
*
* @param {{string}} text - the text to transliterate
* @param {{string}} table - transliteration system, one of:
*  - "DSTU_9112_A": DSTU 9112:2021 System A
*  - "DSTU_9112_B": DSTU 9112:2021 System B
*/
export function decode(text, table) {{
    if (table === undefined) {{ table = {default_table!r}; }}
    const codecs = _UklatnTables.get(table);
    let tr = undefined;
    if (codecs) {{ tr = codecs[1]; }}
    if (tr === undefined) {{ throw new Error("unknown table " + JSON.stringify(table)); }}
    return tr.transform(text);
}}


export default {{ encode, decode }};
'''
    text = template.format(**context)
    return text

