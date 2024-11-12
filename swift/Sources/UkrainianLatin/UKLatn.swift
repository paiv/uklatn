/* Generated by gentables.py, do not edit. */

/* uklatn - https://github.com/paiv/uklatn */
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
public func encode(_ text: String, table: UKLatnTable = .DSTU_9112_A) throws -> String {
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
public func decode(_ text: String, table: UKLatnTable = .DSTU_9112_A) throws -> String {
    guard let transform = _UklatnTables[table]?.decode
    else {
        throw UKLatnError.invalidTable(table.rawValue)
    }
    return try transform(text)
}


private extension Range where Bound == String.UnicodeScalarView.Index {

    init?(_ range: NSRange, in view: String.UnicodeScalarView) {
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
                        if let range = Range(range, in: unicodeScalars) {
                            let s = unicodeScalars[range]
                            so += replacement(i, String(s))
                            return
                        }
                    }
                }
            }
        }
        return so
    }
}


public enum UKLatnTable : Int {
    case DSTU_9112_A = 1
    case DSTU_9112_B = 2
    case KMU_55 = 3
}


private struct _UKLatnCodec {
    typealias Transform = ((String) throws -> String)
    let encode: Transform?
    let decode: Transform?
}


private let _Uklatn_uk_uk_Latn_DSTU_9112_A: () -> _UKLatnCodec.Transform = {
        let _rx1 = try! NSRegularExpression(pattern: #"\b([Ьь])|([Ьь](?=[АаЕеУу])|[ЄЮЯ](?=\u0301?[а-щьюяєіїґ’])|(?<=[Б-ДЖЗК-НП-ТФ-Щб-джзк-нп-тф-щҐґ])[Йй])|([ЁЄІЇЎА-яёєіїўҐґ’])|(.)"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps1:[[String:String]] = [[:], 
            ["Ь":"Ĵ","ь":"ĵ"],
            ["Ь":"J'","ь":"j'","Є":"Je","Ю":"Ju","Я":"Ja","Й":"'J","й":"'j"],
            ["А":"A","а":"a","Б":"B","б":"b","В":"V","в":"v","Г":"Ğ","г":"ğ","Ґ":"G","ґ":"g","Д":"D","д":"d","Е":"E","е":"e","Є":"JE","є":"je","Ж":"Ž","ж":"ž","З":"Z","з":"z","И":"Y","и":"y","І":"I","і":"i","Ї":"Ï","ї":"ï","К":"K","к":"k","Л":"L","л":"l","М":"M","м":"m","Н":"N","н":"n","О":"O","о":"o","П":"P","п":"p","Р":"R","р":"r","С":"S","с":"s","Т":"T","т":"t","У":"U","у":"u","Ф":"F","ф":"f","Х":"X","х":"x","Ц":"C","ц":"c","Ч":"Č","ч":"č","Ш":"Š","ш":"š","Щ":"Ŝ","щ":"ŝ","Ю":"JU","ю":"ju","Я":"JA","я":"ja","Ь":"J","ь":"j","Й":"J","й":"j","’":"'","Ё":"Ö","ё":"ö","Ў":"Ŭ","ў":"ŭ","Ъ":"Ǒ","ъ":"ǒ","Ы":"Ȳ","ы":"ȳ","Э":"Ē","э":"ē"],
            [:],
        ]
    func transform(_ text: String) throws -> String {
        var text = text
        text = text.precomposedStringWithCanonicalMapping // NFC
        text = text.replacing(_rx1) { (i, match) in
            _maps1[i][match] ?? match
        }
        text = text.precomposedStringWithCanonicalMapping // NFC
        return text
    }
    return transform
}

