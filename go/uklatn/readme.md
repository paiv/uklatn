uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


```go
import "github.com/paiv/uklatn/go/uklatn"

uklatn.EncodeString("Доброго вечора!", uklatn.DefaultTable)
```

Set the transliteration scheme:
```go
uklatn.EncodeString("Борщ", uklatn.DSTU_9112_B)
uklatn.EncodeString("Шевченко", uklatn.KMU_55)
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
