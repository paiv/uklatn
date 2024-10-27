import unittest
import uklatn


class TestDSTU_A (unittest.TestCase):

    _data = [
        (
            "Доброго вечора, ми з України!",
            "Dobroğo večora, my z Ukraïny!"
        ),
    ]

    def test_encode(self):
        for cyr, lat in self._data:
            q = uklatn.encode(cyr, uklatn.DSTU_A)
            self.assertEqual(q, lat)

    def test_decode(self):
        for cyr, lat in self._data:
            q = uklatn.decode(lat, uklatn.DSTU_A)
            self.assertEqual(q, cyr)


class TestDSTU_B (unittest.TestCase):

    _data = [
        (
            "Доброго вечора, ми з України!",
            "Dobrogho vechora, my z Ukrajiny!"
        ),
    ]

    def test_encode(self):
        for cyr, lat in self._data:
            q = uklatn.encode(cyr, uklatn.DSTU_B)
            self.assertEqual(q, lat)

    def test_decode(self):
        for cyr, lat in self._data:
            q = uklatn.decode(lat, uklatn.DSTU_B)
            self.assertEqual(q, cyr)


if __name__ == '__main__':
    unittest.main()

