uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


Usage:
```py
import uklatn
s = uklatn.encode("Доброго вечора!")
print(s)
t = uklatn.decode("Paljanycja")
print(t)
```

Select a transliteration scheme:
```py
s = uklatn.encode("Борщ", uklatn.DSTU_9112_A)
```

Module command line
--
```sh
python -m uklatn 'Бери вершину'
```

```txt
usage: uklatn [-h] [-f FILE] [-t {DSTU_9112_A,DSTU_9112_B,KMU_55}] [-l] [-c] [text ...]

positional arguments:
  text                  text to transliterate

options:
  -h, --help            show this help message and exit
  -f, --file FILE       read text from file
  -t, --table {DSTU_9112_A,DSTU_9112_B,KMU_55}
                        transliteration system (default: DSTU_9112_A)
  -l, --latin           convert to Latin script (default)
  -c, --cyrillic        convert to Cyrillic script
```
