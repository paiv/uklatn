import unittest
import uklatn


class TestCase (unittest.TestCase):

    _data = [
        (
            "Доброго вечора, ми з України!",
            "Dobroğo večora, my z Ukraïny!"
        )
    ]

    def test_encode(self):
        for cyr, lat in self._data:
            q = uklatn.encode(cyr)
            self.assertEqual(q, lat)

    def test_decode(self):
        for cyr, lat in self._data:
            q = uklatn.decode(lat)
            self.assertEqual(q, cyr)


if __name__ == '__main__':
    unittest.main()

