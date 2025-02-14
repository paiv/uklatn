---
layout: post
title:  "PHP package for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://packagist.org/packages/paiv/uklatn](https://packagist.org/packages/paiv/uklatn)


Install
--

Add dependency to composer.json:
```sh
php composer.phar require 'paiv/uklatn'
```


Usage
--

```php
use Paiv\UkrainianLatin;

$tr = new UkrainianLatin();

$tr->encode('Доброго вечора!');
$tr->decode('Paljanycja');
```

Set the transliteration scheme:
```php
$tr->encode('Доброго вечора!', UkrainianLatin::DSTU_9112_B);
$tr->encode('Шевченко', UkrainianLatin::KMU_55);
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
