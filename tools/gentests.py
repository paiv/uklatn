#!/usr/bin/env python
import logging
from pathlib import Path


logger = logging.getLogger(Path(__file__).stem)


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
        text = generator(fns)
        yield text


def gen_c(args):
    logger.info('C generator start')
    from gen import gen_c

    source = _basegen(args, 'src/tests', 'test*.json', gen_c.gen_tests)
    for text in source:
        print(text, end='')

    logger.info('C generator end')


def gen_java(args):
    logger.info('Java generator start')
    from gen import gen_java

    source = _basegen(args, 'src/tests', 'test*.json', gen_java.gen_tests)
    for text in source:
        print(text, end='')

    logger.info('Java generator end')


def gen_js(args):
    logger.info('JS generator start')
    from gen import gen_js

    source = _basegen(args, 'src/tests', 'test*.json', gen_js.gen_tests)
    for text in source:
        print(text, end='')

    logger.info('JS generator end')


def gen_py(args):
    logger.info('PY generator start')
    from gen import gen_py

    source = _basegen(args, 'src/tests', 'test*.json', gen_py.gen_tests)
    for text in source:
        print(text, end='')

    logger.info('PY generator end')


def gen_csharp(args):
    logger.info('C# generator start')
    from gen import gen_csharp

    source = _basegen(args, 'src/tests', 'test*.json', gen_csharp.gen_tests)
    for text in source:
        print(text, end='')

    logger.info('C# generator end')


def gen_go(args):
    logger.info('Go generator start')
    from gen import gen_go

    source = _basegen(args, 'src/tests', 'test*.json', gen_go.gen_tests)
    for text in source:
        print(text, end='')

    logger.info('Go generator end')


def gen_ruby(args):
    logger.info('Ruby generator start')
    from gen import gen_ruby

    source = _basegen(args, 'src/tests', 'test*.json', gen_ruby.gen_tests)
    for text in source:
        print(text, end='')

    logger.info('Ruby generator end')


def gen_swift(args):
    logger.info('Swift generator start')
    from gen import gen_swift

    source = _basegen(args, 'src/tests', 'test*.json', gen_swift.gen_tests)
    for text in source:
        print(text, end='')

    logger.info('Swift generator end')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate test code for the transform tables.')
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

    parse_java = subpar.add_parser('java', help='Java code generator')
    parse_java.add_argument('source', nargs='*', help='source directory')
    parse_java.set_defaults(func=gen_java)

    parse_csharp = subpar.add_parser('csharp', help='C# code generator')
    parse_csharp.add_argument('source', nargs='*', help='source directory')
    parse_csharp.set_defaults(func=gen_csharp)

    parse_go = subpar.add_parser('go', help='Go code generator')
    parse_go.add_argument('source', nargs='*', help='source directory')
    parse_go.set_defaults(func=gen_go)

    parse_ruby = subpar.add_parser('ruby', help='Ruby code generator')
    parse_ruby.add_argument('source', nargs='*', help='source directory')
    parse_ruby.set_defaults(func=gen_ruby)

    parse_swift = subpar.add_parser('swift', help='Swfit code generator')
    parse_swift.add_argument('source', nargs='*', help='source directory')
    parse_swift.set_defaults(func=gen_swift)

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level)
    args.func(args)

