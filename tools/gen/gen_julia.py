import json
import logging
import re
from pathlib import Path
import template


logger = logging.getLogger(Path(__file__).stem)


def gen_tests(fns, default_table):
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
        s = json.dumps(s, ensure_ascii=False)
        s = re.sub(r'(?<!\\)\$', '\\$', s)
        return s

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'q = encode(cyr, :{table})\n'
            yield '@test q == lat\n'
        else:
            yield f'q = decode(lat, :{table})\n'
            yield '@test q == cyr\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'q = decode(lat, :{table})\n'
                yield '@test q == cyr\n'
            else:
                yield f'q = encode(cyr, :{table})\n'
                yield '@test q == lat\n'

    def _emit_tests_default(kind):
        if kind[0] == 'c':
            yield 'q = encode(cyr)\n'
            yield '@test q == lat\n'
        else:
            yield 'q = decode(lat)\n'
            yield '@test q == cyr\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield 'q = decode(lat)\n'
                yield '@test q == cyr\n'
            else:
                yield 'q = encode(cyr)\n'
                yield '@test q == lat\n'

    def _emit_testset(data, table):
        def _data(data):
            spl = '''\
            (
                &cyr,
                &lat,
            ),
            '''
            for cyr,lat in data:
                yield template.format(spl, cyr=_j(cyr), lat=_j(lat))

        def _tests():
            tpl = '''
            @testset "test &kind" begin
                data = [
                    &data
                ]

                for (cyr,lat) in data
                    &tests
                    &dtests
                end
            end
            '''
            ctx = dict(table=table)
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                ctx['kind'] = kind
                ctx['data'] = _data(xs)
                ctx['tests'] = _emit_tests(kind, table)
                ctx['dtests'] = iter('')
                if table == default_table:
                    ctx['dtests'] = _emit_tests_default(kind)
                yield template.format(tpl, ctx)

        tpl = '''

        @testset "&table" begin
            &tests
        end
        '''
        return template.format(tpl, table=table, tests=_tests)

    def _test_cases():
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            data = _parse_tests(fn)
            yield from _emit_testset(data, table)

    context = dict()
    context['test_cases'] = _test_cases

    tpl = '''\
    import Documenter: doctest
    import UkrainianLatin: encode, decode, UkrainianLatin
    using Test
    &{test_cases}


    @testset "exceptions" begin
        @test encode("") == ""
        @test decode("") == ""
        @test_throws ArgumentError encode("", :A)
        @test_throws ArgumentError decode("", :A)
    end


    @testset "doctest" begin
        doctest(UkrainianLatin; manual=false)
    end
    '''

    text = template.format(tpl, context)
    return text


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
            [r['regex'] for r in s],
            [r['map'] for r in s]
        ] for s in data]
    def _j(s):
        s = json.dumps(s, ensure_ascii=False)
        s = re.sub(r'(?<!\\)\$', '\\$', s)
        return s

    def _emit_maps(ls):
        def m(d):
            s = ','.join(f'({_j(k)},{_j(v)})' for k,v in d.items())
            return f'Dict([{s}])'
        s = ', '.join(map(m, ls))
        return f'[{s}]'

    def _emit_trrules(cname, rules):
        def _fdef():
            tpl = '''\
            rx&sid::NTuple{&n, Pair{Regex, Function}}
            '''
            for sid, section in enumerate(rules):
                if not isinstance(section, str):
                    rx, maps = section
                    n = len(maps)
                    yield template.format(tpl, sid=sid, n=n)

        def _finit():
            tpl = '''\
            rx&sid = &rx
            maps&sid = &maps
            tr&sid = Tuple(r => s -> get(m, s, s) for (r,m) in zip(rx&sid, maps&sid))
            '''
            for sid, section in enumerate(rules):
                if not isinstance(section, str):
                    rx, maps = section
                    rx = '[' + ', '.join(f'r"{s}"' for s in rx) + ']'
                    yield template.format(tpl, sid=sid, rx=rx,
                        maps=_emit_maps(maps))

        def _fnames():
            res = list()
            for sid, section in enumerate(rules):
                if not isinstance(section, str):
                    res.append(f'tr{sid}')
            return ', '.join(res)

        tpl = '''\
        &defs

        function &cname()
            &fields
            new(&names)
        end
        '''
        yield template.format(tpl, cname=cname, defs=_fdef,
            fields=_finit, names=_fnames)

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'text = normalize(text, :{section})\n'
            else:
                yield f'text = replace(text, table.rx{sid}...)\n'

    def _emit_tr(cname, rules):
        ctx = dict(cname=cname)
        ctx['trrules'] = _emit_trrules(cname, rules)
        ctx['trbody'] = _emit_trbody(rules)
        tpl = '''

        struct &cname
            &trrules
        end

        function _transform(table::&cname, text::AbstractString)
            &trbody
            return text
        end
        '''
        return template.format(tpl, ctx)

    tables = dict()
    for fn in fns:
        logger.info(f'processing {fn!s}')
        with fn.open() as fp:
            rules = json.load(fp)
            rules = _load_rules(rules)
        name = fn.stem
        table = table_name(name)
        cname = class_name(name)
        if table not in tables:
            tables[table] = [None, None]
        tables[table][_isdec(name)] = (cname, rules)

    def _emit_tables():
        for ar in [0,1]:
            for table, codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    yield _emit_tr(cname, rules)

        def _entries():
            for table, codec in tables.items():
                enc,dec = codec
                if enc:
                    yield f'const _encode_{table} = {enc[0]}()\n'
                if dec:
                    yield f'const _decode_{table} = {dec[0]}()\n'

        tpl = '''

        &entries
        '''
        yield template.format(tpl, entries=_entries)

    def _emit_match(names, prefix):
        for name in names:
            yield f'table == :{name} ? _transform({prefix}{name}, s) :\n'

    def _doc_tables(tables):
        inf = {
            'DSTU_9112_A': ', DSTU 9112:2021 System A',
            'DSTU_9112_B': ', DSTU 9112:2021 System B',
            'KMU_55': ', KMU 55:2010',
            }
        return '\n'.join((f' - `:{s}`{inf.get(s,s)}' +
            (' (default)' if s == default_table else ''))
            for s in tables)

    context = dict()
    context['doc_tables'] = _doc_tables(tables)
    context['all_tables'] = ', '.join(f'{s!r}' for s in tables)
    context['global_tables'] = _emit_tables
    context['default_table'] = default_table
    context['match_enc_table'] = _emit_match([k for k,(e,d) in tables.items() if e], '_encode_')
    context['match_dec_table'] = _emit_match([k for k,(e,d) in tables.items() if d], '_decode_')
    context['table_names'] = repr({k:i for i,k in enumerate(tables, 1)}) + '\n'

    tpl = '''
"""
Ukrainian Cyrillic transliteration to Latin script.

https://github.com/paiv/uklatn

Transliteration schemes:
&{doc_tables}
"""
module UkrainianLatin


import Unicode: normalize


export encode, decode


"""
    UkrainianLatin.encode(s::AbstractString)
    UkrainianLatin.encode(s::AbstractString, table::Symbol)

Transliterate the string `s` from Cyrlllic to Latin script.

# Examples

```jldoctest uklatn
julia> using UkrainianLatin

julia> UkrainianLatin.encode("Доброго вечора!")
"Dobroğo večora!"
```

To set the transliteration scheme:

```jldoctest uklatn
julia> UkrainianLatin.encode("Щастя", :KMU_55)
"Shchastia"
```
"""
function encode end


encode(s::AbstractString) = encode(s, :&default_table)


function encode(s::AbstractString, table::Symbol)
    return (
        &match_enc_table
        throw(ArgumentError("invalid table :$table"))
    )
end


"""
    UkrainianLatin.decode(s::AbstractString)
    UkrainianLatin.decode(s::AbstractString, table::Symbol)

Re-transliterate the string `s` from Latin script back to Cyrillic.

# Examples

```jldoctest uklatn
julia> using UkrainianLatin

julia> UkrainianLatin.decode("Paljanycja")
"Паляниця"
```

To set the transliteration scheme:

```jldoctest uklatn
julia> UkrainianLatin.decode("Shchastja", :DSTU_9112_B)
"Щастя"
```
"""
function decode end


decode(s::AbstractString) = decode(s, :&default_table)


function decode(s::AbstractString, table::Symbol)
    return (
        &match_dec_table
        throw(ArgumentError("invalid table :$table"))
    )
end
&{global_tables}

end
'''
    text = template.format(tpl, context)
    return text