private let _Uklatn_uk_uk_Latn_DSTU_9112_B: () -> _UKLatnCodec.Transform = {
        let _rx1 = try! NSRegularExpression(pattern: #"([Ьь](?=[АаЕеІіУу])|(?<=[Б-ДЖЗК-НП-ТФ-Щб-джзк-нп-тф-щҐґ])[Йй])|([ГЄЖЇХЩШЧЮЯЁЎЪЫЭ](?=\u0301?[а-яёєіїўґ’])|\b[Ьь])|([ЁЄІЇЎА-яёєіїўҐґ’])|(.)"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps1:[[String:String]] = [[:], 
            ["Ь":"J'","ь":"j'","Й":"'J","й":"'j"],
            ["Г":"Gh","Є":"Je","Ж":"Zh","Ї":"Ji","Х":"Kh","Щ":"Shch","Ш":"Sh","Ч":"Ch","Ю":"Ju","Я":"Ja","Ё":"Jow","Ў":"Uh","Ъ":"Oh","Ы":"Yw","Э":"Ehw","Ь":"Hj","ь":"hj"],
            ["А":"A","а":"a","Б":"B","б":"b","В":"V","в":"v","Г":"GH","г":"gh","Ґ":"G","ґ":"g","Д":"D","д":"d","Е":"E","е":"e","Є":"JE","є":"je","Ж":"ZH","ж":"zh","З":"Z","з":"z","И":"Y","и":"y","І":"I","і":"i","Ї":"JI","ї":"ji","Х":"KH","х":"kh","К":"K","к":"k","Л":"L","л":"l","М":"M","м":"m","Н":"N","н":"n","О":"O","о":"o","П":"P","п":"p","Р":"R","р":"r","Щ":"SHCH","щ":"shch","Ш":"SH","ш":"sh","С":"S","с":"s","Т":"T","т":"t","У":"U","у":"u","Ф":"F","ф":"f","Ч":"CH","ч":"ch","Ц":"C","ц":"c","Ю":"JU","ю":"ju","Я":"JA","я":"ja","Й":"J","й":"j","Ь":"J","ь":"j","’":"'","Ё":"JOW","ё":"jow","Ў":"UH","ў":"uh","Ъ":"OH","ъ":"oh","Ы":"YW","ы":"yw","Э":"EHW","э":"ehw"],
            [:],
        ]
    func transform(_ text: String) throws -> String {
        var text = text
        text = text.precomposedStringWithCanonicalMapping // NFC
        text = text.replacing(_rx1) { (i, match) in
            _maps1[i][match] ?? match
        }
        text = text.precomposedStringWithCanonicalMapping // NFC
        return text
    }
    return transform
}

private let _Uklatn_uk_uk_Latn_KMU_55: () -> _UKLatnCodec.Transform = {
        let _rx1 = try! NSRegularExpression(pattern: #"(?<=[ЁЄІЇЎА-яёєіїўҐґ])([’\u0027])(?=[ЁЄІЇЎА-яёєіїўҐґ])|(.)"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps1:[[String:String]] = [[:], 
            ["’":"","'":""],
            [:],
        ]
        let _rx2 = try! NSRegularExpression(pattern: #"\b([ЄЇЮЯ])(?=\u0301?[а-яёєіїўґ’])|\b([ЙйЄЇЮЯєїюя])|([Зз]Г|[ЖХЦЩШЧЄЇЮЯ])(?=\u0301?[а-яёєіїўґ’])|([Зз][Гг]|[ЄІЇА-ЩЬЮ-щьюяєіїҐґ’])|(.)"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps2:[[String:String]] = [[:], 
            ["Є":"Ye","Ї":"Yi","Ю":"Yu","Я":"Ya"],
            ["Й":"Y","й":"y","Є":"YE","є":"ye","Ї":"YI","ї":"yi","Ю":"YU","ю":"yu","Я":"YA","я":"ya"],
            ["ЗГ":"ZGh","зГ":"zGh","Ж":"Zh","Х":"Kh","Ц":"Ts","Щ":"Shch","Ш":"Sh","Ч":"Ch","Є":"Ie","Ї":"I","Ю":"Iu","Я":"Ia"],
            ["ЗГ":"ZGH","Зг":"Zgh","зГ":"zGH","зг":"zgh","А":"A","а":"a","Б":"B","б":"b","В":"V","в":"v","Г":"H","г":"h","Ґ":"G","ґ":"g","Д":"D","д":"d","Е":"E","е":"e","Є":"IE","є":"ie","Ж":"ZH","ж":"zh","З":"Z","з":"z","И":"Y","и":"y","І":"I","і":"i","Ї":"I","ї":"i","Х":"KH","х":"kh","К":"K","к":"k","Л":"L","л":"l","М":"M","м":"m","Н":"N","н":"n","О":"O","о":"o","П":"P","п":"p","Р":"R","р":"r","Щ":"SHCH","щ":"shch","Ш":"SH","ш":"sh","С":"S","с":"s","Т":"T","т":"t","У":"U","у":"u","Ф":"F","ф":"f","Ч":"CH","ч":"ch","Ц":"TS","ц":"ts","Ю":"IU","ю":"iu","Я":"IA","я":"ia","Й":"I","й":"i","Ь":"","ь":"","’":""],
            [:],
        ]
    func transform(_ text: String) throws -> String {
        var text = text
        text = text.precomposedStringWithCanonicalMapping // NFC
        text = text.replacing(_rx1) { (i, match) in
            _maps1[i][match] ?? match
        }
        text = text.replacing(_rx2) { (i, match) in
            _maps2[i][match] ?? match
        }
        text = text.precomposedStringWithCanonicalMapping // NFC
        return text
    }
    return transform
}

