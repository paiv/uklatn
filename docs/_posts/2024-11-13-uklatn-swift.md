---
layout: post
title:  "Swift package for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://swiftpackageindex.com/paiv/uklatn](https://swiftpackageindex.com/paiv/uklatn)


Install
--

Add package dependency:
```sh
swift package add-dependency 'https://github.com/paiv/uklatn.git' --from '1.0.0'
swift package add-target-dependency --package uklatn UkrainianLatin <target-name>
```

Usage
--

```swift
import UkrainianLatin
let s = try! encode("Доброго вечора!")
let t = try! decode("Paljanycja")
print(s, t)
```

Select a transliteration scheme:
```swift
try encode("Борщ", table: UKLatnTable.DSTU_9112_A)
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
