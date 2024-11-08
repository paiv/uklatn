#!/usr/bin/env python
import io
import json
import logging
import re
from pathlib import Path


logger = logging.getLogger(Path(__file__).stem)


_DefaultTable = 'DSTU_9112_A'


def gen_c(src):
    logger.info('C generator start')
    src /= 'icu'
    fns = sorted(src.glob('uk*.txt'))
    def table_name(s):
        s = re.sub(r'\buk_Latn_', 'uk_', s, flags=re.I)
        return '-'.join(
          '_'.join(c.replace('_', '') for c in p.split('_', maxsplit=1))
          for p in s.split('-'))
    def table_varname(s):
        s = re.sub(r'\buk_Latn_|\buk_', '', s, flags=re.I)
        s = s.replace('-', '_')
        return f'_TableName_{s}'
    def var_name(s):
        s = re.sub(r'\buk_Latn_|\b_uk', '', s, flags=re.I)
        s = s.replace('-', '_')
        return f'_Table_{s}'
    names = list()
    for fn in fns:
        logger.info(f'processing {fn!s}')
        name = fn.stem
        tname = table_name(name)
        vname = table_varname(name)
        rname = var_name(name)
        names.append((vname, rname))
        text = fn.read_text()
        with io.StringIO() as so:
            print(f'static const UChar {vname}[] = u"{tname}";\n', file=so)
            print(f'static char {rname}[] =', file=so)
            for line in text.splitlines():
                if line:
                    s = json.dumps(line, ensure_ascii=False)
                    print(f'    {s}', file=so)
            print(f'    ;', file=so)
            print(so.getvalue())

    with io.StringIO() as so:
        print('static int', file=so)
        print('_uklatn_register_tables(void) {', file=so)
        print('int err = 0;', file=so)
        for tname, rname in names:
            print(f'    err = _uklatn_register_table({tname}, {rname});', file=so)
            print('    if (err != 0) { return err; }', file=so)
        print('    return 0;', file=so)
        print('}', file=so)
        print(so.getvalue())
    logger.info('C generator end')


def gen_py(src):
    logger.info('PY generator start')
    src /= 'regex'
    fns = sorted(src.glob('uk*.json'))

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

    context['doc_tables'] = '\n'.join((f' - {s}' + (' (default)' if s == _DefaultTable else '')) for s in tables)
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
'''
    text = template.format(**context)
    print(text, end='')
    logger.info('PY generator end')


def main(args):
    cwd = Path.cwd()
    src = Path(__file__).parent.relative_to(cwd, walk_up=True)
    for p in args.package:
        gn = f'gen_{p}'
        g = globals()[gn]
        g(src)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate source code for the transform tables.')
    parser.add_argument('package', choices=['c', 'py'], nargs='*', help='target packages')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    args = parser.parse_args()
    if not args.package:
        parser.print_usage()
    else:
        level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(level=level)
        main(args)

