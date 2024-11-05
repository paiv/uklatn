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


struct _uklatn_test {
    const UChar *cyr, *lat;
    int table;
};


#include "_tests.c"


static int
_run_c2l_tests(const struct _uklatn_test* data, size_t count) {
    for (size_t i = 0; i < count; ++i) {
        int err = _test_uk2latn(data[i].cyr, data[i].lat, data[i].table);
        if (err != 0) { return err; }
    }
    return 0;
}


static int
_run_l2c_tests(const struct _uklatn_test* data, size_t count) {
    for (size_t i = 0; i < count; ++i) {
        int err = _test_latn2uk(data[i].lat, data[i].cyr, data[i].table);
        if (err != 0) { return err; }
    }
    return 0;
}


int main(int argc, const char* argv[]) {
    int err = 0;

    size_t c2lr_n = sizeof(_cyr2lat2cyr_data) / sizeof(_cyr2lat2cyr_data[0]);
    err = _run_c2l_tests(_cyr2lat2cyr_data, c2lr_n);
    if (err != 0) { return err; }
    err = _run_l2c_tests(_cyr2lat2cyr_data, c2lr_n);
    if (err != 0) { return err; }

    size_t l2cr_n = sizeof(_lat2cyr2lat_data) / sizeof(_lat2cyr2lat_data[0]);
    err = _run_l2c_tests(_lat2cyr2lat_data, l2cr_n);
    if (err != 0) { return err; }
    err = _run_c2l_tests(_lat2cyr2lat_data, l2cr_n);
    if (err != 0) { return err; }

    size_t c2l_n = sizeof(_cyr2lat_data) / sizeof(_cyr2lat_data[0]);
    err = _run_c2l_tests(_cyr2lat_data, c2l_n);
    if (err != 0) { return err; }

    size_t l2c_n = sizeof(_lat2cyr_data) / sizeof(_lat2cyr_data[0]);
    err = _run_l2c_tests(_lat2cyr_data, l2c_n);
    if (err != 0) { return err; }

    err = _test_latn2uk(u"B", u"Б", UklatnTable_KMU_55);
    if (err != -1) {
        trace("expect: err -1\n");
        trace("actual: err %d\n", err);
        return err;
    }

    return 0;
}
