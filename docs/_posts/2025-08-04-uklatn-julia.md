---
layout: post
title:  "Julia package for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://github.com/paiv/uklatn/julia/](https://github.com/paiv/uklatn/julia/)


Install
--

```julia-repl
julia> ]
pkg> add https://github.com/paiv/uklatn:julia/
```


Usage:
```julia
using UkrainianLatin: encode, decode

encode("Доброго вечора!")
decode("Paljanycja")
```

Set the transliteration scheme:
```julia
encode("Борщ", :DSTU_9112_B)
encode("Шевченко", :KMU_55)
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

