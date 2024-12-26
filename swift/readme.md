uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


```swift
import UkrainianLatin

encode("Доброго вечора!")
decode("Paljanycja")
```

Set the transliteration scheme:
```swift
encode("Борщ", table: UKLatnTable.DSTU_9112_B)
encode("Шевченко", table: UKLatnTable.KMU_55)
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.


Command-line executable
--

```sh
uklatn 'моє щастя'
```

Running executable from a package:
```sh
swift run uklatn 'моє щастя'
```

```txt
usage: uklatn [-h] [-t TABLE] [-c] [-l] [-f FILE] [text ...]

arguments:
  text            text to transliterate

options:
  -h, --help            show this help message and exit
  -t, --table {DSTU_9112_A,DSTU_9112_B,KMU_55}
                        transliteration system (default: DSTU_9112_A)
  -l, --lat, --latin    convert to Latin script (default)
  -c, --cyr, --cyrillic convert to Cyrillic script
  -f, --file FILE       read text from file
```
