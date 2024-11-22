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
        return re.sub(r'test_', '', s, flags=re.I).replace('-', '_')
    def class_name(s):
        return re.sub(r'test|_', '', s.title(), flags=re.I)
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def all_c2l(data):
        return all(k == 'c2l' for k,_,_ in data)

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'let enc = try encode(cyr, table: UKLatnTable.{table})\n'
            yield 'XCTAssertEqual(lat, enc)\n'
        else:
            yield f'let dec = try decode(lat, table: UKLatnTable.{table})\n'
            yield 'XCTAssertEqual(cyr, dec)\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'let dec = try decode(lat, table: UKLatnTable.{table})\n'
                yield 'XCTAssertEqual(cyr, dec)\n'
            else:
                yield f'let enc = try encode(cyr, table: UKLatnTable.{table})\n'
                yield 'XCTAssertEqual(lat, enc)\n'

    def _emit_tests_default(kind):
        def _tests():
            if kind[0] == 'c':
                yield 'let enc = try encode(cyr)\n'
                yield 'XCTAssertEqual(lat, enc)\n'
            else:
                yield 'let dec = try decode(lat)\n'
                yield 'XCTAssertEqual(cyr, dec)\n'
            if kind[-1] == 'r':
                if kind[0] == 'c':
                    yield 'let dec = try decode(lat)\n'
                    yield 'XCTAssertEqual(cyr, dec)\n'
                else:
                    yield 'let enc = try encode(cyr)\n'
                    yield 'XCTAssertEqual(lat, enc)\n'
        tpl = '''
        for (cyr, lat) in data {
            &tests
        }
        '''
        return template.format(tpl, tests=_tests)

    def _emit_decode_throws(table):
        tpl = '''
        func test_decode_&{table}_throws() throws {
            XCTAssertThrowsError(
                try decode("lat", table: UKLatnTable.&{table})
            ) { error in
                XCTAssertEqual(error as? UKLatnError, UKLatnError.invalidTable(UKLatnTable.&{table}.rawValue))
            }
        }
        '''
        return template.format(tpl, table=table)

    def _emit_testset(data, table, cname):
        def _dump(data):
            tpl = '''\
            (
                &cyr,
                &lat
            ),
            '''
            for cyr, lat in data:
                yield template.format(tpl, cyr=_j(cyr), lat=_j(lat)+'\n')

        def _test_kind(kind, data, table):
            tpl = '''
            func test_&{kind}_&{table}() throws {
                let data: [(String, String)] = [
                &data
                ]

                for (cyr, lat) in data {
                    &tests
                }
                &dtests
            }
            '''
            ctx = dict(kind=kind, table=table)
            ctx['data'] = _dump(data)
            ctx['tests'] = _emit_tests(kind, table)
            ctx['dtests'] = iter('')
            if table == default_table:
                ctx['dtests'] = _emit_tests_default(kind)
            return template.format(tpl, ctx)

        def _tests():
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                yield _test_kind(kind, xs, table)
            if all_c2l(data):
                yield _emit_decode_throws(table)

        tpl = '''

        class &{cname}Tests: XCTestCase {
            &tests
        }
        '''
        return template.format(tpl, cname=cname, tests=_tests)

    def _test_cases():
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            cname = class_name(name)
            data = _parse_tests(fn)
            yield from _emit_testset(data, table, cname)

    context = dict()
    context['test_cases'] = _test_cases

    tpl = '''\
    import XCTest
    @testable import UkrainianLatin
    &{test_cases}
    '''
    text = template.format(tpl, context)
    return text


