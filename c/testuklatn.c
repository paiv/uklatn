#include <uklatn.h>
#include <unicode/ustring.h>

#include <stdio.h>

#define trace(...) fprintf(stderr, __VA_ARGS__)

static void
utrace(const UChar* u) {
    char s[10000];
    UErrorCode err = U_ZERO_ERROR;
    u_strToUTF8(s, sizeof(s), NULL, u, -1, &err);
    if (U_FAILURE(err)) {
        trace("u_strToUTF8: %s\n", u_errorName(err));
        return;
    }
    trace("%s\n", s);
}


static int
_test_uk2latn(const UChar* input, const UChar* expect, int table) {
    const size_t bufsize = 2000;
    UChar lat[bufsize];
    int err = uklatn_encodeu(input, table, lat, 2000);
    if (err != 0) { return err; }
    int i = u_strcmp(lat, expect);
    if (i != 0) {
        trace("table: %d cyr-lat\n", table);
        trace(" input: ");
        utrace(input);
        trace("expect: ");
        utrace(expect);
        trace("actual: ");
        utrace(lat);
        return 1;
    }
    return 0;
}


static int
_test_latn2uk(const UChar* input, const UChar* expect, int table) {
    const size_t bufsize = 2000;
    UChar cyr[bufsize];
    int err = uklatn_decodeu(input, table, cyr, 2000);
    if (err != 0) { return err; }
    int i = u_strcmp(cyr, expect);
    if (i != 0) {
        trace("table: %d lat-cyr\n", table);
        trace(" input: ");
        utrace(input);
        trace("expect: ");
        utrace(expect);
        trace("actual: ");
        utrace(cyr);
        return 1;
    }
    return 0;
}


struct testcase_s {
    const UChar *cyr, *lat;
    int table;
};


