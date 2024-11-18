#!/usr/bin/env python
import json
import logging
import re
from pathlib import Path
import template


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

    tpl = '''
static const struct _uklatn_test _&{name}_data[] = {
    &entries
};
'''
    epl = '''\
{
    u&{cyr},
    u&{lat},
    UklatnTable_&{table},
},
'''
    def _data(name, data):
        ctx = dict(name=name)
        def _ds():
            for cyr, lat, table in data:
                yield template.format(epl, ctx, table=table, cyr=_j(cyr), lat=_j(lat))
        return template.format(tpl, ctx, entries=_ds)

    def _test_data():
        yield _data('cyr2lat2cyr', c2lr)
        yield _data('lat2cyr2lat', l2cr)
        yield _data('cyr2lat', c2l)
        yield _data('lat2cyr', l2c)

    text = template.format('&data', data=_test_data)
    return text


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

    tables = list()

    for fn in fns:
        logger.info(f'processing {fn!s}')
        name = fn.stem
        tname = table_name(name)
        vname = table_varname(name)
        rname = var_name(name)
        text = fn.read_text()
        tables.append((tname, vname, rname, text))

    def _data():
        for tname, vname, rname, text in tables:
            ctx = dict(tname=tname, vname=vname, rname=rname)
            data = ''.join(json.dumps(line, ensure_ascii=False) + '\n'
                for line in text.splitlines() if line)
            yield template.format(dpl, ctx, data=data)

    def _regs():
        for tname, vname, rname, text in tables:
            yield f'err = _uklatn_register_table({vname}, {rname});\n'
            yield 'if (err != 0) { return err; }\n'

    dpl = '''\
static const UChar &vname[] = u"&tname";

static char &rname[] =
    &data
    ;

'''

    tpl = '''\
&data
static int
_uklatn_register_tables(void) {
    int err = 0;
    &regs
    return 0;
}
'''
    text = template.format(tpl, data=_data, regs=_regs)
    return text

