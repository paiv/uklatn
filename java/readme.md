uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


Usage
--

```java
import io.github.paiv.uklatn.UkrainianLatin;

UkrainianLatin tr = new UkrainianLatin();

tr.encode("Доброго вечора!");
tr.decode("Paljanycja");
```

Set the transliteration scheme:
```java
import static io.github.paiv.uklatn.UkrainianLatin.UKLatnTable;

tr.encode("Борщ", UKLatnTable.DSTU_9112_B);
tr.encode("Шевченко", UKLatnTable.KMU_55);
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
