uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

Build
--
The package contains a C extension module, with ICU dependency.

Build with `make`, and provide C compilation flags via environment.
```sh
make clean all test
```

Usage:
```py
import uklatn
uklatn.encode("Доброго вечора!")
uklatn.decode("Paljanycja")
```

Select a transliteration scheme:
```py
uklatn.encode("Борщ", uklatn.DSTU_9112_A)
```
