uklatn
==
Ukrainian Cyrillic transliteration to Latin script.

```swift
import UKLatn
let s = try! encode("Доброго вечора!")
let t = try! decocde("Paljanycja")
print(s, t)
```

Select a transliteration scheme:
```swift
try encode("Борщ", table: UKLatnTable.DSTU_9112_A)
```

