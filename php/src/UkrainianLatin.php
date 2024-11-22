<?php declare(strict_types=1);

/* Note: generated code, do not edit. */

namespace Paiv;

use Normalizer;


/**
* Ukrainian Cyrillic transliteration to and from Latin script.
*/
final class UkrainianLatin {
    private $tables;

    /** DSTU 9112:2021 System A */
    const DSTU_9112_A = 'DSTU_9112_A';

    /** DSTU 9112:2021 System B */
    const DSTU_9112_B = 'DSTU_9112_B';

    /** KMU 55:2010, not reversible */
    const KMU_55 = 'KMU_55';

    /**
    * Transliterates a string of Ukrainian Cyrillic to Latin script.
    *
    * @param string $text the text to transliterate
    * @param string $table the transliteration system
    * @return string the transliterated text
    */
    public function encode(string $text, string $table = self::DSTU_9112_A): string {
        $codec = $this->tables[$table];
        if ($codec) {
            $tr = $codec[0];
            if ($tr) {
                return $tr->transform($text);
            }
        }
        throw new Exception("invalid table $table");
    }

    /**
    * Re-transliterates a string of Ukrainian Latin to Cyrillic script.
    *
    * @param string $text the text to transliterate
    * @param string $table the transliteration system
    * @return string the transliterated text
    */
    public function decode(string $text, string $table = self::DSTU_9112_A) {
        $codec = $this->tables[$table];
        if ($codec) {
            $tr = $codec[1];
            if ($tr) {
                return $tr->transform($text);
            }
        }
        throw new Exception("invalid table $table");
    }

    public function __construct() {
        $this->tables = array(
            'DSTU_9112_A' => [new _Uklatn_uk_uk_Latn_DSTU_9112_A(), new _Uklatn_uk_Latn_DSTU_9112_A_uk()],
            'DSTU_9112_B' => [new _Uklatn_uk_uk_Latn_DSTU_9112_B(), new _Uklatn_uk_Latn_DSTU_9112_B_uk()],
            'KMU_55' => [new _Uklatn_uk_uk_Latn_KMU_55(), null],
        );
    }
}


final class _Uklatn_uk_uk_Latn_DSTU_9112_A {
    private $rx1;
    private $tr1;
    private $maps1;

    public function __construct() {
        $this->rx1 = '#\b([Ьь])|([Ьь](?=[АаЕеУу])|[ЄЮЯ](?=\x{0301}?[а-щьюяєіїґ’])|(?<=[Б-ДЖЗК-НП-ТФ-Щб-джзк-нп-тф-щҐґ])[Йй])|([ЁЄІЇЎА-яёєіїўҐґ’])#u';
        $this->maps1 = [
            array(
                "Ь"=>"Ĵ","ь"=>"ĵ"
            ),
            array(
                "Ь"=>"J'","ь"=>"j'","Є"=>"Je","Ю"=>"Ju","Я"=>"Ja","Й"=>"'J","й"=>"'j"
            ),
            array(
                "А"=>"A","а"=>"a","Б"=>"B","б"=>"b","В"=>"V","в"=>"v","Г"=>"Ğ","г"=>"ğ","Ґ"=>"G","ґ"=>"g","Д"=>"D","д"=>"d","Е"=>"E","е"=>"e","Є"=>"JE","є"=>"je","Ж"=>"Ž","ж"=>"ž","З"=>"Z","з"=>"z","И"=>"Y","и"=>"y","І"=>"I","і"=>"i","Ї"=>"Ï","ї"=>"ï","К"=>"K","к"=>"k","Л"=>"L","л"=>"l","М"=>"M","м"=>"m","Н"=>"N","н"=>"n","О"=>"O","о"=>"o","П"=>"P","п"=>"p","Р"=>"R","р"=>"r","С"=>"S","с"=>"s","Т"=>"T","т"=>"t","У"=>"U","у"=>"u","Ф"=>"F","ф"=>"f","Х"=>"X","х"=>"x","Ц"=>"C","ц"=>"c","Ч"=>"Č","ч"=>"č","Ш"=>"Š","ш"=>"š","Щ"=>"Ŝ","щ"=>"ŝ","Ю"=>"JU","ю"=>"ju","Я"=>"JA","я"=>"ja","Ь"=>"J","ь"=>"j","Й"=>"J","й"=>"j","’"=>"'","Ё"=>"Ö","ё"=>"ö","Ў"=>"Ŭ","ў"=>"ŭ","Ъ"=>"Ǒ","ъ"=>"ǒ","Ы"=>"Ȳ","ы"=>"ȳ","Э"=>"Ē","э"=>"ē"
            )
        ];
        $this->tr1 = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps1[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
    }

    public function transform(string $text): string {
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        $text = preg_replace_callback($this->rx1, $this->tr1, $text);
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        return $text;
    }
}


final class _Uklatn_uk_uk_Latn_DSTU_9112_B {
    private $rx1;
    private $tr1;
    private $maps1;

