---
layout: post
title:  "Ruby Ukrainian Cyrillic to Latin script transliteration"
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
puts tr.encode('Доброго вечора!')
puts tr.decode('Paljanycja')
```

Select a transliteration scheme:

```ruby
tr.encode('Борщ', 'DSTU_9112_A')
```

Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

