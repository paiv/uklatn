Paiv.UkrainianLatin
==

Ukrainian Cyrillic transliteration to Latin script.

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


Usage
--

```elixir
import Paiv.UkrainianLatin
encode("Доброго вечора!")
#=> "Dobroğo večora!"

decode("Paljanycja")
#=> "Паляниця"
```

Select a transliteration scheme:
```elixir
encode("Борщ", :DSTU_9112_B)
#=> "Borshch"
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

