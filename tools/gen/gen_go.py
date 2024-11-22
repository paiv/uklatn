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
        return re.sub(r'test_', '', s, flags=re.I).replace('-', '_')
    def class_name(s):
        return re.sub(r'test|_', '', s.title(), flags=re.I)
    def _j(s):
        return json.dumps(s, ensure_ascii=False)

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'enc := EncodeString(cyrlat[0], {table})\n'
            yield 'assertEqual(t, cyrlat[1], enc, "\\n"+cyrlat[0])\n'
        else:
            yield f'dec := DecodeString(cyrlat[1], {table})\n'
            yield 'assertEqual(t, cyrlat[0], dec, "\\n"+cyrlat[1])\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'dec := DecodeString(cyrlat[1], {table})\n'
                yield 'assertEqual(t, cyrlat[0], dec, "\\n"+cyrlat[1])\n'
            else:
                yield f'enc := EncodeString(cyrlat[0], {table})\n'
                yield 'assertEqual(t, cyrlat[1], enc, "\\n"+cyrlat[0])\n'

    def _emit_testset(data, table, cname):
        def _dump(data):
            tpl = '''\
            {
                &cyr,
                &lat,
            },
            '''
            for cyr, lat in data:
                yield template.format(tpl, cyr=_j(cyr), lat=_j(lat))

        def _data():
            tpl = '''\
            data_&kind := [...][2]string {
                &entries
            }
            '''
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                yield template.format(tpl, kind=kind, entries=_dump(xs))

        def _test_kind(kind, data, table):
            tpl = '''
            for _, cyrlat := range data_&kind {
                &tests
            }
            '''
            ctx = dict(kind=kind, table=table)
            ctx['tests'] = _emit_tests(kind, table)
            return template.format(tpl, ctx)

        def _tests():
            for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
                xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
                if not xs: continue
                yield _test_kind(kind, xs, table)
                if table == default_table:
                    yield _test_kind(kind, xs, 'DefaultTable')

        tpl = '''

        func Test&{cname}(t *testing.T) {
            &data
            &tests
        }
        '''
        yield template.format(tpl, cname=cname, data=_data, tests=_tests)

        if data and all(k == 'c2l' for k,_,_ in data):
            tpl = '''
            func Test&{cname}DecodePanic(t *testing.T) {
                defer func() { _ = recover() }()
                DecodeString("lat", &table)
                t.Errorf("DecodeString did not panic")
            }
            '''
            yield template.format(tpl, table=table, cname=cname)

        if any(k in ('c2lr','l2cr','l2c') for k,_,_ in data):
            tpl = r'''

            func Fuzz&{cname}Decode(f *testing.F) {
                for _, seed := range [...]string { "", "A", "z"} {
                    f.Add(seed)
                }
                f.Fuzz(func(t *testing.T, in string) {
                    if !utf8.ValidString(in) {
                        t.Skip()
                    }
                    DecodeString(in, &table)
                })
            }
            '''
            yield template.format(tpl, table=table, cname=cname)

        if any(k in ('c2lr','l2cr','c2l') for k,_,_ in data):
            tpl = r'''

            func Fuzz&{cname}Encode(f *testing.F) {
                for _, seed := range [...]string { "", "А", "я"} {
                    f.Add(seed)
                }
                f.Fuzz(func(t *testing.T, in string) {
                    if !utf8.ValidString(in) {
                        t.Skip()
                    }
                    EncodeString(in, &table)
                })
            }
            '''
            yield template.format(tpl, table=table, cname=cname)

    def _test_cases():
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            cname = class_name(name)
            data = _parse_tests(fn)
            yield from _emit_testset(data, table, cname)

    context = dict()
    context['test_cases'] = _test_cases

    tpl = r'''package uklatn

    import (
        "fmt"
        "testing"
        "unicode/utf8"
    )

    func ExampleEncodeString() {
        s := EncodeString("Добрий вечір!", DSTU_9112_A)
        fmt.Println(s)
        // Output:
        // Dobryj večir!
    }

    func ExampleDecodeString() {
        s := DecodeString("Paljanycja", DSTU_9112_A)
        fmt.Println(s)
        // Output:
        // Паляниця
    }

    func assertEqual(t *testing.T, actual string, expect string, message string) {
        if actual != expect {
            t.Fatalf("%s\nexpect: %s\nactual: %s", message, expect, actual)
        }
    }
    &{test_cases}
    '''
    text = template.format(tpl, context)
    return text


