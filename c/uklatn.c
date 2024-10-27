#include <stdlib.h>
#include <uklatn.h>
#include <unicode/ustring.h>
#include <unicode/utrans.h>

/* For the rule syntax refer to
  https://www.unicode.org/reports/tr35/tr35-general.html#Transform_Rules_Syntax
  icu4c/source/i18n/unicode/translit.h
*/

static const UChar Tid_DSTU_A[] = u"uk-uk_DSTUA";
static const UChar Rid_DSTU_A[] = u"uk_DSTUA-uk";
static const UChar Tid_DSTU_B[] = u"uk-uk_DSTUB";
static const UChar Rid_DSTU_B[] = u"uk_DSTUB-uk";
static const UChar Tid_KMU[] = u"uk-uk_KMU";


static char _rules_dstu_a[] =
    ":: [АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЬабвгґдеєжзиіїйклмнопрстуфхцчшщюяь’ЁЎЪЫЭёўъыэ] ;"
    ":: NFC (NFC) ;"
    "$quote = \\u0027 ;"
    "$cyrcons = [БВГҐДЖЗКЛМНПРСТФХЦЧШЩбвгґджзклмнпрстфхцчшщ] ;"
    "$cyrlow = [бвгґджзйклмнпрстфхцчшщьаеєиіїоуюя’] ;"
    "$wordBoundary = [^[:L:][:M:][:N:]] ;"

    "($cyrcons) } [Йй] > | $1 $quote ;"
    "А <> A ; а <> a ;"
    "Б <> B ; б <> b ;"
    "В <> V ; в <> v ;"
    "Г <> Ğ ; г <> ğ ;"
    "Ґ <> G ; ґ <> g ;"
    "Д <> D ; д <> d ;"
    "Е <> E ; е <> e ;"
    "Є} $cyrlow > Je ;"
    "Є <> JE ; є <> je ; Є < Je ;"
    "Ж <> Ž ; ж <> ž ;"
    "З <> Z ; з <> z ;"
    "И <> Y ; и <> y ;"
    "І <> I ; і <> i ;"
    "Ї <> Ï ; ї <> ï ;"
    "К <> K ; к <> k ;"
    "Л <> L ; л <> l ;"
    "М <> M ; м <> m ;"
    "Н <> N ; н <> n ;"
    "О <> O ; о <> o ;"
    "П <> P ; п <> p ;"
    "Р <> R ; р <> r ;"
    "С <> S ; с <> s ;"
    "Т <> T ; т <> t ;"
    "У <> U ; у <> u ;"
    "Ф <> F ; ф <> f ;"
    "Х <> X ; х <> x ;"
    "Ц <> C ; ц <> c ;"
    "Ч <> Č ; ч <> č ;"
    "Ш <> Š ; ш <> š ;"
    "Щ <> Ŝ ; щ <> ŝ ;"
    "Ю} $cyrlow > Ju ;"
    "Ю <> JU ; ю <> ju ; Ю < Ju ;"
    "Я} $cyrlow > Ja ;"
    "Я <> JA ; я <> ja ; Я < Ja ;"
    "$wordBoundary {Ь > Ĵ ;"
    "$wordBoundary {ь > ĵ ;"
    "Ь < Ĵ ; ь < ĵ ;"
    "Ь} [АаЕеУу] > J $quote ;"
    "ь} [АаЕеУу] > j $quote ;"
    "Ь > J ; ь > j ;"
    "Ь < $cyrcons {J ;"
    "ь < $cyrcons {j ;"
    " < $cyrcons [Ьь] {$quote} [AaEeUu] ;"
    "Й < $quote J} [^AaEeIiUu] ;"
    "й < $quote j} [^AaEeIiUu] ;"
    "Й <> J ; й <> j ;"
    "’ > $quote ;"
    "’ < $quote} [Jj] ;"
    "Ё <> Ö ; ё <> ö ;"
    "Ў <> Ŭ ; ў <> ŭ ;"
    "Ъ <> Ǒ ; ъ <> ǒ ;"
    "Ы <> Ȳ ; ы <> ȳ ;"
    "Э <> Ē ; э <> ē ;"
    ":: ([BCČDFGĞKLMNPRSŜŠTVXZŽbcčdfgğklmnprsŝštvxzžAEIÏOUYaeiïouyJjĴĵ'ÖŬǑȲĒöŭǒȳē]) ;"
    ;