def gen_transforms(fns, default_table=None):
    def table_name(s):
        s, = re.findall(r'uk_Latn_(.*?)(?:-uk)?\s*$', s, flags=re.I)
        return s.replace('-', '_')
    def class_name(s):
        return '_Uklatn_' + s.replace('-', '_')
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def _isdec(s):
        return s.startswith('uk_Latn_')
    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s) + '|(.)',
            [r['map'] for r in s] + [dict()]
        ] for s in data]

    def _emit_trdefs(rules):
        # Why NSRegularExpression, and not Regex:
        # - no backrefs
        # When backrefs implemented in Regex, and updating this code,
        # use .matchingSemantics(.unicodeScalar)
        # since all other languages operate on code points, and transform tables
        # are designed for it.
        # SE-0448 Regex lookbehind assertions
        # SE-NNNN Unicode Normalization
        tpl = '''\
        let _rx&sid = try! NSRegularExpression(pattern: #"&rx"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps&sid:[[String:String]] = [
            &mappings
        ]
        '''
        mpl = '[&entries]'

        def _ds(data):
            return ','.join(f'{_j(k)}:{_j(v)}' for k,v in data.items()) if data else ':'

        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                data = ',\n'.join(template.format(mpl, entries=_ds(d)) for d in maps) + '\n'
                yield template.format(tpl, sid=sid, rx=rx, mappings=data)

    def _emit_trbody(rules):
        norms = dict(zip('NFC NFD NFKC NFKD'.split(), '''
        precomposedStringWithCanonicalMapping
        decomposedStringWithCanonicalMapping
        precomposedStringWithCompatibilityMapping
        decomposedStringWithCompatibilityMapping
        '''.split()))
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                norm = norms[section]
                yield f'text = text.{norm} // {section}\n'
            else:
                rx, maps = section
                yield f'text = text.replacing(_rx{sid}) {{ (i, match) in\n'
                yield f'    _maps{sid}[i-1][match, default: match]\n}}\n'

    def _emit_tr(cname, rules):
        context = dict(cname=cname)
        context['trdefs'] = _emit_trdefs(rules)
        context['trbody'] = _emit_trbody(rules)
        tpl = '''
        private let &cname: @Sendable () -> _UKLatnCodec.Transform = {
            &trdefs

            @Sendable
            func transform(_ text: String) throws -> String {
                var text = text
                &trbody
                return text
            }
            return transform
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
            for table,codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    yield _emit_tr(cname, rules)

        def _entries():
            for table,codec in tables.items():
                enc,dec = codec
                enc = f'{enc[0]}()' if enc else 'nil'
                dec = f'{dec[0]}()' if dec else 'nil'
                yield f'.{table}: _UKLatnCodec(encode: {enc}, decode: {dec}),\n'

        tpl = '''
        private let _UklatnTables: [UKLatnTable:_UKLatnCodec] = [
            &entries
        ]
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
                doc = f'/// {doc}\n'
            yield f'\n{doc}case {t} = {i}\n'

    context = dict()
    context['tables_enum'] = _emit_tenum
    context['global_tables'] = _emit_tables
    context['default_table'] = default_table

    tpl = '''/* uklatn - https://github.com/paiv/uklatn */
import Foundation


public enum UKLatnError: Error, Equatable {
    case invalidTable(Int)
}


/// Transliterates a string of Ukrainian Cyrillic to Latin script.
///
/// - Parameters:
///   - text: the text to transliterate
///   - table: transliteration system, one of:
///     - `DSTU_9112_A`: DSTU 9112:2021 System A
///     - `DSTU_9112_B`: DSTU 9112:2021 System B
///     - `KMU_55`: KMU 55:2010
/// - Returns: The transliterated string.
@Sendable
public func encode(_ text: String, table: UKLatnTable = .&{default_table}) throws -> String {
    guard let transform = _UklatnTables[table]?.encode
    else {
        throw UKLatnError.invalidTable(table.rawValue)
    }
    return try transform(text)
}


/// Re-transliterates a string of Ukrainian Latin to Cyrillic script.
///
/// - Parameters:
///   - text: the text to transliterate
///   - table: transliteration system, one of:
///     - `DSTU_9112_A`: DSTU 9112:2021 System A
///     - `DSTU_9112_B`: DSTU 9112:2021 System B
/// - Returns: The transliterated string.
@Sendable
public func decode(_ text: String, table: UKLatnTable = .&{default_table}) throws -> String {
    guard let transform = _UklatnTables[table]?.decode
    else {
        throw UKLatnError.invalidTable(table.rawValue)
    }
    return try transform(text)
}


private extension Range where Bound == String.UTF16View.Index {

    init?(_ range: NSRange, in view: String.UTF16View) {
        self = view.index(view.startIndex, offsetBy: range.location) ..< view.index(view.startIndex, offsetBy: range.location + range.length)
    }
}


private extension String {

    func replacing(_ rx: NSRegularExpression, with replacement: @escaping (Int,String) -> String) -> String {
        var so = ""
        rx.enumerateMatches(in: self, range: NSRange(startIndex ..< endIndex, in: self)) { (result: NSTextCheckingResult?, flags: NSRegularExpression.MatchingFlags, stop: UnsafeMutablePointer<ObjCBool>) in
            if let result {
                for i in 1..<result.numberOfRanges {
                    let range = result.range(at: i)
                    if range.location != NSNotFound {
                        if let range = Range(range, in: utf16),
                           let s = String(utf16[range]) {
                            so += replacement(i, s)
                            return
                        }
                    }
                }
            }
        }
        return so
    }
}


public enum UKLatnTable : Int, Sendable {
    &{tables_enum}
}


private struct _UKLatnCodec : Sendable {
    typealias Transform = (@Sendable (String) throws -> String)
    let encode: Transform?
    let decode: Transform?
}

&{global_tables}
'''
    text = template.format(tpl, context)
    return text

