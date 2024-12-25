---
layout: post
title:  "Rust crate for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://crates.io/crates/uklatn](https://crates.io/crates/uklatn)


Install
--

Add package dependency:
```sh
cargo add uklatn
```


Usage
--

```rust
use {uklatn::Table, uklatn::decode, uklatn::encode};

encode("Доброго вечора!", Table::default());
decode("Paljanycja", Table::default());
```

Set the transliteration scheme:

```rust
encode("Борщ", Table::Dstu9112B);
encode("Шевченко", Table::Kmu55);
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

