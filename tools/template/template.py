import io
import logging
import re
import sys
import textwrap
from pathlib import Path


logger = logging.getLogger(Path(__file__).stem)


def format(text, context=None, **kwargs):
    context = (context or dict()) | kwargs
    with io.StringIO() as so:
        print(text, context, file=so)
        return so.getvalue()


def print(text, context=None, file=None):
    if context is None:
        context = dict()
    if file is None:
        file = sys.stdout
    write = file.buffer.write if hasattr(file, 'buffer') else file.write
    parser = _Parser()

    def _s(v): return v if isinstance(v, str) else str(v)

    def _resolve(name):
        if (value := context.get(name)) is None:
            yield '&' + name
        else:
            if callable(value):
                value = value()
            if hasattr(value, '__next__'):
                for v in value:
                    yield _s(v)
            else:
                yield _s(value)

    def _expand(name):
        indent = parser.indent
        for i,s in enumerate(_resolve(name)):
            yield textwrap.indent(s, indent) if indent else s

    for tok in parser.tokenize(text):
        match tok.kind:
            case _Token.CHR:
                write(tok.value)
            case _Token.REF:
                for s in _expand(tok.name):
                    write(s)


class _Token:
    CHR = 1
    REF = 2

    def __init__(self, kind, value=None, name=None):
        self.kind = kind
        self.value = value
        self.name = name


class _Parser:
    def __init__(self):
        self.indent = ''

    def tokenize(self, text):
        name = None
        state = 0
        col = 0
        line = 1
        for c in text:
            if c == '\n':
                line += 1
                col = 0
            else:
                col += 1

            consumed = False
            while not consumed:
                consumed = True

                match state:

                    case 0:
                        match c:
                            case '\\':
                                state = 1
                            case '&':
                                name = ''
                                state = 2
                            case _ if col == 1 and c in ' \t':
                                self.indent = c
                                state = 9
                            case _:
                                yield _Token(_Token.CHR, value=c)

                    case 1:
                        match c:
                            case '&':
                                yield _Token(_Token.CHR, value='&')
                            case _:
                                yield _Token(_Token.CHR, value='\\')
                                consumed = False
                        state = 0

                    case 2:
                        match c:
                            case '{':
                                state = 4
                            case _ if c.isalpha() or c == '_':
                                name += c
                                state = 3
                            case _:
                                if self.indent:
                                    yield _Token(_Token.CHR, value=self.indent)
                                    self.indent = ''
                                yield _Token(_Token.CHR, value='&')
                                consumed = False
                                state = 0

                    case 3:
                        match c:
                            case _ if c.isalnum() or c == '_':
                                name += c
                            case '\n':
                                yield _Token(_Token.REF, name=name)
                                self.indent = ''
                                name = None
                                state = 0
                            case _:
                                yield _Token(_Token.REF, name=name)
                                name = None
                                consumed = False
                                state = 0

                    case 4:
                        match c:
                            case _ if c.isalpha() or c == '_':
                                name += c
                                state = 5
                            case _:
                                if self.indent:
                                    yield _Token(_Token.CHR, value=self.indent)
                                    self.indent = ''
                                yield _Token(_Token.CHR, value='&{')
                                consumed = False
                                state = 0

                    case 5:
                        match c:
                            case '}':
                                state = 6
                            case _:
                                name += c

                    case 6:
                        match c:
                            case '\n':
                                yield _Token(_Token.REF, name=name)
                                self.indent = ''
                                name = None
                                state = 0
                            case _:
                                yield _Token(_Token.REF, name=name)
                                name = None
                                consumed = False
                                state = 0

                    case 9:
                        match c:
                            case _ if c in ' \t':
                                self.indent += c
                            case '&':
                                consumed = False
                                state = 0
                            case _:
                                yield _Token(_Token.CHR, value=self.indent)
                                self.indent = ''
                                consumed = False
                                state = 0
        else:
            match state:
                case 0:
                    pass
                case 1:
                    yield _Token(_Token.CHR, value='\\')
                case 2:
                    yield _Token(_Token.CHR, value='&')
                case 3:
                    yield _Token(_Token.REF, name=name)
                case 4:
                    yield _Token(_Token.CHR, value='&{')
                case 5:
                    yield _Token(_Token.CHR, value='&{'+name)
                case 6:
                    yield _Token(_Token.REF, name=name)
                case 9:
                    yield _Token(_Token.CHR, value=self.indent)
                case _:
                    raise Exception(f'state {state}')

