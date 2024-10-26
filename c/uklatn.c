#include <stdlib.h>
#include <uklatn.h>
#include <unicode/ustring.h>
#include <unicode/utrans.h>

/* For the rule syntax refer to
  https://www.unicode.org/reports/tr35/tr35-general.html#Transform_Rules_Syntax
  icu4c/source/i18n/unicode/translit.h
*/
static char _tr_rules[] =
    ":: [АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЬабвгґдеєжзиіїйклмнопрстуфхцчшщюяь’ЁЎЪЫЭёўъыэ] ;"
    ":: NFC (NFC) ;"
    "$quote = \\u0027 ;"
    // "$quote = '' ;"
    "$cyrcons = [БВГҐДЖЗЙКЛМНПРСТФХЦЧШЩЬбвгґджзйклмнпрстфхцчшщ] ;"
    "$cyrncons = [^БВГҐДЖЗЙКЛМНПРСТФХЦЧШЩЬбвгґджзйклмнпрстфхцчшщь] ;"
    "$cyrvows = [АЕЄИІЇОУЮЯаеєиіїоуюя] ;"
    "$cyrlow = [бвгґджзйклмнпрстфхцчшщьаеєиіїоуюя’] ;"
    "$latcons = [BCČDFGĞKLMNPRSŜŠTVXZŽbcčdfgğklmnprsŝštvxzž] ;"
    "$latvows = [AEIÏOUYaeiïouy] ;"
    "$wordBoundary = [^[:L:][:M:][:N:]] ;"

    "| $1 Ь < {($latcons) J $quote} [AEUaeu] ;"
    "| $1 ь < {($latcons) j $quote} [AEUaeu] ;"
    "| $1 Ь < {($latcons) J} [^AaEeUu] ;"
    "| $1 ь < {($latcons) j} [^AaEeUu] ;"
    "$wordBoundary {Ь > Ĵ ;"
    "$wordBoundary {ь > ĵ ;"
    "($cyrncons) Ь > | $1 Ĵ ;"
    "($cyrncons) ь > | $1 ĵ ;"
    "Ь} [АЕУаеу] > J $quote ;"
    "ь} [АЕУаеу] > j $quote ;"
    "($cyrcons) } [Йй] > | $1 $quote ;"
    "{є} $cyrlow > je ;"
    "Є <> JE ; є <> je ;"
    "{Ю} $cyrlow > Ju ;"
    "Ю <> JU ; ю <> ju ;"
    "{Я} $cyrlow > Ja ;"
    "Я <> JA ; я <> ja ;"
    "А <> A ; а <> a ;"
    "Б <> B ; б <> b ;"
    "В <> V ; в <> v ;"
    "Г <> Ğ ; г <> ğ ;"
    "Ґ <> G ; ґ <> g ;"
    "Д <> D ; д <> d ;"
    "Е <> E ; е <> e ;"
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
    "Й < $quote J} [^AEUIaeui] ;"
    "й < $quote j} [^AEUIaeui];"
    "Й <> J ; й <> j ;"
    "Ь > J ; ь > j ;"
    "Ь < Ĵ ; ь < ĵ ;"
    "’ > $quote ;"
    "’ < $quote} [jJ] ;"
    "Ё <> Ö ; ё <> ö ;"
    "Ў <> Ŭ ; ў <> ŭ ;"
    "Ъ <> Ǒ ; ъ <> ǒ ;"
    "Ы <> Ȳ ; ы <> ȳ ;"
    "Э <> Ē ; э <> ē ;"
    ":: ([BCČDFGĞKLMNPRSŜŠTVXZŽbcčdfgğklmnprsŝštvxzžAEIÏOUYaeiïouyJjĴĵ'ÖŬǑȲĒöŭǒȳē]) ;"
    ;


