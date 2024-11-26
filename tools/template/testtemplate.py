import inspect
import itertools
import template
import unittest


class TemplateTest (unittest.TestCase):

    _data = [
    (
        '',
        ''
    ),
    (
        'a',
        'a'
    ),
    (
        '&a', dict(a='x'),
        'x'
    ),
    (
        '&a', dict(),
        '&a'
    ),
    (
        '&a', dict(a=''),
        ''
    ),
    (
        '&a', dict(a=None),
        ''
    ),
    (
        '&a &a', dict(a='x'),
        'x x'
    ),
    (
        '&a &a  &a', dict(a='x'),
        'x x  x'
    ),
    (
        '&{a}', dict(a='x'),
        'x'
    ),
    (
        '&{a}', dict(),
        '&{a}'
    ),
    (
        '&{a}', dict(a=''),
        ''
    ),
    (
        '&{a}', dict(a=None),
        ''
    ),
    (
        '&{a} &{a}', dict(a='x'),
        'x x'
    ),
    (
        '&{a} &{a}  &{a}', dict(a='x'),
        'x x  x'
    ),
    (
        ' a ',
        ' a '
    ),
    (
        ' a\n',
        'a\n'
    ),
    (
        '''
        a
        ''',
        '\na\n'
    ),
    (
        '''
          a
        ''',
        '\na\n'
    ),
    (
        ' &a ', dict(a='x'),
        ' x '
    ),
    (
        ' &a\n', dict(a='x'),
        'x\n'
    ),
    (
        ' &a\n', dict(a=''),
        '\n'
    ),
    (
        ' &a\n', dict(a=None),
        '\n'
    ),
    (
        '''
        &a
        ''', dict(a='x'),
        '\nx\n'
    ),
    (
        '''
          &a
        ''', dict(a='x'),
        '\nx\n'
    ),
    (
        '''
          &a
        ''', dict(a='x\n'),
        '\nx\n'
    ),
    (
        '''
          &a
        ''', dict(a='x\ny\n'),
        '\nx\ny\n'
    ),
    (
        '''
          &a
        ''', dict(a='x\ny'),
        '\nx\ny\n'
    ),
    (
        '''
        b
          &a
        c
        ''', dict(a=''),
        '\nb\n\nc\n'
    ),
    (
        '''
        b
          &a &a
        c
        ''', dict(a='x'),
        '\nb\n  x x\nc\n'
    ),
    (
        '''
        b
          &a
        ''', dict(a=('x\n' for _ in range(2))),
        '\nb\n  x\n  x\n'
    ),
    (
        '''
        b
          &a
        ''', dict(a=('x\n' for _ in range(0))),
        '\nb\n'
    ),
    (
        r'\n \t \& \\ \&a',
        r'\n \t \& \\ \&a'
    ),
    ]

    def _driver(self, source):
        for tid, (*tpl, expect) in enumerate(source):
            with self.subTest(idx=tid):
                s = template.format(*tpl)
                self.assertEqual(s, expect)

    def test_data(self):
        with self.subTest(source='data'):
            self._driver(self._data)

    def test_from_datagen(self):
        data = DataGen()
        for name, gen in data.sources():
            with self.subTest(source=name):
                self._driver(gen)


class DataGen:

    def sources(self):
        members = inspect.getmembers(DataGen, predicate=inspect.isfunction)
        for name, func in members:
            if name.startswith('src_'):
                yield (name[4:], func(self))

    def src_space_suffix(self):
        space = ' \t\n'
        words = ('v', 'cdefg')
        for ps in itertools.product(words, space):
            s = ''.join(ps)
            yield (s, s)

    def src_space_prefix(self):
        space = ' \t\n'
        words = ('v', 'cdefg')
        for ps in itertools.product(space, words):
            s = ''.join(ps)
            yield (s, s)

    def src_space_around(self):
        space = ' \t'
        words = ('v', 'cdefg')
        for ps in itertools.product(space, words, space):
            s = ''.join(ps)
            yield (s, s)

    def src_ending(self):
        pfx = ('', 'v', 'cdefg')
        sfx = ('&', '\\', '&{')
        for ps in itertools.product(pfx, sfx):
            s = ''.join(ps)
            yield (s, s)


if __name__ == '__main__':
    unittest.main()
