---
layout: post
title:  "Ruby gem for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://rubygems.org/gems/uklatn](https://rubygems.org/gems/uklatn)


Install
--

Add gem dependency:
```ruby
gem 'uklatn'
```


Usage
--

```ruby
require 'uklatn'

tr = UkrainianLatin.new

tr.encode('Доброго вечора!')
tr.decode('Paljanycja')
```

Set the transliteration scheme:

```ruby
tr.encode('Борщ', 'DSTU_9112_B')
tr.encode('Шевченко', 'KMU_55')
```

Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
