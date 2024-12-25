---
layout: post
title:  "Python package for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://pypi.org/project/uklatn/](https://pypi.org/project/uklatn/)


Install
--

Install with pip:
```sh
pip install uklatn
```


Usage:
```py
import uklatn

uklatn.encode("Доброго вечора!")
uklatn.decode("Paljanycja")
```

Set the transliteration scheme:
```py
uklatn.encode("Борщ", uklatn.DSTU_9112_B)
uklatn.encode("Шевченко", uklatn.KMU_55)
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.


Module command line
--
```sh
python -m uklatn 'моє щастя'
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
  -l, --latin, --lat    convert to Latin script (default)
  -c, --cyrillic, --cyr
                        convert to Cyrillic script
```