int main(int argc, const char* argv[]) {

    const struct testcase_s data[] = {
        /* DSTU 9112:2021 System A */
        {
            u"Україна, Хмельницький",
            u"Ukraïna, Xmeljnycjkyj",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
            u"Ŝastjam b'ješ žuk ïx ğlycju v fon j gedzj prič.",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
            u"ĵ Ĵ lj ljje ljï ljju ljja lj'e lji lj'u lj'a ljjo ljo",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"Єл Їл Юл Ял",
            u"Jel Ïl Jul Jal",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
            u"bj vj ğj gj dj žj zj kj lj mj nj pj rj sj tj fj xj cj čj šj ŝj",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
            u"bja vja ğja gja dja žja zja kja lja mja nja pja rja sja tja fja xja cja čja šja ŝja",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
            u"b'ja v'ja ğ'ja g'ja d'ja ž'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja x'ja c'ja č'ja š'ja ŝ'ja",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
            u"b'j b'jo v'j ğ'j g'j d'j ž'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j x'j c'j č'j š'j ŝ'j",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"рос дыня эзёдынъ. бр кроў.",
            u"ros dȳnja ēzödȳnǒ. br kroŭ.",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́",
            u"Á á É é JÉ jé Ý ý Í í Ḯ ḯ Ó ó Ú ú JÚ jú JÁ já",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            u"Jés sJés jés sjés Ḯs sḮs ḯs sḯs Jús sJús jús sjús Jás sJás jás sjás",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"' ім’я 'жук' \"жук\" ' '",
            u"' im'ja 'žuk' \"žuk\" ' '",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.",
            u"Sonce svitytj majže bilym svitlom, odnak čerez syljniše rozsijuvannja i poğlynannja korotkoxvyljovoï častyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverxni našoï planety nabuvaje pevnoğo žovtoğo vidtinku. Jakŝo nebo jasne, to blakytnyj vidtinok rozsijanoğo svitla skladajetjsja z žovtuvatym prjamym sonjačnym svitlom i zağaljne osvitlennja ob'jektiv na Zemli staje bilym.",
            UklatnTable_DSTU_9112_A,
        },

        /* DSTU 9112:2021 System B */
        {
            u"Україна, Хмельницький",
            u"Ukrajina, Khmeljnycjkyj",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
            u"Shchastjam b'jesh zhuk jikh ghlycju v fon j gedzj prich.",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
            u"hj Hj lj ljje ljji ljju ljja lj'e lj'i lj'u lj'a ljjo ljo",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"Єл Їл Юл Ял",
            u"Jel Jil Jul Jal",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
            u"bj vj ghj gj dj zhj zj kj lj mj nj pj rj sj tj fj khj cj chj shj shchj",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
            u"bja vja ghja gja dja zhja zja kja lja mja nja pja rja sja tja fja khja cja chja shja shchja",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
            u"b'ja v'ja gh'ja g'ja d'ja zh'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja kh'ja c'ja ch'ja sh'ja shch'ja",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
            u"b'j b'jo v'j gh'j g'j d'j zh'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j kh'j c'j ch'j sh'j shch'j",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"рос дыня эзёдынъ. бр кроў.",
            u"ros dywnja ehwzjowdywnoh. br krouh.",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́",
            u"Á á É é JÉ jé Ý ý Í í JÍ jí Ó ó Ú ú JÚ jú JÁ já",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            u"Jés sJés jés sjés Jís sJís jís sjís Jús sJús jús sjús Jás sJás jás sjás",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"' ім’я 'жук' \"жук\" ' '",
            u"' im'ja 'zhuk' \"zhuk\" ' '",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.",
            u"Sonce svitytj majzhe bilym svitlom, odnak cherez syljnishe rozsijuvannja i poghlynannja korotkokhvyljovoji chastyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverkhni nashoji planety nabuvaje pevnogho zhovtogho vidtinku. Jakshcho nebo jasne, to blakytnyj vidtinok rozsijanogho svitla skladajetjsja z zhovtuvatym prjamym sonjachnym svitlom i zaghaljne osvitlennja ob'jektiv na Zemli staje bilym.",
            UklatnTable_DSTU_9112_B,
        },

        /* KMU 55:2010 */
        {
            u"Україна, Хмельницький",
            u"Ukraina, Khmelnytskyi",
            UklatnTable_KMU_55,
        },
        {
            u"Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
            u"Shchastiam biesh zhuk yikh hlytsiu v fon y gedz prich.",
            UklatnTable_KMU_55,
        },
        {
            u"згин зГ зГин Згин Зг ЗГ ЗГИН",
            u"zghyn zGH zGhyn Zghyn Zgh ZGH ZGHYN",
            UklatnTable_KMU_55,
        },
        {
            u"ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
            u"  l lie li liu lia le li lu la lio lo",
            UklatnTable_KMU_55,
        },
        {
            u"Єл Їл Юл Ял",
            u"Yel Yil Yul Yal",
            UklatnTable_KMU_55,
        },
        {
            u"бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
            u"b v h g d zh z k l m n p r s t f kh ts ch sh shch",
            UklatnTable_KMU_55,
        },
        {
            u"бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
            u"bia via hia gia dia zhia zia kia lia mia nia pia ria sia tia fia khia tsia chia shia shchia",
            UklatnTable_KMU_55,
        },
        {
            u"б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
            u"bia via hia gia dia zhia zia kia lia mia nia pia ria sia tia fia khia tsia chia shia shchia",
            UklatnTable_KMU_55,
        },
        {
            u"бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
            u"bi bio vi hi gi di zhi zi ki li mi ni pi ri si ti fi khi tsi chi shi shchi",
            UklatnTable_KMU_55,
        },
        {
            u"А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́",
            u"Á á É é YÉ yé Ý ý Í í YÍ yí Ó ó Ú ú YÚ yú YÁ yá",
            UklatnTable_KMU_55,
        },
        {
            u"Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            u"Yés sIés yés siés Yís sÍs yís sís Yús sIús yús siús Yás sIás yás siás",
            UklatnTable_KMU_55,
        },
        {
            u"' ім’я 'жук' \"жук\" ' '",
            u"' imia 'zhuk' \"zhuk\" ' '",
            UklatnTable_KMU_55,
        },
        {
            u"Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.",
            u"Sontse svityt maizhe bilym svitlom, odnak cherez sylnishe rozsiiuvannia i pohlynannia korotkokhvylovoi chastyny spektra atmosferoiu Zemli priame svitlo Sontsia bilia poverkhni nashoi planety nabuvaie pevnoho zhovtoho vidtinku. Yakshcho nebo yasne, to blakytnyi vidtinok rozsiianoho svitla skladaietsia z zhovtuvatym priamym soniachnym svitlom i zahalne osvitlennia obiektiv na Zemli staie bilym.",
            UklatnTable_KMU_55,
        },
    };

    size_t n = sizeof(data)/sizeof(data[0]);
    for (size_t i = 0; i < n; ++i) {
        int err = _test_uk2latn(data[i].cyr, data[i].lat, data[i].table);
        if (err != 0) { return err; }

        err = _test_latn2uk(data[i].lat, data[i].cyr, data[i].table);
        if (data[i].table == UklatnTable_KMU_55) {
            if (err != -1) {
                trace("expect: err -1\n");
                trace("actual: err %d\n", err);
                return err;
            }
        }
        else {
            if (err != 0) { return err; }
        }
    }

    /* cyr to lat one way only */
    const struct testcase_s data1[] = {
        {
            u"в’я в'я",
            u"v'ja v'ja",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"в’я в'я",
            u"v'ja v'ja",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"в’я в'я",
            u"via via",
            UklatnTable_KMU_55,
        },
        {
            u"І\u0308 і\u0308 И\u0306 и\u0306 Е\u0308 е\u0308 У\u0306 у\u0306",
            u"Ï ï J j Ö ö Ŭ ŭ",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"І\u0308 і\u0308 И\u0306 и\u0306 Е\u0308 е\u0308 У\u0306 у\u0306",
            u"JI ji J j JOW jow UH uh",
            UklatnTable_DSTU_9112_B,
        },
    };

    n = sizeof(data1)/sizeof(data1[0]);
    for (size_t i = 0; i < n; ++i) {
        int err = _test_uk2latn(data1[i].cyr, data1[i].lat, data1[i].table);
        if (err != 0) { return err; }
    }

    /* lat to cyr one way only */
    const struct testcase_s data2[] = {
        {
            u"jA jE jU",
            u"я є ю",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"jA jI jE jU gH zH kH sHcH sH cH hJ",
            u"я ї є ю г ж х щ ш ч ь",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"I\u0308 i\u0308 J\u0302 j\u0302 C\u030C c\u030C G\u0306 g\u0306 S\u0302 s\u0302 S\u030C s\u030C Z\u030C z\u030C",
            u"Ї ї Ь ь Ч ч Г г Щ щ Ш ш Ж ж",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"O\u0308 o\u0308 U\u0306 u\u0306 O\u030C o\u030C Y\u0304 y\u0304 E\u0304 e\u0304",
            u"Ё ё Ў ў Ъ ъ Ы ы Э э",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"A\u0301 a\u0301 E\u0301 e\u0301 JE\u0301 Je\u0301 jE\u0301 je\u0301 Y\u0301 y\u0301 I\u0301 i\u0301 Ï\u0301 ï\u0301 O\u0301 o\u0301 U\u0301 u\u0301 JU\u0301 Ju\u0301 jU\u0301 ju\u0301 JA\u0301 Ja\u0301 jA\u0301 ja\u0301",
            u"А́ а́ Е́ е́ Є́ Є́ є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ Ю́ ю́ ю́ Я́ Я́ я́ я́",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"Je\u0301s sJe\u0301s je\u0301s sje\u0301s Ï\u0301s sÏ\u0301s ï\u0301s sï\u0301s Ju\u0301s sJu\u0301s ju\u0301s sju\u0301s Ja\u0301s sJa\u0301s ja\u0301s sja\u0301s",
            u"Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            UklatnTable_DSTU_9112_A,
        },
        {
            u"A\u0301 a\u0301 E\u0301 e\u0301 JE\u0301 Je\u0301 jE\u0301 je\u0301 Y\u0301 y\u0301 I\u0301 i\u0301 JI\u0301 Ji\u0301 jI\u0301 ji\u0301 O\u0301 o\u0301 U\u0301 u\u0301 JU\u0301 Ju\u0301 jU\u0301 ju\u0301 JA\u0301 Ja\u0301 jA\u0301 ja\u0301",
            u"А́ а́ Е́ е́ Є́ Є́ є́ є́ И́ и́ І́ і́ Ї́ Ї́ ї́ ї́ О́ о́ У́ у́ Ю́ Ю́ ю́ ю́ Я́ Я́ я́ я́",
            UklatnTable_DSTU_9112_B,
        },
        {
            u"Je\u0301s sJe\u0301s je\u0301s sje\u0301s Ji\u0301s sJi\u0301s ji\u0301s sji\u0301s Ju\u0301s sJu\u0301s ju\u0301s sju\u0301s Ja\u0301s sJa\u0301s ja\u0301s sja\u0301s",
            u"Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            UklatnTable_DSTU_9112_B,
        },
    };

    n = sizeof(data2)/sizeof(data2[0]);
    for (size_t i = 0; i < n; ++i) {
        int err = _test_latn2uk(data2[i].cyr, data2[i].lat, data2[i].table);
        if (err != 0) { return err; }
    }

    return 0;
}
