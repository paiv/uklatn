uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


The library provides UTF-8 and UTF-16 API. The underlying ICU operates on UTF-16 strings.


Build
--

```sh
mkdir build
cd build && cmake ..
```


Usage
--

The library provides UTF-8 and UTF-16 API. The underlying ICU operates on UTF-16 strings.

```c
#include <uklatn.h>

/* UTF-8 */
uklatn_encode("Доброго вечора!", UklaltnTable_default, dest, destsize);
uklatn_decode("Paljanycja", UklaltnTable_default, dest, destsize);

/* UTF-16 */
uklatn_encodeu(u"Доброго вечора!", UklaltnTable_default, dest, destsize);
uklatn_decodeu(u"Paljanycja", UklaltnTable_default, dest, destsize);
```

Set the transliteration scheme:
```c
uklatn_encode("Борщ", UklaltnTable_DSTU_9112_B, dest, destsize);
uklatn_encode("Шевченко", UklaltnTable_KMU_55, dest, destsize);
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
