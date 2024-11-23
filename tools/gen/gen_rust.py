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
    def camel(s):
        return ''.join(s.title() for s in re.findall(r'[A-Za-z]+|[0-9]+', s))

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
            yield f'let q = encode(cyr, Table::{table});\n'
            yield 'assert_eq!(q, lat);\n'
        else:
            yield f'let q = decode(lat, Table::{table});\n'
            yield 'assert_eq!(q, cyr);\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'let t = decode(lat, Table::{table});\n'
                yield 'assert_eq!(t, cyr);\n'
            else:
                yield f'let t = encode(cyr, Table::{table});\n'
                yield 'assert_eq!(t, lat);\n'

    def _emit_tests_default(kind):
        if kind[0] == 'c':
            yield 'let q = encode(cyr, Table::default());\n'
            yield 'assert_eq!(q, lat);\n'
        else:
            yield 'let q = decode(lat, Table::default());\n'
            yield 'assert_eq!(q, cyr);\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield 'let t = decode(lat, Table::default());\n'
                yield 'assert_eq!(t, cyr);\n'
            else:
                yield 'let t = encode(cyr, Table::default());\n'
                yield 'assert_eq!(t, lat);\n'

    def _emit_testset(data, table):
        tpl = '''
        #[test]
        fn &{table}_t&{tid}&ex() {
            let cyr = &cyr;
            let lat = &lat;
            &tests
        }
        '''
        cname = camel(table)
        lname = cname.lower()
        for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
            xs = [(i,cyr,lat) for i,(k,cyr,lat) in enumerate(data, 1) if k == kind]
            if not xs: continue
            ctx = dict(table=lname, kind=kind)
            for tid, cyr, lat in xs:
                ctx['tests'] = _emit_tests(kind, cname)
                yield template.format(tpl, ctx, tid=tid, ex='', cyr=_j(cyr), lat=_j(lat))
                if table == default_table:
                    ctx['tests'] = _emit_tests_default(kind)
                    yield template.format(tpl, ctx, tid=tid, ex='_default', cyr=_j(cyr), lat=_j(lat))

        if data and all(k == 'c2l' for k,_,_ in data):
            tpl = '''
            #[test]
            #[should_panic]
            fn &{lname}_decode_panic() {
                decode(" ", Table::&cname);
            }
            '''
            yield template.format(tpl, cname=cname, lname=lname)

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
    use {uklatn::decode, uklatn::encode, uklatn::Table};
    &{test_cases}
    '''
    text = template.format(tpl, context)
    return text


def gen_transforms(fns, default_table=None):
    def table_name(s):
        s, = re.findall(r'uk_Latn_(.*?)(?:-uk)?\s*$', s, flags=re.I)
        return s.replace('-', '_')
    def _isdec(s):
        return s.startswith('uk_Latn_')
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def camel(s):
        return ''.join(s.title() for s in re.findall(r'[A-Za-z]+|[0-9]+', s))

    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s),
            [r['map'] for r in s]
        ] for s in data]

    def _emit_trrules(rules):
        tpl = '''\
        static RX&sid: Lazy<Regex> = Lazy::new(|| {
            let rx: &str = r"&rx";
            Regex::new(rx).unwrap()
        });
        '''
        mpl = '''\
        static M&sid&mid: &[(&str, &str); &mn] = &[
            &mappi
        ];
        '''
        kvl = '(&k, &v),\n'
        qpl = '''
        let tr&sid = |caps: &Captures| -> String {
            if let Some(m) = caps.get(1) {
                let s = m.as_str();
                for p in M&{sid}1 {
                    if p.0 == s {
                        return p.1.to_string();
                    }
                }
                return s.to_string();
            &mappi
            } else {
                caps[0].to_string()
            }
        };
        '''
        rtl = '''\
        } else if let Some(m) = caps.get(&mid) {
            let s = m.as_str();
            for p in M&sid&mid {
                if p.0 == s {
                    return p.1.to_string();
                }
            }
            return s.to_string();
        '''
        def _trs(maps):
            for mid in range(2, len(maps)+1):
                yield template.format(rtl, sid=sid, mid=mid)
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                yield template.format(tpl, sid=sid, rx=rx)
                for mid, d in enumerate(maps, 1):
                    ms = (template.format(kvl, k=_j(k), v=_j(v)) for k,v in d.items())
                    yield template.format(mpl, sid=sid, mid=mid, mn=len(d), mappi=ms)
                yield template.format(qpl, sid=sid, mappi=_trs(maps))

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'let text = text.{section.lower()}().collect::<String>();\n'
            else:
                yield f'let text = RX{sid}.replace_all(&text, tr{sid});'

    def _emit_tr(cname, verb, rules):
        ctx = dict(cname=cname, verb=verb, lname=cname.lower())
        ctx['trrules'] = _emit_trrules(rules)
        ctx['trbody'] = _emit_trbody(rules)
        tpl = '''
        fn &{verb}_&{lname}(text: &str) -> String {
            &trrules
            &trbody
            text
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
        cname = camel(table)
        if table not in tables:
            tables[table] = [None, None]
        tables[table][_isdec(name)] = (cname, rules)

    def _emit_tables():
        for ar in [0,1]:
            for table, codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    verb = ['encode', 'decode'][ar]
                    yield _emit_tr(cname, verb, rules)

    def _emit_match_tables(verb):
        ar = ['encode', 'decode'].index(verb)
        for table, codec in tables.items():
            if codec[ar] is not None:
                cname, _ = codec[ar]
                lname = cname.lower()
                yield f'Table::{cname} => {verb}_{lname}(text),'
            else:
                cname = camel(table)
                yield f'Table::{cname} => panic!("invalid table {{:?}}", table),'

    tdoc = {
        'DSTU_9112_A': 'DSTU 9112:2021 System A',
        'DSTU_9112_B': 'DSTU 9112:2021 System B',
        'KMU_55': 'KMU 55:2010, not reversible',
    }
    def _emit_tenum():
        for i, t in enumerate(tables, 1):
            if (doc := tdoc.get(t, '')):
                yield f'/// {doc}\n'
            if t == default_table:
                yield '#[default]'
            n = camel(t)
            yield f'{n} = {i},\n'

    context = dict()
    context['tables_enum'] = _emit_tenum
    context['global_tables'] = _emit_tables
    context['match_encode'] = _emit_match_tables('encode')
    context['match_decode'] = _emit_match_tables('decode')

    tpl = '''\
//! Ukrainian Cyrillic transliteration to and from Latin script.
//!
//! Tables:
//! - DSTU 9112:2021 System A
//! - DSTU 9112:2021 System B
//! - KMU 55:2010, not reversible
//!
//! # Examples
//! ```
//! let s = uklatn::encode("Доброго вечора!", uklatn::Table::default());
//! assert_eq!(s, "Dobroğo večora!");
//! ```
//! ```
//! let s = uklatn::decode("Paljanycja", uklatn::Table::default());
//! assert_eq!(s, "Паляниця");
//! ```
//!
//! Select a transliteration scheme:
//! ```
//! let s = uklatn::encode("Борщ", uklatn::Table::Dstu9112B);
//! assert_eq!(s, "Borshch");
//! ```
//!
use {
    once_cell::sync::Lazy, fancy_regex::Captures, fancy_regex::Regex,
    unicode_normalization::UnicodeNormalization,
};

#[derive(Default, Debug)]
pub enum Table {
    &{tables_enum}
}


/// Transliterates a string of Ukrainian Cyrillic to Latin script.
///
/// # Examples
/// ```
/// let s = uklatn::encode("Доброго вечора!", uklatn::Table::default());
/// assert_eq!(s, "Dobroğo večora!");
/// ```
/// ```
/// let s = uklatn::encode("Шевченко", uklatn::Table::Kmu55);
/// assert_eq!(s, "Shevchenko");
/// ```
pub fn encode(text: &str, table: Table) -> String {
    match table {
        &{match_encode}
    }
}

/// Re-transliterates a string of Ukrainian Latin to Cyrillic script.
///
/// # Examples
/// ```
/// let s = uklatn::decode("Paljanycja", uklatn::Table::default());
/// assert_eq!(s, "Паляниця");
/// ```
/// ```
/// let s = uklatn::decode("Shevchenko", uklatn::Table::Dstu9112B);
/// assert_eq!(s, "Шевченко");
/// ```
///
pub fn decode(text: &str, table: Table) -> String {
    match table {
        &{match_decode}
    }
}
&{global_tables}
'''
    text = template.format(tpl, context)
    return text

