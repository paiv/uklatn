---
layout: post
title:  "PHP package for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://github.com/paiv/uklatn/tree/php](https://github.com/paiv/uklatn/tree/php)


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

$s = $tr->encode('Доброго вечора!');
$t = $tr->decode('Paljanycja');
```

Select a transliteration scheme:
```php
$tr->encode('Доброго вечора!', UkrainianLatin::DSTU_9112_A);
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

