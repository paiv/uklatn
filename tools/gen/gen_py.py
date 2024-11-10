import io
import json
import logging
import re
from pathlib import Path


logger = logging.getLogger(Path(__file__).stem)


def gen_tests(fns):
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
    def _emit_tests(kind, data, table, file):
        data = [(cyr,lat) for k,cyr,lat in data if k == kind]
        if not data: return
        print(f'    def test_{kind}(self):', file=so)
        print('        data = [', file=so)
        for cyr,lat in data:
            print('            (', file=so)
            print(f'                {_j(cyr)},', file=so)
            print(f'                {_j(lat)},', file=so)
            print('            ),', file=so)
        print('        ]\n', file=so)
        print(f'        for cyr,lat in data:', file=so)
        if kind[0] == 'c':
            print(f'            q = uklatn.encode(cyr, uklatn.{table})', file=so)
            print(f'            self.assertEqual(q, lat)', file=so)
        else:
            print(f'            q = uklatn.decode(lat, uklatn.{table})', file=so)
            print(f'            self.assertEqual(q, cyr)', file=so)
        if kind[-1] == 'r':
            if kind[0] == 'c':
                print(f'            q = uklatn.decode(lat, uklatn.{table})', file=so)
                print(f'            self.assertEqual(q, cyr)', file=so)
            else:
                print(f'            q = uklatn.encode(cyr, uklatn.{table})', file=so)
                print(f'            self.assertEqual(q, lat)', file=so)
        print('', file=so)

    with io.StringIO() as so:
        print('import uklatn', file=so)
        print('import unittest\n\n', file=so)
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            data = _parse_tests(fn)
            print(f'class Test{table} (unittest.TestCase):\n', file=so)
            _emit_tests('c2lr', data, table, file=so)
            _emit_tests('l2cr', data, table, file=so)
            _emit_tests('c2l', data, table, file=so)
            _emit_tests('l2c', data, table, file=so)
            print('', file=so)

        print('if __name__ == "__main__":', file=so)
        print('    unittest.main()', file=so)
        print('', file=so)
        return so.getvalue()


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

    def _emit_tr(cname, rules, file):
        rules = _load_rules(rules)
        print(f'class {cname}:', file=file)
        print(f'    def __init__(self):', file=file)
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                print(f'        self._rx{sid} = re.compile(r"{rx}")', file=file)
                print(f'        _maps{sid} = {maps!r}', file=file)
                print(f'        def tr{sid}(m):', file=file)
                print(f'            value = None', file=file)
                print(f'            if (i := m.lastindex) is not None:', file=file)
                print(f'                value = _maps{sid}[i-1].get(m.group(i))', file=file)
                print(f'            return value if (value is not None) else m.group(0)', file=file)
                print(f'        self._tr{sid} = tr{sid}', file=file)
        print('', file=file)
        print(f'    def transform(self, text):', file=file)
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                print(f'        text = unicodedata.normalize({section!r}, text)', file=file)
            else:
                print(f'        text = self._rx{sid}.sub(self._tr{sid}, text)', file=file)
        print(f'        return text', file=file)
        print('\n', file=file)

    context = dict()
    tables = dict()
    with io.StringIO() as so:
        for fn in fns:
            logger.info(f'processing {fn!s}')
            with fn.open() as fp:
                rules = json.load(fp)
            name = fn.stem
            table = table_name(name)
            cname = class_name(name)
            if table not in tables:
                tables[table] = [None, None]
            tables[table][_isdec(name)] = cname
            _emit_tr(cname, rules, so)
        classdefs_tables = so.getvalue()

    all_tables = ', '.join(f'{s!r}' for s in tables)
    context['global_all'] = f"__all__ = [{all_tables}, 'decode', 'encode']"

    context['doc_tables'] = '\n'.join((f' - {s}' + (' (default)' if s == default_table else '')) for s in tables)
    context['global_tenum'] = '\n'.join(f'{table} = {tid}' for tid, table in enumerate(tables, 1))

    with io.StringIO() as so:
        print('_UklatnTables = [', file=so)
        print('    [None, None],', file=so)
        for tid, (table, (enc, dec)) in enumerate(tables.items(), 1):
            if enc:
                enc = f'{enc}()'
            if dec:
                dec = f'{dec}()'
            print(f'    [{enc}, {dec}],', file=so)
        print(']', end='', file=so)
        tabledef = so.getvalue()

    context['global_tables'] = classdefs_tables + tabledef
    context['default_table'] = default_table
    context['table_list'] = list(tables)
    context['table_names'] = {k:i for i,k in enumerate(tables, 1)}

    template = '''
"""Ukrainian Cyrillic transliteration to Latin script

https://github.com/paiv/uklatn

encode(...): tranliterate Cyrlllic to Latin script
decode(...): re-transliterate Latin script back to Cyrillic

Tranliteration schemes:
{doc_tables}

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


{global_all}


{global_tenum}


{global_tables}


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
        raise ValueError(f'invalid table {{table!r}}')
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
        raise ValueError(f'invalid table {{table!r}}')
    return dec.transform(text)


def main(args):
    table = args.table
    if table is None:
        table = {default_table!r}

    names = {table_names!r}
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
    parser.add_argument('-t', '--table', choices={table_list!r}, help='transliteration system (default: {default_table})')
    parser.add_argument('-l', '--latin', action='store_true', help='convert to Latin script (default)')
    parser.add_argument('-c', '--cyrillic', action='store_true', help='convert to Cyrillic script')

    args = parser.parse_args()
    if (not args.text) and (not args.file):
        parser.error(f'the following arguments are required: text or file')

    main(args)
'''
    text = template.format(**context)
    return text

