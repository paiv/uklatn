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
        /* DSTU System A */
        {
            u"Україна, Хмельницький",
            u"Ukraïna, Xmeljnycjkyj",
            UklatnTable_DSTU_A,
        },
        {
            u"Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
            u"Ŝastjam b'ješ žuk ïx ğlycju v fon j gedzj prič.",
            UklatnTable_DSTU_A,
        },
        {
            u"ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
            u"ĵ Ĵ lj ljje ljï ljju ljja lj'e lji lj'u lj'a ljjo ljo",
            UklatnTable_DSTU_A,
        },
        {
            u"Єл Їл Юл Ял",
            u"Jel Ïl Jul Jal",
            UklatnTable_DSTU_A,
        },
        {
            u"бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
            u"bj vj ğj gj dj žj zj kj lj mj nj pj rj sj tj fj xj cj čj šj ŝj",
            UklatnTable_DSTU_A,
        },
        {
            u"бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
            u"bja vja ğja gja dja žja zja kja lja mja nja pja rja sja tja fja xja cja čja šja ŝja",
            UklatnTable_DSTU_A,
        },
        {
            u"б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
            u"b'ja v'ja ğ'ja g'ja d'ja ž'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja x'ja c'ja č'ja š'ja ŝ'ja",
            UklatnTable_DSTU_A,
        },
        {
            u"бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
            u"b'j b'jo v'j ğ'j g'j d'j ž'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j x'j c'j č'j š'j ŝ'j",
            UklatnTable_DSTU_A,
        },
        {
            u"рос дыня эзёдынъ. бр кроў.",
            u"ros dȳnja ēzödȳnǒ. br kroŭ.",
            UklatnTable_DSTU_A,
        },
        {
            u"на́голос надві́рний лля́ю",
            u"náğolos nadvírnyj lljáju",
            UklatnTable_DSTU_A,
        },
        {
            u"Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.",
            u"Sonce svitytj majže bilym svitlom, odnak čerez syljniše rozsijuvannja i poğlynannja korotkoxvyljovoï častyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverxni našoï planety nabuvaje pevnoğo žovtoğo vidtinku. Jakŝo nebo jasne, to blakytnyj vidtinok rozsijanoğo svitla skladajetjsja z žovtuvatym prjamym sonjačnym svitlom i zağaljne osvitlennja ob'jektiv na Zemli staje bilym.",
            UklatnTable_DSTU_A,
        },

        /* DSTU System B */
        {
            u"Україна, Хмельницький",
            u"Ukrajina, Khmeljnycjkyj",
            UklatnTable_DSTU_B,
        },
        {
            u"Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
            u"Shchastjam b'jesh zhuk jikh ghlycju v fon j gedzj prich.",
            UklatnTable_DSTU_B,
        },
        {
            u"ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
            u"hj Hj lj ljje ljji ljju ljja lj'e lj'i lj'u lj'a ljjo ljo",
            UklatnTable_DSTU_B,
        },
        {
            u"Єл Їл Юл Ял",
            u"Jel Jil Jul Jal",
            UklatnTable_DSTU_B,
        },
        {
            u"бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
            u"bj vj ghj gj dj zhj zj kj lj mj nj pj rj sj tj fj khj cj chj shj shchj",
            UklatnTable_DSTU_B,
        },
        {
            u"бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
            u"bja vja ghja gja dja zhja zja kja lja mja nja pja rja sja tja fja khja cja chja shja shchja",
            UklatnTable_DSTU_B,
        },
        {
            u"б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
            u"b'ja v'ja gh'ja g'ja d'ja zh'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja kh'ja c'ja ch'ja sh'ja shch'ja",
            UklatnTable_DSTU_B,
        },
        {
            u"бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
            u"b'j b'jo v'j gh'j g'j d'j zh'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j kh'j c'j ch'j sh'j shch'j",
            UklatnTable_DSTU_B,
        },
        {
            u"рос дыня эзёдынъ. бр кроў.",
            u"ros dywnja ehwzjowdywnoh. br krouh.",
            UklatnTable_DSTU_B,
        },
        {
            u"на́голос надві́рний лля́ю",
            u"nágholos nadvírnyj lljáju",
            UklatnTable_DSTU_B,
        },
        {
            u"Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.",
            u"Sonce svitytj majzhe bilym svitlom, odnak cherez syljnishe rozsijuvannja i poghlynannja korotkokhvyljovoji chastyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverkhni nashoji planety nabuvaje pevnogho zhovtogho vidtinku. Jakshcho nebo jasne, to blakytnyj vidtinok rozsijanogho svitla skladajetjsja z zhovtuvatym prjamym sonjachnym svitlom i zaghaljne osvitlennja ob'jektiv na Zemli staje bilym.",
            UklatnTable_DSTU_B,
        },
    };

    size_t n = sizeof(data)/sizeof(data[0]);
    for (size_t i = 0; i < n; ++i) {
        int err = _test_uk2latn(data[i].cyr, data[i].lat, data[i].table);
        if (err != 0) { return err; }

        err = _test_latn2uk(data[i].lat, data[i].cyr, data[i].table);
        if (err != 0) { return err; }
    }

    return 0;
}
