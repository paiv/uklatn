---
layout: post
title:  "JavaScript Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- https://www.npmjs.com/package/uklatn


Install
--

Install with npm:
```sh
npm install uklatn
```


Usage:
--

```js
import * as uklatn from 'uklatn';
let s = uklatn.encode('Доброго вечора!');
let t = uklatn.decode('Paljanycja');
```

Select a transliteration scheme:
```js
let s = uklatn.encode('Борщ', 'DSTU_9112_A');
```

Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.


Command-line executable
--
```sh
npx uklatn 'моє щастя'
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
