uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


Usage:
```csharp
using paiv.uklatn;

UkrainianLatin tr = new UkrainianLatin();
string s = tr.Encode("Доброго вечора!");
string t = tr.Decode("Paljanycja");
```

Select a transliteration scheme:
```csharp
s = tr.Encode("Борщ", UkrainianLatin.Table.DSTU_9112_A);
```

Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