static char _rules_dstu_b[] =
    ":: [АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЬабвгґдеєжзиіїйклмнопрстуфхцчшщюяь’ЁЎЪЫЭёўъыэ] ;"
    ":: NFC (NFC) ;"
    "$quote = \\u0027 ;"
    "$cyrcons = [БВГҐДЖЗКЛМНПРСТФХЦЧШЩбвгґджзклмнпрстфхцчшщ] ;"
    "$cyrlow = [бвгґджзйклмнпрстфхцчшщьаеєиіїоуюя’] ;"
    "$wordBoundary = [^[:L:][:M:][:N:]] ;"

    "($cyrcons) } [Йй] > | $1 $quote ;"
    "Ё < J [Oo] [Ww] ; ё < j [Oo] [Ww] ;"
    "Ў < U [Hh] ; ў < u [Hh] ;"
    "Ъ < O [Hh] ; ъ < o [Hh] ;"
    "Ы < Y [Ww] ; ы < y [Ww] ;"
    "Э < E [Hh] [Ww] ; э < e [Hh] [Ww] ;"
    "А <> A ; а <> a ;"
    "Б <> B ; б <> b ;"
    "В <> V ; в <> v ;"
    "Г} $cyrlow > Gh ;"
    "Г <> GH ; г <> gh ; Г < Gh ;"
    "Ґ <> G ; ґ <> g ;"
    "Д <> D ; д <> d ;"
    "Е <> E ; е <> e ;"
    "Є} $cyrlow > Je ;"
    "Є <> JE ; є <> je ; Є < Je ;"
    "Ж} $cyrlow > Zh ;"
    "Ж <> ZH ; ж <> zh ; Ж < Zh ;"
    "З <> Z ; з <> z ;"
    "И <> Y ; и <> y ;"
    "І <> I ; і <> i ;"
    "Ї} $cyrlow > Ji ;"
    "Ї <> JI ; ї <> ji ; Ї < Ji ;"
    "Х} $cyrlow > Kh ;"
    "Х <> KH ; х <> kh ; Х < Kh ;"
    "К <> K ; к <> k ;"
    "Л <> L ; л <> l ;"
    "М <> M ; м <> m ;"
    "Н <> N ; н <> n ;"
    "О <> O ; о <> o ;"
    "П <> P ; п <> p ;"
    "Р <> R ; р <> r ;"
    "Щ} $cyrlow > Shch ; "
    "Щ > SHCH ; щ > shch ;"
    "Щ < S [Hh] [Cc] [Hh] ;"
    "щ < s [Hh] [Cc] [Hh] ;"
    "Ш} $cyrlow > Sh ;"
    "Ш <> SH ; ш <> sh ; Ш < Sh ;"
    "С <> S ; с <> s ;"
    "Т <> T ; т <> t ;"
    "У <> U ; у <> u ;"
    "Ф <> F ; ф <> f ;"
    "Ч} $cyrlow > Ch ;"
    "Ч <> CH ; ч <> ch ; Ч < Ch ;"
    "Ц <> C ; ц <> c ;"
    "Ю} $cyrlow > Ju ;"
    "Ю <> JU ; ю <> ju ; Ю < Ju ;"
    "Я} $cyrlow > Ja ;"
    "Я <> JA ; я <> ja ; Я < Ja ;"
    "Й > J ; й > j ;"
    "$wordBoundary {Ь > Hj ;"
    "$wordBoundary {ь > hj ;"
    "Ь < H[Jj] ; ь < hj ;"
    "Ь} [АаЕеІіУу] > J $quote ;"
    "ь} [АаЕеІіУу] > j $quote ;"
    "Ь > J ; ь > j ;"
    "Ь < $cyrcons {J ;"
    "ь < $cyrcons {j ;"
    " < $cyrcons [Ьь] {$quote} [AaEeIiUu] ;"
    "Й < $quote J} [^AaEeIiUu] ;"
    "й < $quote j} [^AaEeIiUu] ;"
    "Й < J ; й < j ;"
    "’ > $quote ;"
    "’ < $quote} [Jj] ;"
    "Ё} $cyrlow > Jow ;"
    "Ё > JOW ; ё > jow ;"
    "Ў} $cyrlow > Uh ;"
    "Ў > UH ; ў > uh ;"
    "Ъ} $cyrlow > Oh ;"
    "Ъ > OH ; ъ > oh ;"
    "Ы} $cyrlow > Yw ;"
    "Ы > YW ; ы > yw ;"
    "Э} $cyrlow > Ehw ;"
    "Э > EHW ; э > ehw ;"
    ":: ([BCDFGHKLMNPRSTVWXZbcdfghklmnprstvwxzAEIOUYaeiouyJj']) ;"
    ;


