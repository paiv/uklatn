import io
import sys
import textwrap


__all__ = ['format', 'print']


def format(text, context=None, **kwargs):
    """
    Formats text template, substituting `&`-variables:
        >>> import template
        >>> template.format('&v &{v}', v='hello')
        'hello hello'
    """
    context = (context or dict()) | kwargs
    with io.StringIO() as so:
        print(text, context, file=so)
        return so.getvalue()


def print(text, context=None, file=None):
    if context is None:
        context = dict()
    if file is None:
        file = sys.stdout
    if '\n' in text:
        text = textwrap.dedent(text)

    write = file.buffer.write if hasattr(file, 'buffer') else file.write
    parser = _Parser()

    def _s(v): return v if isinstance(v, str) else str(v)

    def _resolve(tok):
        if (value := context.get(tok.name)) is not None:
            if callable(value):
                value = value()
            if hasattr(value, '__next__'):
                for v in value:
                    yield _s(v)
            else:
                yield _s(value)
        elif tok.name in context:
            yield ''
        else:
            yield tok.value

    def _expand(tok, indent):
        for i,s in enumerate(_resolve(tok)):
            yield textwrap.indent(s, indent) if indent else s

    indent = None
    last_expand_count = None
    last_expand_nl = False
    for tok in parser.tokenize(text):
        match tok.kind:
            case _Token.CHR:
                if indent:
                    write(indent)
                    indent = None
                if tok.value == '\n':
                    if last_expand_nl or last_expand_count == 0:
                        pass
                    else:
                        write(tok.value)
                else:
                    write(tok.value)
                last_expand_count = None
                last_expand_nl = False
            case _Token.NDT:
                indent = tok.value
            case _Token.REF:
                last_expand_count = 0
                for last_expand_count, s in enumerate(_expand(tok, indent), 1):
                    write(s)
                    last_expand_nl = bool(s) and s[-1] == '\n'
                indent = None


class _Token:
    CHR = 'CHR'
    NDT = 'NDT'
    REF = 'REF'

    def __init__(self, kind, value=None, name=None):
        self.kind = kind
        self.value = value
        self.name = name

    def __repr__(self):
        return f'Token({self.kind} {self.name!r}, {self.value!r})'


class _Parser:

    def tokenize(self, text):
        name = None
        indent = None
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
                                indent = c
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
                                yield _Token(_Token.CHR, value='&')
                                consumed = False
                                state = 0

                    case 3:
                        match c:
                            case _ if c.isalnum() or c == '_':
                                name += c
                            case _:
                                yield _Token(_Token.REF, name=name, value=f'&{name}')
                                name = None
                                consumed = False
                                state = 0

                    case 4:
                        match c:
                            case _ if c.isalpha() or c == '_':
                                name += c
                                state = 5
                            case _:
                                yield _Token(_Token.CHR, value='&{')
                                consumed = False
                                state = 0

                    case 5:
                        match c:
                            case '}':
                                yield _Token(_Token.REF, name=name, value=f'&{{{name}}}')
                                name = None
                                state = 0
                            case _ if c.isalpha() or c == '_':
                                name += c
                            case _:
                                yield _Token(_Token.CHR, value='&{'+name)
                                state = 0

                    case 9:
                        match c:
                            case _ if c in ' \t':
                                indent += c
                            case _:
                                yield _Token(_Token.NDT, value=indent)
                                indent = None
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
                    yield _Token(_Token.REF, name=name, value=f'&{name}')
                case 4:
                    yield _Token(_Token.CHR, value='&{')
                case 5:
                    yield _Token(_Token.CHR, value='&{'+name)
                case 9:
                    yield _Token(_Token.NDT, value=indent)
                case _:
                    raise Exception(f'state {state}')

