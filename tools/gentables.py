#!/usr/bin/env python
import logging
from pathlib import Path


logger = logging.getLogger(Path(__file__).stem)


_DefaultTable = 'DSTU_9112_A'


def _basegen(args, default_path, glob, generator):
    cwd = Path.cwd()
    source = args.source
    if isinstance(source, str):
        source = [source]
    if not source:
        root = Path(__file__).parent.parent
        source = [root / default_path]

    for src in source:
        src = Path(src).absolute().relative_to(cwd, walk_up=True)
        if not src.exists():
            raise ValueError(f'not found: {str(src)!r}')
        fns = sorted(src.glob(glob))
        if not fns:
            logger.warning(f'empty source: {str(src)!r}')
        text = generator(fns, _DefaultTable)
        yield text


def gen_c(args):
    logger.info('C generator start')
    from gen import gen_c

    source = _basegen(args, 'src/icu', 'uk*.txt', gen_c.gen_transforms)
    for text in source:
        print(text, end='')

    logger.info('C generator end')


def gen_java(src):
    logger.info('Java generator start')
    from gen import gen_java

    source = _basegen(args, 'src/regex', 'uk*.json', gen_java.gen_transforms)
    for text in source:
        print(text, end='')

    logger.info('Java generator end')


def gen_js(src):
    logger.info('JS generator start')
    from gen import gen_js

    source = _basegen(args, 'src/regex', 'uk*.json', gen_js.gen_transforms)
    for text in source:
        print(text, end='')

    logger.info('JS generator end')


def gen_py(src):
    logger.info('PY generator start')
    from gen import gen_py

    source = _basegen(args, 'src/regex', 'uk*.json', gen_py.gen_transforms)
    for text in source:
        print(text, end='')

    logger.info('PY generator end')


def gen_ruby(src):
    logger.info('Ruby generator start')
    from gen import gen_ruby

    source = _basegen(args, 'src/regex', 'uk*.json', gen_ruby.gen_transforms)
    for text in source:
        print(text, end='')

    logger.info('Ruby generator end')


def gen_swift(src):
    logger.info('Swift generator start')
    from gen import gen_swift

    source = _basegen(args, 'src/regex', 'uk*.json', gen_swift.gen_transforms)
    for text in source:
        print(text, end='')

    logger.info('Swift generator end')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate source code for the transform tables.')
    subpar = parser.add_subparsers(required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')

    parse_c = subpar.add_parser('c', help='C code generator')
    parse_c.add_argument('source', nargs='*', help='source directory')
    parse_c.set_defaults(func=gen_c)

    parse_py = subpar.add_parser('js', help='JavaScript code generator')
    parse_py.add_argument('source', nargs='*', help='source directory')
    parse_py.set_defaults(func=gen_js)

    parse_py = subpar.add_parser('py', help='Python code generator')
    parse_py.add_argument('source', nargs='*', help='source directory')
    parse_py.set_defaults(func=gen_py)

    parse_ruby = subpar.add_parser('ruby', help='Ruby code generator')
    parse_ruby.add_argument('source', nargs='*', help='source directory')
    parse_ruby.set_defaults(func=gen_ruby)

    parse_java = subpar.add_parser('java', help='Java code generator')
    parse_java.add_argument('source', nargs='*', help='source directory')
    parse_java.set_defaults(func=gen_java)

    parse_swift = subpar.add_parser('swift', help='Swift code generator')
    parse_swift.add_argument('source', nargs='*', help='source directory')
    parse_swift.set_defaults(func=gen_swift)

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level)
    args.func(args)

