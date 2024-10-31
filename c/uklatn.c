#include <stdlib.h>
#include <uklatn.h>
#include <unicode/ustring.h>
#include <unicode/utrans.h>


#if !defined(NDEBUG)

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


enum UklatnDirection {
    UklatnDirection_forward,
    UklatnDirection_reverse,
};


static int
_uklatn_register_table(const UChar* name, const char* text) {
    UErrorCode err = U_ZERO_ERROR;
    UChar rules[2400];
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

    return 0;
}


#include "_tables.c"


static int
_uklatn_gettr(const UChar* tid, UTransliterator** ptr) {
    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr;
    tr = utrans_openU(tid, -1, UTRANS_FORWARD, NULL, 0, NULL, &err);
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
            err = _uklatn_register_tables();
            if (U_FAILURE(err)) { return err; }
            tr = utrans_openU(tid, -1, UTRANS_FORWARD, NULL, 0, NULL, &err);
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
_uklatn_table_name(int table, int direction) {
    if (table == UklatnTable_default) {
        table = UKLATN_DEFAULT_TABLE;
    }
    switch (table) {
        case UklatnTable_default:
        case UklatnTable_DSTU_9112_A:
            return direction == UklatnDirection_reverse ?
                _TableName_DSTU_9112_A_uk :
                _TableName_uk_DSTU_9112_A ;
        case UklatnTable_DSTU_9112_B:
            return direction == UklatnDirection_reverse ?
                _TableName_DSTU_9112_B_uk :
                _TableName_uk_DSTU_9112_B ;
        case UklatnTable_KMU_55:
            if (direction == UklatnDirection_forward) {
                return _TableName_uk_KMU_55;
            }
            // pass through
        default:
            trace("invalid table %d (direction %d)", table, direction);
            return NULL;
    }
}


int
uklatn_encodeu(const UChar* src, int table, UChar* dest, int destsize) {
    const UChar* name = _uklatn_table_name(table, UklatnDirection_forward);
    if (name == NULL) { return -1; }

    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr = NULL;
    err = _uklatn_gettr(name, &tr);
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

    const UChar* name = _uklatn_table_name(table, UklatnDirection_reverse);
    if (name == NULL) { return -1; }

    UErrorCode err = U_ZERO_ERROR;
    UTransliterator* tr = NULL;
    err = _uklatn_gettr(name, &tr);
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

