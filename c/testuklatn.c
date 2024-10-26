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
_test_uk2latn(const UChar* input, const UChar* expect) {
    const size_t bufsize = 2000;
    UChar lat[bufsize];
    int err = uklatn_encodeu(input, lat, 2000);
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
_test_latn2uk(const UChar* input, const UChar* expect) {
    const size_t bufsize = 2000;
    UChar cyr[bufsize];
    int err = uklatn_decodeu(input, cyr, 2000);
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


int main(int argc, const char* argv[]) {

    const UChar* data[] = {
        u"Україна, Хмельницький",
        u"Ukraïna, Xmeljnycjkyj",

        u"Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
        u"Ŝastjam b'ješ žuk ïx ğlycju v fon j gedzj prič.",

        u"ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
        u"ĵ Ĵ lj ljje ljï ljju ljja lj'e lji lj'u lj'a ljjo ljo",

        u"бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
        u"bj vj ğj gj dj žj zj kj lj mj nj pj rj sj tj fj xj cj čj šj ŝj",

        u"бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
        u"bja vja ğja gja dja žja zja kja lja mja nja pja rja sja tja fja xja cja čja šja ŝja",

        u"б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
        u"b'ja v'ja ğ'ja g'ja d'ja ž'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja x'ja c'ja č'ja š'ja ŝ'ja",

        u"бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
        u"b'j b'jo v'j ğ'j g'j d'j ž'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j x'j c'j č'j š'j ŝ'j",

        u"рос дыня эзёдынъ. бр кроў.",
        u"ros dȳnja ēzödȳnǒ. br kroŭ.",

        u"на́голос надві́рний лля́ю",
        u"náğolos nadvírnyj lljáju",
    };

    size_t n = sizeof(data)/sizeof(data[0]);
    for (size_t i = 0; i < n; i += 2) {
        int err = _test_uk2latn(data[i], data[i+1]);
        if (err != 0) { return err; }

        err = _test_latn2uk(data[i+1], data[i]);
        if (err != 0) { return err; }
    }

    return 0;
}
