#ifndef _UKLATN_H_
#define _UKLATN_H_


#ifndef UChar
#include <stdint.h>
#define UChar uint16_t
#endif


enum UklatnTable {
    UklatnTable_default = 0,
    UklatnTable_DSTU_9112_A = 1,
    UklatnTable_DSTU_9112_B = 2,
    UklatnTable_KMU_55 = 3,
};


#ifndef UKLATN_DEFAULT_TABLE
#define UKLATN_DEFAULT_TABLE UklatnTable_DSTU_9112_A
#endif


#if defined(__cplusplus)
extern "C" {
#endif


/* Cyrillic to Latin transiteration
  UTF-8 parameters.
*/
int uklatn_encode(const char* restrict src, int table, char* restrict dest, int destsize);


/* Cyrillic to Latin transiteration
  UTF-16 parameters.
*/
int uklatn_encodeu(const UChar* restrict src, int table, UChar* restrict dest, int destsize);


/* Latin to Cyrillic re-transliteration
  UTF-8 parameters.
*/
int uklatn_decode(const char* restrict src, int table, char* restrict dest, int destsize);


/* Latin to Cyrillic re-transliteration
  UTF-16 parameters.
*/
int uklatn_decodeu(const UChar* restrict src, int table, UChar* restrict dest, int destsize);


#if defined(__cplusplus)
} /* extern "C" */
#endif

#endif /* _UKLATN_H_ */
