import json
import logging
import re
from pathlib import Path
import template


logger = logging.getLogger(Path(__file__).stem)


def gen_tests(fns, default_table):
    def _parse_tests(fn):
        def parse_kind(s):
            match s.lower().split():
                case ['cyr', '<>', 'lat']: return 'c2lr'
                case ['lat', '<>', 'cyr']: return 'l2cr'
                case ['cyr', '>', 'lat']: return 'c2l'
                case ['lat', '>', 'cyr']: return 'l2c'
                case _:
                    raise Exception(f'unknown test kind: {s!r}')
        with fn.open() as fp:
            data = json.load(fp)
        return [[parse_kind(obj['test']), obj['cyr'], obj['lat']] for obj in data]

    def table_name(s):
        return re.sub(r'test_', '', s)
    def _j(s):
        return json.dumps(s, ensure_ascii=False)

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'q = uklatn.encode(cyr, uklatn.{table})\n'
            yield 'self.assertEqual(q, lat)\n'
        else:
            yield f'q = uklatn.decode(lat, uklatn.{table})\n'
            yield 'self.assertEqual(q, cyr)\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'q = uklatn.decode(lat, uklatn.{table})\n'
                yield 'self.assertEqual(q, cyr)\n'
            else:
                yield f'q = uklatn.encode(cyr, uklatn.{table})\n'
                yield 'self.assertEqual(q, lat)\n'

    def _emit_tests_default(kind):
        if kind[0] == 'c':
            yield 'q = uklatn.encode(cyr)\n'
            yield 'self.assertEqual(q, lat)\n'
        else:
            yield 'q = uklatn.decode(lat)\n'
            yield 'self.assertEqual(q, cyr)\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield 'q = uklatn.decode(lat)\n'
                yield 'self.assertEqual(q, cyr)\n'
            else:
                yield 'q = uklatn.encode(cyr)\n'
                yield 'self.assertEqual(q, lat)\n'

    def _emit_testset(data, table):
        def _data(data):
            spl = '''\
            (
                &cyr,
                &lat,
            ),
            '''
            for cyr,lat in data:
                yield template.format(spl, cyr=_j(cyr), lat=_j(lat))

        def _tests():
            tpl = '''
            def test_&kind(self):
                data = [
                    &data
                ]

                for cyr,lat in data:
                    &tests
                    &dtests
            '''
            ctx = dict(table=table)
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                ctx['kind'] = kind
                ctx['data'] = _data(xs)
                ctx['tests'] = _emit_tests(kind, table)
                ctx['dtests'] = iter('')
                if table == default_table:
                    ctx['dtests'] = _emit_tests_default(kind)
                yield template.format(tpl, ctx)

        tpl = '''

        class Test&table (unittest.TestCase):
            &tests
        '''
        return template.format(tpl, table=table, tests=_tests)

    def _test_cases():
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            data = _parse_tests(fn)
            yield from _emit_testset(data, table)

    context = dict()
    context['test_cases'] = _test_cases

    tpl = '''\
    import uklatn
    import unittest
    &{test_cases}


    if __name__ == "__main__":
        unittest.main()
    '''

    text = template.format(tpl, context)
    return text