static char _rules_kmu[] =
    ":: [АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЬабвгґдеєжзиіїйклмнопрстуфхцчшщюяь’] ;"
    ":: NFC ;"
    "$quote = \\u0027 ;"
    "$cyrlow = [бвгґджзйклмнпрстфхцчшщьаеєиіїоуюя’] ;"
    "$wordBoundary = [^[:L:][:M:][:N:]] ;"

    "А > A ; а > a ;"
    "Б > B ; б > b ;"
    "В > V ; в > v ;"
    "Г > H ; г > h ;"
    "Ґ > G ; ґ > g ;"
    "Д > D ; д > d ;"
    "Е > E ; е > e ;"
    "$wordBoundary {Є} $cyrlow > Ye ;"
    "$wordBoundary {Є > YE ;"
    "$wordBoundary {є > ye ;"
    "Є} $cyrlow > Ie ;"
    "Є > IE ; є > ie ;"
    "Ж} $cyrlow > Zh ;"
    "Ж > ZH ; ж > zh ;"
    "З > Z ; з > z ;"
    "И > Y ; и > y ;"
    "І > I ; і > i ;"
    "$wordBoundary {Ї} $cyrlow > Yi ;"
    "$wordBoundary {Ї > YI ;"
    "$wordBoundary {ї > yi ;"
    "Ї > I ; ї > i ;"
    "$wordBoundary {Й > Y ;"
    "$wordBoundary {й > y ;"
    "Й > I ; й > i ;"
    "К > K ; к > k ;"
    "Л > L ; л > l ;"
    "М > M ; м > m ;"
    "Н > N ; н > n ;"
    "О > O ; о > o ;"
    "П > P ; п > p ;"
    "Р > R ; р > r ;"
    "С > S ; с > s ;"
    "Т > T ; т > t ;"
    "У > U ; у > u ;"
    "Ф > F ; ф > f ;"
    "Х} $cyrlow > Kh ;"
    "Х > KH ; х > kh ;"
    "Ц} $cyrlow > Ts ;"
    "Ц > TS ; ц > ts ;"
    "Ч} $cyrlow > Ch ;"
    "Ч > CH ; ч > ch ;"
    "Ш} $cyrlow > Sh ;"
    "Ш > SH ; ш > sh ;"
    "Щ} $cyrlow > Shch ; "
    "Щ > SHCH ; щ > shch ;"
    "$wordBoundary {Ю} $cyrlow > Yu ;"
    "$wordBoundary {Ю > YU ;"
    "$wordBoundary {ю > yu ;"
    "Ю} $cyrlow > Iu ;"
    "Ю > IU ; ю > iu ;"
    "$wordBoundary {Я} $cyrlow > Ya ;"
    "$wordBoundary {Я > YA ;"
    "$wordBoundary {я > ya ;"
    "Я} $cyrlow > Ia ;"
    "Я > IA ; я > ia ;"
    "[Ьь] > ;"
    "’ > ;"
    ;


#if defined(DEBUG) && DEBUG

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