static const UChar Tid_DSTU_A[] = u"uk-uk_DSTUA";
static const UChar Rid_DSTU_A[] = u"uk_DSTUA-uk";


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
uklatn_init(void) {
    UErrorCode err = U_ZERO_ERROR;
    UChar rules[2000];
    int rulessize = sizeof(rules) / sizeof(rules[0]);

    u_strFromUTF8(rules, rulessize, NULL, _tr_rules, -1, &err);
    if (U_FAILURE(err)) {
        trace("u_strFromUTF8: %s\n", u_errorName(err));
        return err;
    }

    UTransliterator* tr;
    UParseError perr;
    tr = utrans_openU(Tid_DSTU_A, -1, UTRANS_FORWARD, rules, -1, &perr, &err);
    if (U_FAILURE(err)) {
        trace("utrans_openU: %s\n", u_errorName(err));
        return err;
    }

    dump_rules(tr);

    utrans_register(tr, &err);
    if (U_FAILURE(err)) {
        trace("utrans_register: %s\n", u_errorName(err));
        utrans_close(tr);
        return err;
    }

    tr = utrans_openU(Rid_DSTU_A, -1, UTRANS_REVERSE, rules, -1, &perr, &err);
    if (U_FAILURE(err)) {
        trace("utrans_openU: %s\n", u_errorName(err));
        return err;
    }

    dump_rules(tr);

    utrans_register(tr, &err);
    if (U_FAILURE(err)) {
        trace("utrans_register: %s\n", u_errorName(err));
        utrans_close(tr);
        return err;
    }

    return 0;
}


static int
uklatn_gettr(const UChar* tid, UTransDirection dir, UTransliterator** ptr) {
    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr;
    tr = utrans_openU(tid, -1, dir, NULL, 0, NULL, &err);
    #if 0
    /* id hierarchy is a mess
      https://unicode-org.atlassian.net/browse/ICU-21324
    */
    if (U_SUCCESS(err)) {
        const UChar* name = utrans_getUnicodeID(tr, NULL);
        int eq = u_strcmp(name, tid);
        if (eq != 0) {
            trace("asked for transliterator ");
            utrace(tid);
            trace("got transliterator ");
            utrace(name);
            err = U_INVALID_ID;
        }
    }
    #endif
    if (U_FAILURE(err)) {
        if (err == U_INVALID_ID) {
            err = uklatn_init();
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


int
uklatn_encodeu(const UChar* src, UChar* dest, int destsize) {
    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr = NULL;
    err = uklatn_gettr(Tid_DSTU_A, UTRANS_FORWARD, &tr);
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
uklatn_decodeu(const UChar* src, UChar* dest, int destsize) {
    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr = NULL;
    err = uklatn_gettr(Tid_DSTU_A, UTRANS_REVERSE, &tr);
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
uklatn_encode(const char* src, char* dest, int destsize) {
    UErrorCode err = U_ZERO_ERROR;
    int32_t bufsize = 0;
    u_strFromUTF8WithSub(NULL, 0, &bufsize, src, -1, 0xFFFD, NULL, &err);
    if (U_FAILURE(err) && err != U_BUFFER_OVERFLOW_ERROR) {
        trace("u_strFromUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }
    err = U_ZERO_ERROR;
    UChar* usrc = calloc(bufsize, sizeof(UChar));
    u_strFromUTF8WithSub(usrc, bufsize, NULL, src, -1, 0xFFFD, NULL, &err);
    if (U_FAILURE(err)) {
        free(usrc);
        trace("u_strFromUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }

    bufsize *= 3;
    UChar* udst = calloc(bufsize, sizeof(UChar));

    err = uklatn_encodeu(usrc, udst, bufsize);
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
uklatn_decode(const char* src, char* dest, int destsize) {
    UErrorCode err = U_ZERO_ERROR;
    int32_t bufsize = 0;
    u_strFromUTF8WithSub(NULL, 0, &bufsize, src, -1, 0xFFFD, NULL, &err);
    if (U_FAILURE(err) && err != U_BUFFER_OVERFLOW_ERROR) {
        trace("u_strFromUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }
    err = U_ZERO_ERROR;
    UChar* usrc = calloc(bufsize, sizeof(UChar));
    u_strFromUTF8WithSub(usrc, bufsize, NULL, src, -1, 0xFFFD, NULL, &err);
    if (U_FAILURE(err)) {
        free(usrc);
        trace("u_strFromUTF8WithSub: %s\n", u_errorName(err));
        return err;
    }

    bufsize *= 3;
    UChar* udst = calloc(bufsize, sizeof(UChar));

    err = uklatn_decodeu(usrc, udst, bufsize);
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

