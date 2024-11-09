uklatn
==
Ukrainian Cyrillic transliteration to Latin script.


Usage:
```js
import * as uklatn from 'uklatn';
let s = uklatn.encode('Доброго вечора!');
let t = uklatn.decode('Paljanycja');
```

Select a transliteration scheme:
```js
let s = uklatn.encode('Борщ', 'DSTU_9112_A');
```

Command-line executable
--
```sh
npx uklatn 'моє щастя'
```

```txt
usage: uklatn [-h] [-t TABLE] [-c] [-l] text [text ...]

arguments:
  text            text to transliterate
  -               read text from stdin

options:
  -h, --help            show this help message and exit
  -t, --table {DSTU_9112_A,DSTU_9112_B,KMU_55}
                        transliteration system (default: DSTU_9112_A)
  -l, --lat, --latin    convert to Latin script (default)
  -c, --cyr, --cyrillic convert to Cyrillic script
```
