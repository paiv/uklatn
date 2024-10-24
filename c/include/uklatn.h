#ifndef _UKLATN_H_
#define _UKLATN_H_


#ifndef UChar
#include <stdint.h>
#define UChar uint16_t
#endif


#if defined(__cplusplus) || defined(c_plusplus)
extern "C" {
#endif


/* Cyrillic to Latin transiteration */
int uklatn_encode(const UChar* restrict src, UChar* restrict dest, int destsize);


/* Latin to Cyrillic re-transliteration */
int uklatn_decode(const UChar* restrict src, UChar* restrict dest, int destsize);


#if defined(__cplusplus) || defined(c_plusplus)
} /* extern "C" */
#endif

#endif /* _UKLATN_H_ */
