#!/usr/bin/env python
import io
import json
import logging
import re
import sys
from pathlib import Path


logger = logging.getLogger(Path(__file__).stem)


def _parse_tests(fn):
    hrx = re.compile(r'^\s*==\s*(.*?)\s*$', re.I)
    def state_for_header(line):
        m = hrx.match(line)
        if m:
            ps = tuple(m.group(1).lower().split())
            if (len(ps) == 3):
                match ps:
                    case ('cyr', '<>', 'lat'):
                        return 0
                    case ('lat', '<>', 'cyr'):
                        return 2
                    case ('cyr', '>', 'lat'):
                        return 4
                    case ('lat', '>', 'cyr'):
                        return 6
            raise Exception(f'invalid section header: {line!r}')

    text = fn.read_text()
    test_in = None
    state = 0
    for row, line in enumerate(text.splitlines(), 1):
        if not line.strip(): continue
        header = state_for_header(line)
        match state:
            case 0:
                if header is not None:
                    state = header
                else:
                    test_in = line
                    state += 1
            case 1:
                if header is not None:
                    raise Exception(f':{row}: incomplete test')
                yield ('c2lr', test_in, line)
                state -= 1
            case 2:
                if header is not None:
                    state = header
                else:
                    test_in = line
                    state += 1
            case 3:
                if header is not None:
                    raise Exception(f':{row}: incomplete test')
                yield ('l2cr', line, test_in)
                state -= 1
            case 4:
                if header is not None:
                    state = header
                else:
                    test_in = line
                    state += 1
            case 5:
                if header is not None:
                    raise Exception(f':{row}: incomplete test')
                yield ('c2l', test_in, line)
                state -= 1
            case 6:
                if header is not None:
                    state = header
                else:
                    test_in = line
                    state += 1
            case 7:
                if header is not None:
                    raise Exception(f':{row}: incomplete test')
                yield ('l2c', line, test_in)
                state -= 1
    match state:
        case 1 | 3 | 5 | 7:
            raise Exception(f':{row}: incomplete test')


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
        for kind, a, b in _parse_tests(fn):
            match kind:
                case 'c2lr': c2lr.append((a, b, table))
                case 'l2cr': l2cr.append((a, b, table))
                case 'c2l' : c2l.append((a, b, table))
                case 'l2c' : l2c.append((a, b, table))
                case _: raise Exception()
    return [c2lr, l2cr, c2l, l2c]


def gen_c(fns):
    logger.info('C generator start')
    c2lr, l2cr, c2l, l2c = _collect_tests(fns)

    def gen_test_data(name, data, file):
        print(f'static const struct _uklatn_test _{name}_data[] = {{', file=file)
        for a,b,t in data:
            print('    {', file=file)
            print(f'        u{a},', file=file)
            print(f'        u{b},', file=file)
            print(f'        UklatnTable_{t},', file=file)
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
    fns = sorted(src.glob('test*.txt'))
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

