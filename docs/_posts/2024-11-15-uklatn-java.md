---
layout: post
title:  "Java package for Ukrainian Cyrillic to Latin script transliteration"
author: paiv
---

- [https://central.sonatype.com/artifact/io.github.paiv.uklatn/uklatn](https://central.sonatype.com/artifact/io.github.paiv.uklatn/uklatn)


Install
--

Add dependency to pom.xml:
```pom.xml
<dependency>
    <groupId>io.github.paiv.uklatn</groupId>
    <artifactId>uklatn</artifactId>
    <version>1.20.0</version>
</dependency>
```


Usage
--

```java
import io.github.paiv.uklatn.UkrainianLatin;

UkrainianLatin tr = new UkrainianLatin();

tr.encode("Доброго вечора!");
tr.decode("Paljanycja");
```

Set the transliteration scheme:
```java
import static io.github.paiv.uklatn.UkrainianLatin.UKLatnTable;

tr.encode("Борщ", UKLatnTable.DSTU_9112_B);
tr.encode("Шевченко", UKLatnTable.KMU_55);
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.