def gen_transforms(fns, default_table=None):
    def table_name(s):
        s, = re.findall(r'uk_Latn_(.*?)(?:-uk)?\s*$', s, flags=re.I)
        return s.replace('-', '_')
    def class_name(s):
        return 'table_' + s.replace('-', '_')
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def _isdec(s):
        return s.startswith('uk_Latn_')
    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s),
            [r['map'] for r in s]
        ] for s in data]

    def _emit_trdefs(rules):
        tpl = '''\
        rx&sid := regexp2.MustCompile(`&rx`, regexp2.Compiled | regexp2.Unicode)
        maps&sid := [...]map[string]string {
            &mappings
        }
        tr&sid := func(i int, s string) string {
    		if v,t := maps&sid[i-1][s]; t {
                return v
            }
            return s
        }
        '''
        mpl = '{&entries},'

        def _ds(data):
            return ','.join(f'{_j(k)}:{_j(v)}' for k,v in data.items()) if data else ':'

        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                data = '\n'.join(template.format(mpl, entries=_ds(d)) for d in maps) + '\n'
                yield template.format(tpl, sid=sid, rx=rx, mappings=data)

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'text = norm.{section}.String(text)\n'
            else:
                yield f'text = replaceAllStringSubmatchFunc(rx{sid}, text, tr{sid})\n'

    def _emit_tr(cname, rules):
        context = dict(cname=cname)
        context['trdefs'] = _emit_trdefs(rules)
        context['trbody'] = _emit_trbody(rules)
        tpl = '''
        var &cname = func() func(string) string {
            &trdefs

            return func(text string) string {
                &trbody
                return text
            }
        }()
        '''
        return template.format(tpl, context)

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
            for table,codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    yield _emit_tr(cname, rules)

        def _entries():
            for table,codec in tables.items():
                enc,dec = codec
                enc = f'{enc[0]}' if enc else 'nil'
                dec = f'{dec[0]}' if dec else 'nil'
                yield f'{{{enc}, {dec}}},\n'

        tpl = '''
        var tables = [...][2]func(string) string {
            {nil, nil},
            &entries
        }
        '''
        yield template.format(tpl, entries=_entries)

    tdoc = {
        'DSTU_9112_A': 'DSTU 9112:2021 System A',
        'DSTU_9112_B': 'DSTU 9112:2021 System B',
        'KMU_55': 'KMU 55:2010, not reversible',
    }
    def _emit_tenum():
        for i, t in enumerate(tables, 1):
            if (doc := tdoc.get(t, '')):
                doc = f' // {doc}'
            yield f'{t}{doc}\n'

    context = dict()
    context['tables_enum'] = _emit_tenum
    context['global_tables'] = _emit_tables
    context['default_table'] = default_table

    tpl = r'''// Package uklatn implements transliteration
// of Ukrainian Cyrillic to and from Latin script.
//
// Supported transliteration schemes:
//   - [DSTU 9112:2021]
//   - [KMU 55:2010] (to Latin script only)
//
// [DSTU 9112:2021]:  https://uk.wikipedia.org/wiki/ДСТУ_9112:2021
// [KMU 55:2010]: https://zakon.rada.gov.ua/laws/show/55-2010-п
package uklatn

import (
    "golang.org/x/text/unicode/norm"
    "github.com/dlclark/regexp2"
)

type Table int

const (
    DefaultTable Table = iota
    &tables_enum
)


// EncodeString transliterates a string of Ukrainian Cyrillic to Latin script,
// given the transliteration table.
func EncodeString(s string, t Table) string {
	if t == DefaultTable {
		t = &{default_table}
	}
	tr := tables[t][0]
	if tr != nil {
		return tr(s)
	}
	panic(t)
}


// DecodeString re-transliterates a string of Ukrainian Latin to Cyrillic script,
// given the transliteration table.
func DecodeString(s string, t Table) string {
	if t == DefaultTable {
		t = &{default_table}
	}
	if tr := tables[t][1]; tr != nil {
		return tr(s)
	}
	panic(t)
}

func replaceAllStringSubmatchFunc(re *regexp2.Regexp, src string, repl func(int, string) string) string {
    res, err := re.ReplaceFunc(src, func(m regexp2.Match) string {
        for i := m.GroupCount() - 1; i > 0; i -= 1 {
            g := m.Groups()[i]
            if g.Capture.Length > 0 {
                s := g.Capture.String()
                return repl(i, s)
            }
        }
        return m.Group.Capture.String()
    }, -1, -1)
    if err == nil {
        return res
    }
    panic(err)
}
&{global_tables}
'''
    text = template.format(tpl, context)
    return text

