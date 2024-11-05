Test data
==

The format of a test data file:
- The file is divided into sections, each section having a header.
- Possible section headers are:
  - `== cyr <> lat`
  - `== lat <> cyr`
  - `== cyr > lat`
  - `== lat > cyr`
- Each test case inside a section is a pair of `"`-quoted strings.
- Each string in the pair is iterpreted according to its section header.


Example
--
```txt
== cyr > lat
"щастя"
"shchastja"
"мрія"
"mrija"
```
