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
        return re.sub(r'test_', '', s, flags=re.I).replace('-', '_')
    def class_name(s):
        return re.sub(r'test|_', '', s.title(), flags=re.I)
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def all_c2l(data):
        return all(k == 'c2l' for k,_,_ in data)
    def _emit_tests(kind, data, table, file):
        data = [(cyr,lat) for k,cyr,lat in data if k == kind]
        if not data: return
        print('', file=file)
        print(f'    func test_{kind}_{table}() throws {{', file=file)
        vs, ws = ' ' * 8, ' ' * 12
        dump = '[\n' + ''.join(f'{vs}(\n{ws}{_j(cyr)},\n{ws}{_j(lat)}\n{vs}),\n' for cyr,lat in data) + '        ]\n'
        print(f'        let data: [(String, String)] = {dump}', file=file)
        print('        for (cyr,lat) in data {', file=file)
        if kind[0] == 'c':
            print(f'            let enc = try encode(cyr, table: UKLatnTable.{table})', file=file)
            print(f'            XCTAssertEqual(lat, enc)', file=file)
        else:
            print(f'            let dec = try decode(lat, table: UKLatnTable.{table})', file=file)
            print(f'            XCTAssertEqual(cyr, dec)', file=file)
        if kind[-1] == 'r':
            if kind[0] == 'c':
                print(f'            let dec = try decode(lat, table: UKLatnTable.{table})', file=file)
                print(f'            XCTAssertEqual(cyr, dec)', file=file)
            else:
                print(f'            let enc = try encode(cyr, table: UKLatnTable.{table})', file=file)
                print(f'            XCTAssertEqual(lat, enc)', file=file)
        print('        }', file=file)
        print('    }', file=file)
    def _emit_decode_throws(table, file):
        print(f'''
    func test_decode_{table}_throws() throws {{
        XCTAssertThrowsError(
            try decode("lat", table: UKLatnTable.{table})
        ) {{ error in
            XCTAssertEqual(error as? UKLatnError, UKLatnError.invalidTable(UKLatnTable.{table}.rawValue))
        }}
    }}''', file=file)

    with io.StringIO() as so:
        print('import XCTest', file=so)
        print('@testable import UkrainianLatin', file=so)
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            cname = class_name(name)
            data = _parse_tests(fn)
            print(f'\n\nclass {cname}Tests: XCTestCase {{', file=so)
            _emit_tests('c2lr', data, table, file=so)
            _emit_tests('l2cr', data, table, file=so)
            _emit_tests('c2l', data, table, file=so)
            _emit_tests('l2c', data, table, file=so)
            if all_c2l(data):
                _emit_decode_throws(table, file=so)
            print('}', file=so)

        return so.getvalue()


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

    def _emit_tr(cname, rules, file):
        rules = _load_rules(rules)
        norms = dict(zip('NFC NFD NFKC NFKD'.split(), '''
        precomposedStringWithCanonicalMapping
        decomposedStringWithCanonicalMapping
        precomposedStringWithCompatibilityMapping
        decomposedStringWithCompatibilityMapping
        '''.split()))
        print(f'private let {cname}: @Sendable () -> _UKLatnCodec.Transform = {{', file=file)
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                gn = len(maps)
                print(f'        let _rx{sid} = try! NSRegularExpression(pattern: #"{rx}"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])', file=file)
                print(f'        let _maps{sid}:[[String:String]] = [[:], ', file=file)
                for d in maps:
                    ds = '[' + ','.join(f'{_j(k)}:{_j(v)}' for k,v in d.items()) + ']' if d else '[:]'
                    print(f'            {ds},', file=file)
                print(f'        ]', file=file)
        print('    @Sendable', file=file)
        print('    func transform(_ text: String) throws -> String {', file=file)
        print('        var text = text', file=file)
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                norm = norms[section]
                print(f'        text = text.{norm} // {section}', file=file)
            else:
                rx, maps = section
                print(f'        text = text.replacing(_rx{sid}) {{ (i, match) in', file=file)
                print(f'            _maps{sid}[i][match] ?? match', file=file)
                print(f'        }}', file=file)
        print('''        return text
    }
    return transform
}
''', file=file)

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
        print('private let _UklatnTables: [UKLatnTable:_UKLatnCodec] = [', file=so)
        for tid, (table, (enc, dec)) in enumerate(tables.items(), 1):
            enc = f'{enc}()' if enc else 'nil'
            dec = f'{dec}()' if dec else 'nil'
            print(f'    .{table}: _UKLatnCodec(encode: {enc}, decode: {dec}),', file=so)
        print(']', end='', file=so)
        tabledef = so.getvalue()

    context['global_tables'] = classdefs_tables + tabledef
    context['default_table'] = default_table
    context['tables_enum'] = '\n'.join(f'    case {t} = {i}' for i,t in enumerate(tables, 1))

    context['string_replacing'] = '''private extension Range where Bound == String.UTF16View.Index {

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
}'''

    template = '''/* uklatn - https://github.com/paiv/uklatn */
import Foundation


public enum UKLatnError: Error, Equatable {{
    case invalidTable(Int)
}}


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
public func encode(_ text: String, table: UKLatnTable = .{default_table}) throws -> String {{
    guard let transform = _UklatnTables[table]?.encode
    else {{
        throw UKLatnError.invalidTable(table.rawValue)
    }}
    return try transform(text)
}}


/// Re-transliterates a string of Ukrainian Latin to Cyrillic script.
///
/// - Parameters:
///   - text: the text to transliterate
///   - table: transliteration system, one of:
///     - `DSTU_9112_A`: DSTU 9112:2021 System A
///     - `DSTU_9112_B`: DSTU 9112:2021 System B
/// - Returns: The transliterated string.
@Sendable
public func decode(_ text: String, table: UKLatnTable = .{default_table}) throws -> String {{
    guard let transform = _UklatnTables[table]?.decode
    else {{
        throw UKLatnError.invalidTable(table.rawValue)
    }}
    return try transform(text)
}}


{string_replacing}


public enum UKLatnTable : Int, Sendable {{
{tables_enum}
}}


private struct _UKLatnCodec : Sendable {{
    typealias Transform = (@Sendable (String) throws -> String)
    let encode: Transform?
    let decode: Transform?
}}


{global_tables}
'''
    text = template.format(**context)
    return text

