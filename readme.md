uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

[![standwithukraine](docs/StandWithUkraine.svg)](https://ukrainewar.carrd.co/)

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


Python module
--
- [uklatn Python module](python/)

Install with pip:
```sh
pip install 'git+https://github.com/paiv/uklatn.git'
```

Usage:
```py
import uklatn
uklatn.encode("Доброго вечора!")
uklatn.decode("Paljanycja")
```


C library
--
- [uklatn C library](c/)


Swift package
--
- [uklatn Swift package](swift/)

Add package dependency:
```sh
swift package add-dependency 'https://github.com/paiv/uklatn.git' --from '1.0.0'
```

Use in target dependencies in `Package.swift`:
```swift
.product(name: "UKLatn", package: "uklatn")
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed fully.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