private let _Uklatn_uk_Latn_DSTU_9112_A_uk: () -> _UKLatnCodec.Transform = {
        let _rx1 = try! NSRegularExpression(pattern: #"([ÁáÉéÍíÓóÚúÝýḮḯ])|(.)"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps1:[[String:String]] = [[:], 
            ["Á":"Á","á":"á","É":"É","é":"é","Í":"Í","í":"í","Ó":"Ó","ó":"ó","Ú":"Ú","ú":"ú","Ý":"Ý","ý":"ý","Ḯ":"Ḯ","ḯ":"ḯ"],
            [:],
        ]
        let _rx2 = try! NSRegularExpression(pattern: #"(J[Ee]|j[Ee]|J[Uu]|j[Uu]|J[Aa]|j[Aa]|[A-GIK-PR-VXYZa-gik-pr-vxyzÏÖïöČčĒēĞğĴĵŜŝŠšŬŭŽžǑǒȲȳ])|(?<=[BbCcDdFfGgKkLlMmNnPpRrSsTtVvXxZzČčĞğŜŝŠšŽž])([Jj]\u0027(?=[AaEeUu])|[Jj])|(\u0027[Jj](?![AaEeIiUu])|\u0027(?=[Jj])|[Jj])|(.)"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps2:[[String:String]] = [[:], 
            ["A":"А","a":"а","B":"Б","b":"б","V":"В","v":"в","Ğ":"Г","ğ":"г","G":"Ґ","g":"ґ","D":"Д","d":"д","E":"Е","e":"е","JE":"Є","Je":"Є","jE":"є","je":"є","Ž":"Ж","ž":"ж","Z":"З","z":"з","Y":"И","y":"и","I":"І","i":"і","Ï":"Ї","ï":"ї","K":"К","k":"к","L":"Л","l":"л","M":"М","m":"м","N":"Н","n":"н","O":"О","o":"о","P":"П","p":"п","R":"Р","r":"р","S":"С","s":"с","T":"Т","t":"т","U":"У","u":"у","F":"Ф","f":"ф","X":"Х","x":"х","C":"Ц","c":"ц","Č":"Ч","č":"ч","Š":"Ш","š":"ш","Ŝ":"Щ","ŝ":"щ","JU":"Ю","Ju":"Ю","jU":"ю","ju":"ю","JA":"Я","Ja":"Я","jA":"я","ja":"я","Ĵ":"Ь","ĵ":"ь","Ö":"Ё","ö":"ё","Ŭ":"Ў","ŭ":"ў","Ǒ":"Ъ","ǒ":"ъ","Ȳ":"Ы","ȳ":"ы","Ē":"Э","ē":"э"],
            ["J":"Ь","j":"ь","J'":"Ь","j'":"ь"],
            ["'J":"Й","'j":"й","'":"’","J":"Й","j":"й"],
            [:],
        ]
    func transform(_ text: String) throws -> String {
        var text = text
        text = text.precomposedStringWithCanonicalMapping // NFC
        text = text.replacing(_rx1) { (i, match) in
            _maps1[i][match] ?? match
        }
        text = text.replacing(_rx2) { (i, match) in
            _maps2[i][match] ?? match
        }
        text = text.precomposedStringWithCanonicalMapping // NFC
        return text
    }
    return transform
}