static void
dump_rules(UTransliterator* tr) {
    UChar text[8000];
    UErrorCode err = U_ZERO_ERROR;
    const UChar* sid = utrans_getUnicodeID(tr, NULL);
    trace("# ==== start "); utrace(sid);
    utrans_toRules(tr, 0, text, 8000, &err);
    utrace(text);
    trace("# ==== end "); utrace(sid);
}

#else

#define trace(...)
#define utrace(s)
#define dump_rules(tr)

#endif


static int
_uklatn_register_rules(const UChar* name, const UChar* rname, const char* text) {
    UErrorCode err = U_ZERO_ERROR;
    UChar rules[2000];
    int rulessize = sizeof(rules) / sizeof(rules[0]);

    u_strFromUTF8(rules, rulessize, NULL, text, -1, &err);
    if (U_FAILURE(err)) {
        trace("u_strFromUTF8: %s\n", u_errorName(err));
        return err;
    }

    UTransliterator* tr;
    UParseError perr;
    tr = utrans_openU(name, -1, UTRANS_FORWARD, rules, -1, &perr, &err);
    if (U_FAILURE(err)) {
        trace("utrans_openU: %s\n", u_errorName(err));
        return err;
    }

    // dump_rules(tr);

    utrans_register(tr, &err);
    if (U_FAILURE(err)) {
        trace("utrans_register: %s\n", u_errorName(err));
        utrans_close(tr);
        return err;
    }

    if (rname != NULL) {
        tr = utrans_openU(rname, -1, UTRANS_REVERSE, rules, -1, &perr, &err);
        if (U_FAILURE(err)) {
            trace("utrans_openU: %s\n", u_errorName(err));
            return err;
        }

        // dump_rules(tr);

        utrans_register(tr, &err);
        if (U_FAILURE(err)) {
            trace("utrans_register: %s\n", u_errorName(err));
            utrans_close(tr);
            return err;
        }
    }

    return 0;
}


static int
_uklatn_init(void) {
    UErrorCode err = U_ZERO_ERROR;

    err = _uklatn_register_rules(Tid_DSTU_A, Rid_DSTU_A, _rules_dstu_a);
    if (U_FAILURE(err)) { return err; }

    err = _uklatn_register_rules(Tid_DSTU_B, Rid_DSTU_B, _rules_dstu_b);
    if (U_FAILURE(err)) { return err; }

    err = _uklatn_register_rules(Tid_KMU, NULL, _rules_kmu);
    if (U_FAILURE(err)) { return err; }

    return 0;
}


static int
_uklatn_gettr(const UChar* tid, UTransDirection dir, UTransliterator** ptr) {
    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr;
    tr = utrans_openU(tid, -1, dir, NULL, 0, NULL, &err);
    #if 0
    /* id hierarchy is a mess
      https://unicode-org.atlassian.net/browse/ICU-21324
    */
    if (U_SUCCESS(err)) {
        const UChar* name = utrans_getUnicodeID(tr, NULL);
        trace("asked for transliterator (direction %d) ", dir);
        utrace(tid);
        trace("got transliterator ");
        utrace(name);
        err = U_INVALID_ID;
    }
    #endif
    if (U_FAILURE(err)) {
        if (err == U_INVALID_ID) {
            err = _uklatn_init();
            if (U_FAILURE(err)) { return err; }
            tr = utrans_openU(tid, -1, dir, NULL, 0, NULL, &err);
        }
        if (U_FAILURE(err)) {
            trace("utrans_openU: %s\n", u_errorName(err));
            return err;
        }
    }
    *ptr = tr;
    return 0;
}


static const UChar*
_uklatn_table_name(int table) {
    if (table == UklatnTable_default) {
        table = UKLATN_DEFAULT_TABLE;
    }
    switch (table) {
        case UklatnTable_default:
        case UklatnTable_DSTU_9112_A:
            return Tid_DSTU_A;
        case UklatnTable_DSTU_9112_B:
            return Tid_DSTU_B;
        case UklatnTable_KMU_55:
            return Tid_KMU;
        default:
            trace("invalid table %d", table);
            return NULL;
    }
}


