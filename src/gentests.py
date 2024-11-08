#!/usr/bin/env python
import io
import json
import logging
import re
import sys
from pathlib import Path


logger = logging.getLogger(Path(__file__).stem)


def _parse_tests(fn):
    def parse_kind(s):
        match s.lower().split():
            case ['cyr', '<>', 'lat']:
                return 'c2lr'
            case ['lat', '<>', 'cyr']:
                return 'l2cr'
            case ['cyr', '>', 'lat']:
                return 'c2l'
            case ['lat', '>', 'cyr']:
                return 'l2c'
            case _:
                raise Exception(f'unknown test kind: {s!r}')
    with fn.open() as fp:
        data = json.load(fp)
    return [[parse_kind(obj['test']), obj['cyr'], obj['lat']] for obj in data]


def _collect_tests(fns):
    def table_name(s):
        return re.sub(r'test_', '', s)
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
    return [c2lr, l2cr, c2l, l2c]


def gen_c(fns):
    logger.info('C generator start')
    c2lr, l2cr, c2l, l2c = _collect_tests(fns)

    def _j(s):
        return json.dumps(s, ensure_ascii=False)
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
        print(so.getvalue())

    logger.info('C generator end')


def main(args):
    cwd = Path.cwd()
    src = Path(__file__).parent.relative_to(cwd, walk_up=True)
    src /= 'tests'
    fns = sorted(src.glob('test*.json'))
    for p in args.package:
        gn = f'gen_{p}'
        g = globals()[gn]
        g(fns)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate test code for the transform tables.')
    parser.add_argument('package', choices=['c'], nargs='*', help='target packages')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    args = parser.parse_args()
    if not args.package:
        parser.print_usage()
    else:
        level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(level=level)
        main(args)

