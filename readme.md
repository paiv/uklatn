uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

[![standwithukraine](docs/StandWithUkraine.svg)](https://ukrainewar.carrd.co/)
[![](https://github.com/paiv/uklatn/actions/workflows/test-builds.yml/badge.svg)](https://github.com/paiv/uklatn/actions)

[JavaScript](#javascript-package) | [Python](#python-module) | [C](c/) | [Java](#java-library) | [.NET](#net-package) | [Go](#go-package) | [PHP](#php-package) | [Swift](#swift-package) | [Ruby](#ruby-gem)

Supported transliteration schemes:
- [DSTU 9112:2021](https://uk.wikipedia.org/wiki/ДСТУ_9112:2021)
- [KMU 55:2010](https://zakon.rada.gov.ua/laws/show/55-2010-п)


JavaScript package
--
- [uklatn JavaScript package](js/)

Install with npm:
```sh
npm install uklatn
```

Usage:
```js
import * as uklatn from 'uklatn';
uklatn.encode("Доброго вечора!");
uklatn.decode("Paljanycja");
```


Python module
--
- [uklatn Python module](python/)

Install with pip:
```sh
pip install uklatn
```


Java library
--
- [uklatn Java library](java/)

Add dependency to pom.xml:
```pom.xml
<dependency>
    <groupId>io.github.paiv.uklatn</groupId>
    <artifactId>uklatn</artifactId>
    <version>1.12.0</version>
</dependency>
```


.NET package
--
- [uklatn .NET package](csharp/)

Add package dependency:
```sh
dotnet add package UkrainianLatin
```


Go package
--
- [uklatn Go package](go/uklatn/)

Add package dependency:
```sh
go get github.com/paiv/uklatn/go/uklatn
```


PHP package
--
- [uklatn PHP package](php/)

Add package dependency:
```sh
php composer.phar require 'paiv/uklatn'
```


Swift package
--
- [uklatn Swift package](swift/)

Add package dependency:
```sh
swift package add-dependency 'https://github.com/paiv/uklatn.git' --from '1.0.0'
swift package add-target-dependency --package uklatn UkrainianLatin <target-name>
```


Ruby Gem
--
- [uklatn Ruby gem](ruby/)

Add gem dependency:
```ruby
gem 'uklatn'
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