    public function __construct() {
        $this->rx1 = '#([Ьь](?=[АаЕеІіУу])|(?<=[Б-ДЖЗК-НП-ТФ-Щб-джзк-нп-тф-щҐґ])[Йй])|([ГЄЖЇХЩШЧЮЯЁЎЪЫЭ](?=\x{0301}?[а-яёєіїўґ’])|\b[Ьь])|([ЁЄІЇЎА-яёєіїўҐґ’])#u';
        $this->maps1 = [
            array(
                "Ь"=>"J'","ь"=>"j'","Й"=>"'J","й"=>"'j"
            ),
            array(
                "Г"=>"Gh","Є"=>"Je","Ж"=>"Zh","Ї"=>"Ji","Х"=>"Kh","Щ"=>"Shch","Ш"=>"Sh","Ч"=>"Ch","Ю"=>"Ju","Я"=>"Ja","Ё"=>"Jow","Ў"=>"Uh","Ъ"=>"Oh","Ы"=>"Yw","Э"=>"Ehw","Ь"=>"Hj","ь"=>"hj"
            ),
            array(
                "А"=>"A","а"=>"a","Б"=>"B","б"=>"b","В"=>"V","в"=>"v","Г"=>"GH","г"=>"gh","Ґ"=>"G","ґ"=>"g","Д"=>"D","д"=>"d","Е"=>"E","е"=>"e","Є"=>"JE","є"=>"je","Ж"=>"ZH","ж"=>"zh","З"=>"Z","з"=>"z","И"=>"Y","и"=>"y","І"=>"I","і"=>"i","Ї"=>"JI","ї"=>"ji","Х"=>"KH","х"=>"kh","К"=>"K","к"=>"k","Л"=>"L","л"=>"l","М"=>"M","м"=>"m","Н"=>"N","н"=>"n","О"=>"O","о"=>"o","П"=>"P","п"=>"p","Р"=>"R","р"=>"r","Щ"=>"SHCH","щ"=>"shch","Ш"=>"SH","ш"=>"sh","С"=>"S","с"=>"s","Т"=>"T","т"=>"t","У"=>"U","у"=>"u","Ф"=>"F","ф"=>"f","Ч"=>"CH","ч"=>"ch","Ц"=>"C","ц"=>"c","Ю"=>"JU","ю"=>"ju","Я"=>"JA","я"=>"ja","Й"=>"J","й"=>"j","Ь"=>"J","ь"=>"j","’"=>"'","Ё"=>"JOW","ё"=>"jow","Ў"=>"UH","ў"=>"uh","Ъ"=>"OH","ъ"=>"oh","Ы"=>"YW","ы"=>"yw","Э"=>"EHW","э"=>"ehw"
            )
        ];
        $this->tr1 = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps1[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
    }

    public function transform(string $text): string {
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        $text = preg_replace_callback($this->rx1, $this->tr1, $text);
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        return $text;
    }
}


final class _Uklatn_uk_uk_Latn_KMU_55 {
    private $rx1;
    private $tr1;
    private $maps1;
    private $rx2;
    private $tr2;
    private $maps2;