private let _Uklatn_uk_Latn_DSTU_9112_B_uk: () -> _UKLatnCodec.Transform = {
        let _rx1 = try! NSRegularExpression(pattern: #"([ÁáÉéÍíÓóÚúÝý])|(.)"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps1:[[String:String]] = [[:], 
            ["Á":"Á","á":"á","É":"É","é":"é","Í":"Í","í":"í","Ó":"Ó","ó":"ó","Ú":"Ú","ú":"ú","Ý":"Ý","ý":"ý"],
            [:],
        ]
        let _rx2 = try! NSRegularExpression(pattern: #"([Jj][Oo][Ww]|[Ss][Hh][Cc][Hh]|[CcGgKkSsZzUuOo][Hh]|[Yy][Ww]|[Ee][Hh][Ww]|[Jj][EeIiUuAa]|[Hh][Jj]|[A-GIK-PR-VYZa-gik-pr-vyz])|(?<=[Ss][Hh][Cc][Hh])([Jj]\u0027(?=[AaEeIiUu])|[Jj])|(?<=[CcGgKkSsZz][Hh])([Jj]\u0027(?=[AaEeIiUu])|[Jj])|(?<=[BCDFGKLMNPRSTVZbcdfgklmnprstvzv])([Jj]\u0027(?=[AaEeIiUu])|[Jj])|(\u0027[Jj](?![AaEeIiUu])|\u0027(?=[Jj])|[Jj])|(.)"#, options: [.dotMatchesLineSeparators, .useUnicodeWordBoundaries])
        let _maps2:[[String:String]] = [[:], 
            ["A":"А","a":"а","B":"Б","b":"б","V":"В","v":"в","GH":"Г","Gh":"Г","gH":"г","gh":"г","G":"Ґ","g":"ґ","D":"Д","d":"д","E":"Е","e":"е","JE":"Є","Je":"Є","jE":"є","je":"є","ZH":"Ж","Zh":"Ж","zH":"ж","zh":"ж","Z":"З","z":"з","Y":"И","y":"и","I":"І","i":"і","JI":"Ї","Ji":"Ї","jI":"ї","ji":"ї","KH":"Х","Kh":"Х","kH":"х","kh":"х","K":"К","k":"к","L":"Л","l":"л","M":"М","m":"м","N":"Н","n":"н","O":"О","o":"о","P":"П","p":"п","R":"Р","r":"р","SHCH":"Щ","SHCh":"Щ","SHcH":"Щ","SHch":"Щ","ShCH":"Щ","ShCh":"Щ","ShcH":"Щ","Shch":"Щ","sHCH":"щ","sHCh":"щ","sHcH":"щ","sHch":"щ","shCH":"щ","shCh":"щ","shcH":"щ","shch":"щ","SH":"Ш","Sh":"Ш","sH":"ш","sh":"ш","S":"С","s":"с","T":"Т","t":"т","U":"У","u":"у","F":"Ф","f":"ф","CH":"Ч","Ch":"Ч","cH":"ч","ch":"ч","C":"Ц","c":"ц","JU":"Ю","Ju":"Ю","jU":"ю","ju":"ю","JA":"Я","Ja":"Я","jA":"я","ja":"я","HJ":"Ь","Hj":"Ь","hJ":"ь","hj":"ь","JOW":"Ё","JOw":"Ё","JoW":"Ё","Jow":"Ё","jOW":"ё","jOw":"ё","joW":"ё","jow":"ё","UH":"Ў","Uh":"Ў","uH":"ў","uh":"ў","OH":"Ъ","Oh":"Ъ","oH":"ъ","oh":"ъ","YW":"Ы","Yw":"Ы","yW":"ы","yw":"ы","EHW":"Э","EHw":"Э","EhW":"Э","Ehw":"Э","eHW":"э","eHw":"э","ehW":"э","ehw":"э"],
            ["J":"Ь","j":"ь","J'":"Ь","j'":"ь"],
            ["J":"Ь","j":"ь","J'":"Ь","j'":"ь"],
            ["J":"Ь","j":"ь","J'":"Ь","j'":"ь"],
            ["'J":"Й","'j":"й","'":"’","J":"Й","j":"й"],
            [:],
        ]
    func transform(_ text: String) throws -> String {
        var text = text
        text = text.precomposedStringWithCanonicalMapping // NFC
        text = text.replacing(_rx1) { (i, match) in
            _maps1[i][match] ?? match
        }
        text = text.replacing(_rx2) { (i, match) in
            _maps2[i][match] ?? match
        }
        text = text.precomposedStringWithCanonicalMapping // NFC
        return text
    }
    return transform
}

private let _UklatnTables: [UKLatnTable:_UKLatnCodec] = [
    .DSTU_9112_A: _UKLatnCodec(encode: _Uklatn_uk_uk_Latn_DSTU_9112_A(), decode: _Uklatn_uk_Latn_DSTU_9112_A_uk()),
    .DSTU_9112_B: _UKLatnCodec(encode: _Uklatn_uk_uk_Latn_DSTU_9112_B(), decode: _Uklatn_uk_Latn_DSTU_9112_B_uk()),
    .KMU_55: _UKLatnCodec(encode: _Uklatn_uk_uk_Latn_KMU_55(), decode: nil),
]
