---
layout: post
title:  "Elixir package for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://hex.pm/packages/uklatn](https://hex.pm/packages/uklatn)


Install
--

Add package dependency:
```elixir
{:uklatn, "~> 1.17"}
```


Usage
--

```elixir
import Paiv.UkrainianLatin

encode("Доброго вечора!")
#=> "Dobroğo večora!"

decode("Paljanycja")
#=> "Паляниця"
```

Select a transliteration scheme:
```elixir
encode("Борщ", :DSTU_9112_B)
#=> "Borshch"

encode("Шевченко", :KMU_55)
#=> "Shevchenko"
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