def gen_transforms(fns, default_table=None):
    def table_name(s):
        s, = re.findall(r'uk_Latn_(.*?)(?:-uk)?\s*$', s, flags=re.I)
        return s.replace('-', '_')
    def class_name(s):
        return '_Uklatn_' + s.replace('-', '_')
    def _isdec(s):
        return s.startswith('uk_Latn_')
    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s),
            [r['map'] for r in s]
        ] for s in data]

    def _emit_trrules(rules):
        tpl = '''\
        self._rx&sid = re.compile(r"&rx")
        _maps&sid = &maps
        def tr&sid(m):
            value = None
            if (i := m.lastindex) is not None:
                value = _maps&sid[i-1].get(m.group(i))
            return value if (value is not None) else m.group(0)
        self._tr&sid = tr&sid
        '''
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                yield template.format(tpl, sid=sid, rx=rx, maps=repr(maps))

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'text = unicodedata.normalize({section!r}, text)\n'
            else:
                yield f'text = self._rx{sid}.sub(self._tr{sid}, text)\n'

    def _emit_tr(cname, rules):
        ctx = dict(cname=cname)
        ctx['trrules'] = _emit_trrules(rules)
        ctx['trbody'] = _emit_trbody(rules)
        tpl = '''

        class &cname:
            def __init__(self):
                &trrules

            def transform(self, text):
                &trbody
                return text
        '''
        return template.format(tpl, ctx)

    tables = dict()
    for fn in fns:
        logger.info(f'processing {fn!s}')
        with fn.open() as fp:
            rules = json.load(fp)
            rules = _load_rules(rules)
        name = fn.stem
        table = table_name(name)
        cname = class_name(name)
        if table not in tables:
            tables[table] = [None, None]
        tables[table][_isdec(name)] = (cname, rules)

    def _emit_tables():
        for ar in [0,1]:
            for table, codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    yield _emit_tr(cname, rules)

        def _entries():
            for table, codec in tables.items():
                enc,dec = codec
                enc = f'{enc[0]}()' if enc else None
                dec = f'{dec[0]}()' if dec else None
                yield f'[{enc}, {dec}],\n'
        tpl = '''

        _UklatnTables = [
            [None, None],
            &entries
        ]
        '''
        yield template.format(tpl, entries=_entries)

    context = dict()
    context['doc_tables'] = '\n'.join((f' - {s}' + (' (default)' if s == default_table else '')) for s in tables) + '\n'
    context['global_tenum'] = '\n'.join(f'{table} = {tid}' for tid, table in enumerate(tables, 1))
    context['all_tables'] = ', '.join(f'{s!r}' for s in tables)
    context['global_tables'] = _emit_tables
    context['default_table'] = default_table
    context['sdefault_table'] = repr(default_table) + '\n'
    context['table_list'] = repr(list(tables))
    context['table_names'] = repr({k:i for i,k in enumerate(tables, 1)}) + '\n'

    tpl = '''
"""Ukrainian Cyrillic transliteration to Latin script

https://github.com/paiv/uklatn

encode(...): transliterate Cyrlllic to Latin script
decode(...): re-transliterate Latin script back to Cyrillic

Transliteration schemes:
&{doc_tables}

For example,
    >>> import uklatn
    >>> uklatn.encode("Доброго вечора!")
    'Dobroğo večora!'
    >>> uklatn.decode("Paljanycja")
    'Паляниця'

To set the transliteration scheme:
    >>> uklatn.encode("Щастя", table=uklatn.KMU_55)
    'Shchastia'

"""

import re
import unicodedata


__all__ = [&{all_tables}, 'decode', 'encode']


&{global_tenum}
&{global_tables}


def encode(text, table=None):
    """
    Transliterates a string of Ukrainian Cyrillic to Latin script.

    Signature:
      encode(str, int)

    Args:
      text (str): The Ukrainian Cyrillic string to transliterate.
      table (int): The transliteration table, one of:
       - uklatn.DSTU_9112_A: DSTU 9112:2021 System A
       - uklatn.DSTU_9112_B: DSTU 9112:2021 System B
       - uklatn.KMU_55: KMU 55:2010

    Returns:
      The transliterated string.
    """

    if table is None:
        table = DSTU_9112_A
    enc, _ = _UklatnTables[table]
    if not enc:
        raise ValueError(f'invalid table {table!r}')
    return enc.transform(text)


def decode(text, table=None):
    """
    Re-transliterates a string of Ukrainian Latin to Cyrillic script.

    Signature:
      decode(str, int)

    Args:
      text (str): The Ukrainian Latin string to transliterate.
      table (int): The transliteration table, one of:
       - uklatn.DSTU_9112_A: DSTU 9112:2021 System A
       - uklatn.DSTU_9112_B: DSTU 9112:2021 System B

    Returns:
      The re-transliterated string.
    """

    if table is None:
        table = DSTU_9112_A
    _, dec = _UklatnTables[table]
    if not dec:
        raise ValueError(f'invalid table {table!r}')
    return dec.transform(text)


def main(args):
    table = args.table
    if table is None:
        table = &{sdefault_table}

    names = &{table_names}
    table = names[table]

    tr = encode
    if args.cyrillic and not args.latin:
        tr = decode

    if args.file:
        text = args.file.read()
        res = tr(text, table)
        print(res, end='')

    if args.text:
        text = ' '.join(args.text)
        res = tr(text, table)
        print(res)


if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('text', nargs='*', help='text to transliterate')
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='read text from file')
    parser.add_argument('-t', '--table', choices=&{table_list}, help='transliteration system (default: &{default_table})')
    parser.add_argument('-l', '--latin', '--lat', action='store_true', help='convert to Latin script (default)')
    parser.add_argument('-c', '--cyrillic', '--cyr', action='store_true', help='convert to Cyrillic script')

    args = parser.parse_args()
    if (not args.text) and (not args.file):
        parser.error(f'the following arguments are required: text or file')

    main(args)
'''
    text = template.format(tpl, context)
    return text

