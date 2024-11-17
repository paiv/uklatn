---
layout: post
title:  ".NET Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://www.nuget.org/packages/UkrainianLatin](https://www.nuget.org/packages/UkrainianLatin)


Install
--

Add package dependency:
```sh
dotnet add package UkrainianLatin
```


Usage
--

```csharp
using paiv.uklatn;

UkrainianLatin tr = new UkrainianLatin();
string s = tr.Encode("Доброго вечора!");
string t = tr.Decode("Paljanycja");
```

Select a transliteration scheme:
```csharp
s = tr.Encode("Борщ", UkrainianLatin.Table.DSTU_9112_A);
```

Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
