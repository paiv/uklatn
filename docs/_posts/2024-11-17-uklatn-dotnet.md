---
layout: post
title:  ".NET package for Ukrainian Cyrillic to Latin script transliteration"
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
tr.Encode("Доброго вечора!");
tr.Decode("Paljanycja");
```

Set the transliteration scheme:
```csharp
tr.Encode("Борщ", UkrainianLatin.Table.DSTU_9112_B);
tr.Encode("Шевченко", UkrainianLatin.Table.KMU_55);
```

Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
