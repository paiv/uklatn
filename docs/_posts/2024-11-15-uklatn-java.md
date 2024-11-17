---
layout: post
title:  "Java Ukrainian Cyrillic to Latin script transliteration"
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
    <version>1.12.0</version>
</dependency>
```


Usage
--

```java
import io.github.paiv.uklatn.UkrainianLatin;

UkrainianLatin tr = new UkrainianLatin();

String s = tr.encode("Доброго вечора!");
String t = tr.decode("Paljanycja");

System.out.println(s);
System.out.println(t);
```

Select a transliteration scheme:
```java
import static io.github.paiv.uklatn.UkrainianLatin.UKLatnTable;

tr.encode("Борщ", UKLatnTable.DSTU_9112_A);
```


Notes
--
Input is assumed to be in Ukrainian (Cyrillic or Latin script), and will be processed in full.
If your data has mixed languages, do preprocessing to extract Ukrainian chunks.

