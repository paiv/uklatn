# Generated by gentables.py, do not edit.


"""Ukrainian Cyrillic transliteration to Latin script

https://github.com/paiv/uklatn

encode(...): tranliterate Cyrlllic to Latin script
decode(...): re-transliterate Latin script back to Cyrillic

Tranliteration schemes:
 - DSTU_9112_A (default)
 - DSTU_9112_B
 - KMU_55

For example,
    >>> import uklatn
    >>> uklatn.encode("Доброго вечора!")
    'Dobroğo večora!'
    >>> uklatn.decode("Paljanycja")
    'Паляниця'

To set the transliteration scheme:
    >>> uklatn.encode("Щастя", table=uklatn.KMU_55)
    'Shchastia'

"""

import re
import unicodedata


__all__ = ['DSTU_9112_A', 'DSTU_9112_B', 'KMU_55', 'decode', 'encode']


DSTU_9112_A = 1
DSTU_9112_B = 2
KMU_55 = 3


class _Uklatn_uk_uk_Latn_DSTU_9112_A:
    def __init__(self):
        self._rx1 = re.compile(r"\b([Ьь])|([Ьь](?=[АаЕеУу])|[ЄЮЯ](?=\u0301?[а-щьюяєіїґ’])|(?<=[Б-ДЖЗК-НП-ТФ-Щб-джзк-нп-тф-щҐґ])[Йй])|(А|а|Б|б|В|в|Г|г|Ґ|ґ|Д|д|Е|е|Є|є|Ж|ж|З|з|И|и|І|і|Ї|ї|К|к|Л|л|М|м|Н|н|О|о|П|п|Р|р|С|с|Т|т|У|у|Ф|ф|Х|х|Ц|ц|Ч|ч|Ш|ш|Щ|щ|Ю|ю|Я|я|Ь|ь|Й|й|’|Ё|ё|Ў|ў|Ъ|ъ|Ы|ы|Э|э)")
        _maps1 = [{'Ь': 'Ĵ', 'ь': 'ĵ'}, {'Ь': "J'", 'ь': "j'", 'Є': 'Je', 'Ю': 'Ju', 'Я': 'Ja', 'Й': "'J", 'й': "'j"}, {'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v', 'Г': 'Ğ', 'г': 'ğ', 'Ґ': 'G', 'ґ': 'g', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e', 'Є': 'JE', 'є': 'je', 'Ж': 'Ž', 'ж': 'ž', 'З': 'Z', 'з': 'z', 'И': 'Y', 'и': 'y', 'І': 'I', 'і': 'i', 'Ї': 'Ï', 'ї': 'ï', 'К': 'K', 'к': 'k', 'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r', 'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f', 'Х': 'X', 'х': 'x', 'Ц': 'C', 'ц': 'c', 'Ч': 'Č', 'ч': 'č', 'Ш': 'Š', 'ш': 'š', 'Щ': 'Ŝ', 'щ': 'ŝ', 'Ю': 'JU', 'ю': 'ju', 'Я': 'JA', 'я': 'ja', 'Ь': 'J', 'ь': 'j', 'Й': 'J', 'й': 'j', '’': "'", 'Ё': 'Ö', 'ё': 'ö', 'Ў': 'Ŭ', 'ў': 'ŭ', 'Ъ': 'Ǒ', 'ъ': 'ǒ', 'Ы': 'Ȳ', 'ы': 'ȳ', 'Э': 'Ē', 'э': 'ē'}]
        def tr1(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps1[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr1 = tr1

    def transform(self, text):
        text = unicodedata.normalize('NFC', text)
        text = self._rx1.sub(self._tr1, text)
        text = unicodedata.normalize('NFC', text)
        return text


class _Uklatn_uk_uk_Latn_DSTU_9112_B:
    def __init__(self):
        self._rx1 = re.compile(r"([Ьь](?=[АаЕеІіУу])|(?<=[Б-ДЖЗК-НП-ТФ-Щб-джзк-нп-тф-щҐґ])[Йй])|([ГЄЖЇХЩШЧЮЯЁЎЪЫЭ](?=\u0301?[а-яёєіїўґ’])|\b[Ьь])|([ЁЄІЇЎА-яёєіїўҐґ’])")
        _maps1 = [{'Ь': "J'", 'ь': "j'", 'Й': "'J", 'й': "'j"}, {'Г': 'Gh', 'Є': 'Je', 'Ж': 'Zh', 'Ї': 'Ji', 'Х': 'Kh', 'Щ': 'Shch', 'Ш': 'Sh', 'Ч': 'Ch', 'Ю': 'Ju', 'Я': 'Ja', 'Ё': 'Jow', 'Ў': 'Uh', 'Ъ': 'Oh', 'Ы': 'Yw', 'Э': 'Ehw', 'Ь': 'Hj', 'ь': 'hj'}, {'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v', 'Г': 'GH', 'г': 'gh', 'Ґ': 'G', 'ґ': 'g', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e', 'Є': 'JE', 'є': 'je', 'Ж': 'ZH', 'ж': 'zh', 'З': 'Z', 'з': 'z', 'И': 'Y', 'и': 'y', 'І': 'I', 'і': 'i', 'Ї': 'JI', 'ї': 'ji', 'Х': 'KH', 'х': 'kh', 'К': 'K', 'к': 'k', 'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r', 'Щ': 'SHCH', 'щ': 'shch', 'Ш': 'SH', 'ш': 'sh', 'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f', 'Ч': 'CH', 'ч': 'ch', 'Ц': 'C', 'ц': 'c', 'Ю': 'JU', 'ю': 'ju', 'Я': 'JA', 'я': 'ja', 'Й': 'J', 'й': 'j', 'Ь': 'J', 'ь': 'j', '’': "'", 'Ё': 'JOW', 'ё': 'jow', 'Ў': 'UH', 'ў': 'uh', 'Ъ': 'OH', 'ъ': 'oh', 'Ы': 'YW', 'ы': 'yw', 'Э': 'EHW', 'э': 'ehw'}]
        def tr1(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps1[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr1 = tr1

    def transform(self, text):
        text = unicodedata.normalize('NFC', text)
        text = self._rx1.sub(self._tr1, text)
        text = unicodedata.normalize('NFC', text)
        return text


class _Uklatn_uk_uk_Latn_KMU_55:
    def __init__(self):
        self._rx1 = re.compile(r"(?<=[ЁЄІЇЎА-яёєіїўҐґ])([’\u0027])(?=[ЁЄІЇЎА-яёєіїўҐґ])")
        _maps1 = [{'’': '', "'": ''}]
        def tr1(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps1[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr1 = tr1
        self._rx2 = re.compile(r"\b([ЄЇЮЯ])(?=\u0301?[а-яёєіїўґ’])|\b([ЙйЄЇЮЯєїюя])|([Зз]Г|[ЖХЦЩШЧЄЇЮЯ])(?=\u0301?[а-яёєіїўґ’])|([Зз][Гг]|[ЄІЇА-ЩЬЮ-щьюяєіїҐґ’])")
        _maps2 = [{'Є': 'Ye', 'Ї': 'Yi', 'Ю': 'Yu', 'Я': 'Ya'}, {'Й': 'Y', 'й': 'y', 'Є': 'YE', 'є': 'ye', 'Ї': 'YI', 'ї': 'yi', 'Ю': 'YU', 'ю': 'yu', 'Я': 'YA', 'я': 'ya'}, {'ЗГ': 'ZGh', 'зГ': 'zGh', 'Ж': 'Zh', 'Х': 'Kh', 'Ц': 'Ts', 'Щ': 'Shch', 'Ш': 'Sh', 'Ч': 'Ch', 'Є': 'Ie', 'Ї': 'I', 'Ю': 'Iu', 'Я': 'Ia'}, {'ЗГ': 'ZGH', 'Зг': 'Zgh', 'зГ': 'zGH', 'зг': 'zgh', 'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v', 'Г': 'H', 'г': 'h', 'Ґ': 'G', 'ґ': 'g', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e', 'Є': 'IE', 'є': 'ie', 'Ж': 'ZH', 'ж': 'zh', 'З': 'Z', 'з': 'z', 'И': 'Y', 'и': 'y', 'І': 'I', 'і': 'i', 'Ї': 'I', 'ї': 'i', 'Х': 'KH', 'х': 'kh', 'К': 'K', 'к': 'k', 'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r', 'Щ': 'SHCH', 'щ': 'shch', 'Ш': 'SH', 'ш': 'sh', 'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f', 'Ч': 'CH', 'ч': 'ch', 'Ц': 'TS', 'ц': 'ts', 'Ю': 'IU', 'ю': 'iu', 'Я': 'IA', 'я': 'ia', 'Й': 'I', 'й': 'i', 'Ь': '', 'ь': '', '’': ''}]
        def tr2(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps2[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr2 = tr2

    def transform(self, text):
        text = unicodedata.normalize('NFC', text)
        text = self._rx1.sub(self._tr1, text)
        text = self._rx2.sub(self._tr2, text)
        text = unicodedata.normalize('NFC', text)
        return text


class _Uklatn_uk_Latn_DSTU_9112_A_uk:
    def __init__(self):
        self._rx1 = re.compile(r"([ÁáÉéÍíÓóÚúÝýḮḯ])")
        _maps1 = [{'Á': 'Á', 'á': 'á', 'É': 'É', 'é': 'é', 'Í': 'Í', 'í': 'í', 'Ó': 'Ó', 'ó': 'ó', 'Ú': 'Ú', 'ú': 'ú', 'Ý': 'Ý', 'ý': 'ý', 'Ḯ': 'Ḯ', 'ḯ': 'ḯ'}]
        def tr1(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps1[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr1 = tr1
        self._rx2 = re.compile(r"(A|a|B|b|V|v|Ğ|ğ|G|g|D|d|E|e|J[Ee]|j[Ee]|Ž|ž|Z|z|Y|y|I|i|Ï|ï|K|k|L|l|M|m|N|n|O|o|P|p|R|r|S|s|T|t|U|u|F|f|X|x|C|c|Č|č|Š|š|Ŝ|ŝ|J[Uu]|j[Uu]|J[Aa]|j[Aa]|Ĵ|ĵ|Ö|ö|Ŭ|ŭ|Ǒ|ǒ|Ȳ|ȳ|Ē|ē)|(?<=[BbCcDdFfGgKkLlMmNnPpRrSsTtVvXxZzČčĞğŜŝŠšŽž])([Jj]\u0027(?=[AaEeUu])|[Jj])|(\u0027[Jj](?![AaEeIiUu])|\u0027(?=[Jj])|[Jj])")
        _maps2 = [{'A': 'А', 'a': 'а', 'B': 'Б', 'b': 'б', 'V': 'В', 'v': 'в', 'Ğ': 'Г', 'ğ': 'г', 'G': 'Ґ', 'g': 'ґ', 'D': 'Д', 'd': 'д', 'E': 'Е', 'e': 'е', 'JE': 'Є', 'Je': 'Є', 'jE': 'є', 'je': 'є', 'Ž': 'Ж', 'ž': 'ж', 'Z': 'З', 'z': 'з', 'Y': 'И', 'y': 'и', 'I': 'І', 'i': 'і', 'Ï': 'Ї', 'ï': 'ї', 'K': 'К', 'k': 'к', 'L': 'Л', 'l': 'л', 'M': 'М', 'm': 'м', 'N': 'Н', 'n': 'н', 'O': 'О', 'o': 'о', 'P': 'П', 'p': 'п', 'R': 'Р', 'r': 'р', 'S': 'С', 's': 'с', 'T': 'Т', 't': 'т', 'U': 'У', 'u': 'у', 'F': 'Ф', 'f': 'ф', 'X': 'Х', 'x': 'х', 'C': 'Ц', 'c': 'ц', 'Č': 'Ч', 'č': 'ч', 'Š': 'Ш', 'š': 'ш', 'Ŝ': 'Щ', 'ŝ': 'щ', 'JU': 'Ю', 'Ju': 'Ю', 'jU': 'ю', 'ju': 'ю', 'JA': 'Я', 'Ja': 'Я', 'jA': 'я', 'ja': 'я', 'Ĵ': 'Ь', 'ĵ': 'ь', 'Ö': 'Ё', 'ö': 'ё', 'Ŭ': 'Ў', 'ŭ': 'ў', 'Ǒ': 'Ъ', 'ǒ': 'ъ', 'Ȳ': 'Ы', 'ȳ': 'ы', 'Ē': 'Э', 'ē': 'э'}, {'J': 'Ь', 'j': 'ь', "J'": 'Ь', "j'": 'ь'}, {"'J": 'Й', "'j": 'й', "'": '’', 'J': 'Й', 'j': 'й'}]
        def tr2(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps2[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr2 = tr2

    def transform(self, text):
        text = unicodedata.normalize('NFC', text)
        text = self._rx1.sub(self._tr1, text)
        text = self._rx2.sub(self._tr2, text)
        text = unicodedata.normalize('NFC', text)
        return text


class _Uklatn_uk_Latn_DSTU_9112_B_uk:
    def __init__(self):
        self._rx1 = re.compile(r"([ÁáÉéÍíÓóÚúÝý])")
        _maps1 = [{'Á': 'Á', 'á': 'á', 'É': 'É', 'é': 'é', 'Í': 'Í', 'í': 'í', 'Ó': 'Ó', 'ó': 'ó', 'Ú': 'Ú', 'ú': 'ú', 'Ý': 'Ý', 'ý': 'ý'}]
        def tr1(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps1[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr1 = tr1
        self._rx2 = re.compile(r"([Jj][Oo][Ww]|[Ss][Hh][Cc][Hh]|[CcGgKkSsZzUuOo][Hh]|[Yy][Ww]|[Ee][Hh][Ww]|[Jj][EeIiUuAa]|[Hh][Jj]|[A-GIK-PR-VYZa-gik-pr-vyz])|(?<=[Ss][Hh][Cc][Hh])([Jj]\u0027(?=[AaEeIiUu])|[Jj])|(?<=[CcGgKkSsZz][Hh])([Jj]\u0027(?=[AaEeIiUu])|[Jj])|(?<=[BCDFGKLMNPRSTVZbcdfgklmnprstvzv])([Jj]\u0027(?=[AaEeIiUu])|[Jj])|(\u0027[Jj](?![AaEeIiUu])|\u0027(?=[Jj])|[Jj])")
        _maps2 = [{'A': 'А', 'a': 'а', 'B': 'Б', 'b': 'б', 'V': 'В', 'v': 'в', 'GH': 'Г', 'Gh': 'Г', 'gH': 'г', 'gh': 'г', 'G': 'Ґ', 'g': 'ґ', 'D': 'Д', 'd': 'д', 'E': 'Е', 'e': 'е', 'JE': 'Є', 'Je': 'Є', 'jE': 'є', 'je': 'є', 'ZH': 'Ж', 'Zh': 'Ж', 'zH': 'ж', 'zh': 'ж', 'Z': 'З', 'z': 'з', 'Y': 'И', 'y': 'и', 'I': 'І', 'i': 'і', 'JI': 'Ї', 'Ji': 'Ї', 'jI': 'ї', 'ji': 'ї', 'KH': 'Х', 'Kh': 'Х', 'kH': 'х', 'kh': 'х', 'K': 'К', 'k': 'к', 'L': 'Л', 'l': 'л', 'M': 'М', 'm': 'м', 'N': 'Н', 'n': 'н', 'O': 'О', 'o': 'о', 'P': 'П', 'p': 'п', 'R': 'Р', 'r': 'р', 'SHCH': 'Щ', 'SHCh': 'Щ', 'SHcH': 'Щ', 'SHch': 'Щ', 'ShCH': 'Щ', 'ShCh': 'Щ', 'ShcH': 'Щ', 'Shch': 'Щ', 'sHCH': 'щ', 'sHCh': 'щ', 'sHcH': 'щ', 'sHch': 'щ', 'shCH': 'щ', 'shCh': 'щ', 'shcH': 'щ', 'shch': 'щ', 'SH': 'Ш', 'Sh': 'Ш', 'sH': 'ш', 'sh': 'ш', 'S': 'С', 's': 'с', 'T': 'Т', 't': 'т', 'U': 'У', 'u': 'у', 'F': 'Ф', 'f': 'ф', 'CH': 'Ч', 'Ch': 'Ч', 'cH': 'ч', 'ch': 'ч', 'C': 'Ц', 'c': 'ц', 'JU': 'Ю', 'Ju': 'Ю', 'jU': 'ю', 'ju': 'ю', 'JA': 'Я', 'Ja': 'Я', 'jA': 'я', 'ja': 'я', 'HJ': 'Ь', 'Hj': 'Ь', 'hJ': 'ь', 'hj': 'ь', 'JOW': 'Ё', 'JOw': 'Ё', 'JoW': 'Ё', 'Jow': 'Ё', 'jOW': 'ё', 'jOw': 'ё', 'joW': 'ё', 'jow': 'ё', 'UH': 'Ў', 'Uh': 'Ў', 'uH': 'ў', 'uh': 'ў', 'OH': 'Ъ', 'Oh': 'Ъ', 'oH': 'ъ', 'oh': 'ъ', 'YW': 'Ы', 'Yw': 'Ы', 'yW': 'ы', 'yw': 'ы', 'EHW': 'Э', 'EHw': 'Э', 'EhW': 'Э', 'Ehw': 'Э', 'eHW': 'э', 'eHw': 'э', 'ehW': 'э', 'ehw': 'э'}, {'J': 'Ь', 'j': 'ь', "J'": 'Ь', "j'": 'ь'}, {'J': 'Ь', 'j': 'ь', "J'": 'Ь', "j'": 'ь'}, {'J': 'Ь', 'j': 'ь', "J'": 'Ь', "j'": 'ь'}, {"'J": 'Й', "'j": 'й', "'": '’', 'J': 'Й', 'j': 'й'}]
        def tr2(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps2[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr2 = tr2

    def transform(self, text):
        text = unicodedata.normalize('NFC', text)
        text = self._rx1.sub(self._tr1, text)
        text = self._rx2.sub(self._tr2, text)
        text = unicodedata.normalize('NFC', text)
        return text


_UklatnTables = [
    [None, None],
    [_Uklatn_uk_uk_Latn_DSTU_9112_A(), _Uklatn_uk_Latn_DSTU_9112_A_uk()],
    [_Uklatn_uk_uk_Latn_DSTU_9112_B(), _Uklatn_uk_Latn_DSTU_9112_B_uk()],
    [_Uklatn_uk_uk_Latn_KMU_55(), None],
]


def encode(text, table=None):
    """
    Transliterates a string of Ukrainian Cyrillic to Latin script.

    Signature:
      encode(str, int)

    Args:
      text (str): The Ukrainian Cyrillic string to transliterate.
      table (int): The transliteration table, one of:
       - uklatn.DSTU_9112_A: DSTU 9112:2021 System A
       - uklatn.DSTU_9112_B: DSTU 9112:2021 System B
       - uklatn.KMU_55: KMU 55:2010

    Returns:
      The transliterated string.
    """

    if table is None:
        table = DSTU_9112_A
    enc, _ = _UklatnTables[table]
    if not enc:
        raise ValueError(f'invalid table {table!r}')
    return enc.transform(text)


def decode(text, table=None):
    """
    Re-transliterates a string of Ukrainian Latin to Cyrillic script.

    Signature:
      decode(str, int)

    Args:
      text (str): The Ukrainian Latin string to transliterate.
      table (int): The transliteration table, one of:
       - uklatn.DSTU_9112_A: DSTU 9112:2021 System A
       - uklatn.DSTU_9112_B: DSTU 9112:2021 System B

    Returns:
      The re-transliterated string.
    """

    if table is None:
        table = DSTU_9112_A
    _, dec = _UklatnTables[table]
    if not dec:
        raise ValueError(f'invalid table {table!r}')
    return dec.transform(text)


def main(args):
    text = ' '.join(args.text)
    table = args.table
    if table is None:
        table = 'DSTU_9112_A'
    names = {'DSTU_9112_A': 1, 'DSTU_9112_B': 2, 'KMU_55': 3}
    table = names[table]
    tr = encode
    if args.cyrillic and not args.latin:
        tr = decode
    res = tr(text, table)
    print(res)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='+', help='text to transliterate')
    parser.add_argument('-t', '--table', choices=['DSTU_9112_A', 'DSTU_9112_B', 'KMU_55'], help='transliteration system (default: DSTU_9112_A)')
    parser.add_argument('-l', '--latin', action='store_true', help='convert to Latin script (default)')
    parser.add_argument('-c', '--cyrillic', action='store_true', help='convert to Cyrillic script')

    args = parser.parse_args()
    main(args)