int
uklatn_encodeu(const UChar* src, int table, UChar* dest, int destsize) {
    const UChar* name = _uklatn_table_name(table);
    if (name == NULL) { return -1; }

    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr = NULL;
    err = _uklatn_gettr(name, UTRANS_FORWARD, &tr);
    if (err != 0) { return err; }

    u_strncpy(dest, src, destsize);
    int32_t lim = u_strlen(dest);

    utrans_transUChars(tr, dest, NULL, destsize, 0, &lim, &err);
    if (U_FAILURE(err)) {
        trace("utrans_transUChars: %s\n", u_errorName(err));
        return err;
    }
    utrans_close(tr);
    return 0;
}


int
uklatn_decodeu(const UChar* src, int table, UChar* dest, int destsize) {
    if (table == UklatnTable_KMU_55) {
        return -1;
    }

    const UChar* name = _uklatn_table_name(table);
    if (name == NULL) { return -1; }

    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr = NULL;
    err = _uklatn_gettr(name, UTRANS_REVERSE, &tr);
    if (err != 0) { return err; }

    u_strncpy(dest, src, destsize);
    int32_t lim = u_strlen(dest);

    utrans_transUChars(tr, dest, NULL, destsize, 0, &lim, &err);
    if (U_FAILURE(err)) {
        trace("utrans_transUChars: %s\n", u_errorName(err));
        return err;
    }
    utrans_close(tr);
    return 0;
}


int
uklatn_encode(const char* src, int table, char* dest, int destsize) {
    UErrorCode err = U_ZERO_ERROR;
    int32_t bufsize = 0;
    u_strFromUTF8WithSub(NULL, 0, &bufsize, src, -1, 0xFFFD, NULL, &err);
    if (U_FAILURE(err) && err != U_BUFFER_OVERFLOW_ERROR) {
        trace("u_strFromUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }
    err = U_ZERO_ERROR;
    ++bufsize;
    UChar* usrc = calloc(bufsize, sizeof(UChar));
    u_strFromUTF8WithSub(usrc, bufsize, NULL, src, -1, 0xFFFD, NULL, &err);
    if (U_FAILURE(err)) {
        free(usrc);
        trace("u_strFromUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }

    bufsize *= 3;
    UChar* udst = calloc(bufsize, sizeof(UChar));

    err = uklatn_encodeu(usrc, table, udst, bufsize);
    free(usrc);
    if (U_FAILURE(err)) {
        free(udst);
        trace("uklatn_encodeu: %s\n", u_errorName(err));
        return err;
    }

    u_strToUTF8WithSub(dest, destsize, NULL, udst, -1, 0xFFFD, NULL, &err);
    free(udst);
    if (U_FAILURE(err)) {
        trace("u_strToUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }

    return 0;
}


int
uklatn_decode(const char* src, int table, char* dest, int destsize) {
    if (table == UklatnTable_KMU_55) {
        return -1;
    }

    UErrorCode err = U_ZERO_ERROR;
    int32_t bufsize = 0;
    u_strFromUTF8WithSub(NULL, 0, &bufsize, src, -1, 0xFFFD, NULL, &err);
    if (U_FAILURE(err) && err != U_BUFFER_OVERFLOW_ERROR) {
        trace("u_strFromUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }
    err = U_ZERO_ERROR;
    ++bufsize;
    UChar* usrc = calloc(bufsize, sizeof(UChar));
    u_strFromUTF8WithSub(usrc, bufsize, NULL, src, -1, 0xFFFD, NULL, &err);
    if (U_FAILURE(err)) {
        free(usrc);
        trace("u_strFromUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }

    bufsize *= 3;
    UChar* udst = calloc(bufsize, sizeof(UChar));

    err = uklatn_decodeu(usrc, table, udst, bufsize);
    free(usrc);
    if (U_FAILURE(err)) {
        free(udst);
        trace("uklatn_decodeu: %s\n", u_errorName(err));
        return err;
    }

    u_strToUTF8WithSub(dest, destsize, NULL, udst, -1, 0xFFFD, NULL, &err);
    free(udst);
    if (U_FAILURE(err)) {
        trace("u_strToUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }

    return 0;
}

