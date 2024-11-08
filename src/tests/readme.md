Test data
==

The structure of a test json file:
- Each test record has these properties:
  - `cyr` the Cyrillic text,
  - `lat` the Latin equivalent,
  - `test` the direction of the test, one of:
    - `cyr <> lat`
    - `cyr > lat`
    - `lat > cyr`

Example
--
```json
[
  {
    "test": "cyr > lat",
    "cyr": "щастя",
    "lat": "shchastja"
  },
  {
    "test": "lat > cyr",
    "lat": "mrija",
    "cyr": "мрія"
  }
]
```
