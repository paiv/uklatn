#!/usr/bin/env python
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
    c2lr = list()
    l2cr = list()
    c2l = list()
    l2c = list()

    for fn in fns:
        logger.info(f'processing {fn!s}')
        name = fn.stem
        table = table_name(name)
        for kind, cyr, lat in _parse_tests(fn):
            match kind:
                case 'c2lr': c2lr.append((cyr, lat, table))
                case 'l2cr': l2cr.append((cyr, lat, table))
                case 'c2l' : c2l.append((cyr, lat, table))
                case 'l2c' : l2c.append((cyr, lat, table))
                case _: raise Exception()

    def gen_test_data(name, data, file):
        print(f'static const struct _uklatn_test _{name}_data[] = {{', file=file)
        for cyr, lat, table in data:
            print('    {', file=file)
            print(f'        u{_j(cyr)},', file=file)
            print(f'        u{_j(lat)},', file=file)
            print(f'        UklatnTable_{table},', file=file)
            print('    },', file=file)
        print('};\n', file=file)
    with io.StringIO() as so:
        gen_test_data('cyr2lat2cyr', c2lr, file=so)
        gen_test_data('lat2cyr2lat', l2cr, file=so)
        gen_test_data('cyr2lat', c2l, file=so)
        gen_test_data('lat2cyr', l2c, file=so)
        return so.getvalue()


def gen_transforms(fns, default_table):
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

    with io.StringIO() as so:
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            tname = table_name(name)
            vname = table_varname(name)
            rname = var_name(name)
            names.append((vname, rname))
            text = fn.read_text()
            print(f'static const UChar {vname}[] = u"{tname}";\n', file=so)
            print(f'static char {rname}[] =', file=so)
            for line in text.splitlines():
                if line:
                    s = json.dumps(line, ensure_ascii=False)
                    print(f'    {s}', file=so)
            print(f'    ;', file=so)
            print('', file=so)

        print('static int', file=so)
        print('_uklatn_register_tables(void) {', file=so)
        print('int err = 0;', file=so)
        for tname, rname in names:
            print(f'    err = _uklatn_register_table({tname}, {rname});', file=so)
            print('    if (err != 0) { return err; }', file=so)
        print('    return 0;', file=so)
        print('}', file=so)
        return so.getvalue()

