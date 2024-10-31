#!/usr/bin/env python
import io
import json
import logging
import re
from pathlib import Path


logger = logging.getLogger('')


def gen_c(fns):
    logger.debug('C generator start')
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
        logger.debug(f'processing {fn!s}')
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
    logger.debug('C generator end')


def main(args):
    cwd = Path.cwd()
    src = Path(__file__).parent.relative_to(cwd, walk_up=True)
    fns = list(src.glob('uk*.txt'))
    for p in args.package:
        gn = f'gen_{p}'
        g = globals()[gn]
        g(fns)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate source code for the transform tables, and update source packages.')
    parser.add_argument('package', choices=['c'], nargs='*', help='target packages')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    args = parser.parse_args()
    if not args.package:
        parser.print_usage()
    else:
        level = logging.DEBUG if args.verbose else logging.WARN
        logging.basicConfig(level=level)
        main(args)