    public function __construct() {
        $this->rx1 = '#(?<=[ЁЄІЇЎА-яёєіїўҐґ])([’\x{0027}])(?=[ЁЄІЇЎА-яёєіїўҐґ])#u';
        $this->maps1 = [
            array(
                "’"=>"","'"=>""
            )
        ];
        $this->tr1 = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps1[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
        $this->rx2 = '#\b([ЄЇЮЯ])(?=\x{0301}?[а-яёєіїўґ’])|\b([ЙйЄЇЮЯєїюя])|([Зз]Г|[ЖХЦЩШЧЄЇЮЯ])(?=\x{0301}?[а-яёєіїўґ’])|([Зз][Гг]|[ЄІЇА-ЩЬЮ-щьюяєіїҐґ’])#u';
        $this->maps2 = [
            array(
                "Є"=>"Ye","Ї"=>"Yi","Ю"=>"Yu","Я"=>"Ya"
            ),
            array(
                "Й"=>"Y","й"=>"y","Є"=>"YE","є"=>"ye","Ї"=>"YI","ї"=>"yi","Ю"=>"YU","ю"=>"yu","Я"=>"YA","я"=>"ya"
            ),
            array(
                "ЗГ"=>"ZGh","зГ"=>"zGh","Ж"=>"Zh","Х"=>"Kh","Ц"=>"Ts","Щ"=>"Shch","Ш"=>"Sh","Ч"=>"Ch","Є"=>"Ie","Ї"=>"I","Ю"=>"Iu","Я"=>"Ia"
            ),
            array(
                "ЗГ"=>"ZGH","Зг"=>"Zgh","зГ"=>"zGH","зг"=>"zgh","А"=>"A","а"=>"a","Б"=>"B","б"=>"b","В"=>"V","в"=>"v","Г"=>"H","г"=>"h","Ґ"=>"G","ґ"=>"g","Д"=>"D","д"=>"d","Е"=>"E","е"=>"e","Є"=>"IE","є"=>"ie","Ж"=>"ZH","ж"=>"zh","З"=>"Z","з"=>"z","И"=>"Y","и"=>"y","І"=>"I","і"=>"i","Ї"=>"I","ї"=>"i","Х"=>"KH","х"=>"kh","К"=>"K","к"=>"k","Л"=>"L","л"=>"l","М"=>"M","м"=>"m","Н"=>"N","н"=>"n","О"=>"O","о"=>"o","П"=>"P","п"=>"p","Р"=>"R","р"=>"r","Щ"=>"SHCH","щ"=>"shch","Ш"=>"SH","ш"=>"sh","С"=>"S","с"=>"s","Т"=>"T","т"=>"t","У"=>"U","у"=>"u","Ф"=>"F","ф"=>"f","Ч"=>"CH","ч"=>"ch","Ц"=>"TS","ц"=>"ts","Ю"=>"IU","ю"=>"iu","Я"=>"IA","я"=>"ia","Й"=>"I","й"=>"i","Ь"=>"","ь"=>"","’"=>""
            )
        ];
        $this->tr2 = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps2[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
    }

    public function transform(string $text): string {
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        $text = preg_replace_callback($this->rx1, $this->tr1, $text);
        $text = preg_replace_callback($this->rx2, $this->tr2, $text);
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        return $text;
    }
}


final class _Uklatn_uk_Latn_DSTU_9112_A_uk {
    private $rx1;
    private $tr1;
    private $maps1;
    private $rx2;
    private $tr2;
    private $maps2;

    public function __construct() {
        $this->rx1 = '#([ÁáÉéÍíÓóÚúÝýḮḯ])#u';
        $this->maps1 = [
            array(
                "Á"=>"Á","á"=>"á","É"=>"É","é"=>"é","Í"=>"Í","í"=>"í","Ó"=>"Ó","ó"=>"ó","Ú"=>"Ú","ú"=>"ú","Ý"=>"Ý","ý"=>"ý","Ḯ"=>"Ḯ","ḯ"=>"ḯ"
            )
        ];
        $this->tr1 = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps1[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
        $this->rx2 = '#(J[Ee]|j[Ee]|J[Uu]|j[Uu]|J[Aa]|j[Aa]|[A-GIK-PR-VXYZa-gik-pr-vxyzÏÖïöČčĒēĞğĴĵŜŝŠšŬŭŽžǑǒȲȳ])|(?<=[BbCcDdFfGgKkLlMmNnPpRrSsTtVvXxZzČčĞğŜŝŠšŽž])([Jj]\x{0027}(?=[AaEeUu])|[Jj])|(\x{0027}[Jj](?![AaEeIiUu])|\x{0027}(?=[Jj])|[Jj])#u';
        $this->maps2 = [
            array(
                "A"=>"А","a"=>"а","B"=>"Б","b"=>"б","V"=>"В","v"=>"в","Ğ"=>"Г","ğ"=>"г","G"=>"Ґ","g"=>"ґ","D"=>"Д","d"=>"д","E"=>"Е","e"=>"е","JE"=>"Є","Je"=>"Є","jE"=>"є","je"=>"є","Ž"=>"Ж","ž"=>"ж","Z"=>"З","z"=>"з","Y"=>"И","y"=>"и","I"=>"І","i"=>"і","Ï"=>"Ї","ï"=>"ї","K"=>"К","k"=>"к","L"=>"Л","l"=>"л","M"=>"М","m"=>"м","N"=>"Н","n"=>"н","O"=>"О","o"=>"о","P"=>"П","p"=>"п","R"=>"Р","r"=>"р","S"=>"С","s"=>"с","T"=>"Т","t"=>"т","U"=>"У","u"=>"у","F"=>"Ф","f"=>"ф","X"=>"Х","x"=>"х","C"=>"Ц","c"=>"ц","Č"=>"Ч","č"=>"ч","Š"=>"Ш","š"=>"ш","Ŝ"=>"Щ","ŝ"=>"щ","JU"=>"Ю","Ju"=>"Ю","jU"=>"ю","ju"=>"ю","JA"=>"Я","Ja"=>"Я","jA"=>"я","ja"=>"я","Ĵ"=>"Ь","ĵ"=>"ь","Ö"=>"Ё","ö"=>"ё","Ŭ"=>"Ў","ŭ"=>"ў","Ǒ"=>"Ъ","ǒ"=>"ъ","Ȳ"=>"Ы","ȳ"=>"ы","Ē"=>"Э","ē"=>"э"
            ),
            array(
                "J"=>"Ь","j"=>"ь","J'"=>"Ь","j'"=>"ь"
            ),
            array(
                "'J"=>"Й","'j"=>"й","'"=>"’","J"=>"Й","j"=>"й"
            )
        ];
        $this->tr2 = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps2[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
    }

    public function transform(string $text): string {
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        $text = preg_replace_callback($this->rx1, $this->tr1, $text);
        $text = preg_replace_callback($this->rx2, $this->tr2, $text);
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        return $text;
    }
}


final class _Uklatn_uk_Latn_DSTU_9112_B_uk {
    private $rx1;
    private $tr1;
    private $maps1;
    private $rx2;
    private $tr2;
    private $maps2;

    public function __construct() {
        $this->rx1 = '#([ÁáÉéÍíÓóÚúÝý])#u';
        $this->maps1 = [
            array(
                "Á"=>"Á","á"=>"á","É"=>"É","é"=>"é","Í"=>"Í","í"=>"í","Ó"=>"Ó","ó"=>"ó","Ú"=>"Ú","ú"=>"ú","Ý"=>"Ý","ý"=>"ý"
            )
        ];
        $this->tr1 = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps1[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
        $this->rx2 = '#([Jj][Oo][Ww]|[Ss][Hh][Cc][Hh]|[CcGgKkSsZzUuOo][Hh]|[Yy][Ww]|[Ee][Hh][Ww]|[Jj][EeIiUuAa]|[Hh][Jj]|[A-GIK-PR-VYZa-gik-pr-vyz])|(?<=[Ss][Hh][Cc][Hh])([Jj]\x{0027}(?=[AaEeIiUu])|[Jj])|(?<=[CcGgKkSsZz][Hh])([Jj]\x{0027}(?=[AaEeIiUu])|[Jj])|(?<=[BCDFGKLMNPRSTVZbcdfgklmnprstvzv])([Jj]\x{0027}(?=[AaEeIiUu])|[Jj])|(\x{0027}[Jj](?![AaEeIiUu])|\x{0027}(?=[Jj])|[Jj])#u';
        $this->maps2 = [
            array(
                "A"=>"А","a"=>"а","B"=>"Б","b"=>"б","V"=>"В","v"=>"в","GH"=>"Г","Gh"=>"Г","gH"=>"г","gh"=>"г","G"=>"Ґ","g"=>"ґ","D"=>"Д","d"=>"д","E"=>"Е","e"=>"е","JE"=>"Є","Je"=>"Є","jE"=>"є","je"=>"є","ZH"=>"Ж","Zh"=>"Ж","zH"=>"ж","zh"=>"ж","Z"=>"З","z"=>"з","Y"=>"И","y"=>"и","I"=>"І","i"=>"і","JI"=>"Ї","Ji"=>"Ї","jI"=>"ї","ji"=>"ї","KH"=>"Х","Kh"=>"Х","kH"=>"х","kh"=>"х","K"=>"К","k"=>"к","L"=>"Л","l"=>"л","M"=>"М","m"=>"м","N"=>"Н","n"=>"н","O"=>"О","o"=>"о","P"=>"П","p"=>"п","R"=>"Р","r"=>"р","SHCH"=>"Щ","SHCh"=>"Щ","SHcH"=>"Щ","SHch"=>"Щ","ShCH"=>"Щ","ShCh"=>"Щ","ShcH"=>"Щ","Shch"=>"Щ","sHCH"=>"щ","sHCh"=>"щ","sHcH"=>"щ","sHch"=>"щ","shCH"=>"щ","shCh"=>"щ","shcH"=>"щ","shch"=>"щ","SH"=>"Ш","Sh"=>"Ш","sH"=>"ш","sh"=>"ш","S"=>"С","s"=>"с","T"=>"Т","t"=>"т","U"=>"У","u"=>"у","F"=>"Ф","f"=>"ф","CH"=>"Ч","Ch"=>"Ч","cH"=>"ч","ch"=>"ч","C"=>"Ц","c"=>"ц","JU"=>"Ю","Ju"=>"Ю","jU"=>"ю","ju"=>"ю","JA"=>"Я","Ja"=>"Я","jA"=>"я","ja"=>"я","HJ"=>"Ь","Hj"=>"Ь","hJ"=>"ь","hj"=>"ь","JOW"=>"Ё","JOw"=>"Ё","JoW"=>"Ё","Jow"=>"Ё","jOW"=>"ё","jOw"=>"ё","joW"=>"ё","jow"=>"ё","UH"=>"Ў","Uh"=>"Ў","uH"=>"ў","uh"=>"ў","OH"=>"Ъ","Oh"=>"Ъ","oH"=>"ъ","oh"=>"ъ","YW"=>"Ы","Yw"=>"Ы","yW"=>"ы","yw"=>"ы","EHW"=>"Э","EHw"=>"Э","EhW"=>"Э","Ehw"=>"Э","eHW"=>"э","eHw"=>"э","ehW"=>"э","ehw"=>"э"
            ),
            array(
                "J"=>"Ь","j"=>"ь","J'"=>"Ь","j'"=>"ь"
            ),
            array(
                "J"=>"Ь","j"=>"ь","J'"=>"Ь","j'"=>"ь"
            ),
            array(
                "J"=>"Ь","j"=>"ь","J'"=>"Ь","j'"=>"ь"
            ),
            array(
                "'J"=>"Й","'j"=>"й","'"=>"’","J"=>"Й","j"=>"й"
            )
        ];
        $this->tr2 = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps2[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
    }

    public function transform(string $text): string {
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        $text = preg_replace_callback($this->rx1, $this->tr1, $text);
        $text = preg_replace_callback($this->rx2, $this->tr2, $text);
        $text = Normalizer::normalize($text, Normalizer::FORM_C);
        return $text;
    }
}
