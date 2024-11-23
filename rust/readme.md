uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


Usage
--

```rust
use { uklatn::Table, uklatn::decode, uklatn::encode };

encode("Доброго вечора!", Table::default());
decode("Paljanycja", Table::default());
```

Select a transliteration scheme:

```rust
encode("Борщ", Table::Dstu9112B);
encode("Шевченко", Table::Kmu55);
```

Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

