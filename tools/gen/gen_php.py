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
        return s.replace('$', '\\$')

    def _emit_testdata(kind, data, table):
        spl = '''\
        [
            &cyr,
            &lat
        ],
        '''
        for cyr, lat in data:
            yield template.format(spl, cyr=_j(cyr), lat=_j(lat)+'\n')

    def _emit_tests(kind, table):
        if kind[0] == 'c':
            yield f'$q = $this->tr->encode($cyr, {table!r});\n'
            yield '$this->assertSame($lat, $q);\n'
        else:
            yield f'$q = $this->tr->decode($lat, {table!r});\n'
            yield '$this->assertSame($cyr, $q);\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield f'$t = $this->tr->decode($lat, {table!r});\n'
                yield '$this->assertSame($cyr, $t);\n'
            else:
                yield f'$t = $this->tr->encode($cyr, {table!r});\n'
                yield '$this->assertSame($lat, $t);\n'

    def _emit_tests_default(kind):
        if kind[0] == 'c':
            yield '$q = $this->tr->encode($cyr);\n'
            yield '$this->assertSame($lat, $q);\n'
        else:
            yield '$q = $this->tr->decode($lat);\n'
            yield '$this->assertSame($cyr, $q);\n'
        if kind[-1] == 'r':
            if kind[0] == 'c':
                yield '$t = $this->tr->decode($lat);\n'
                yield '$this->assertSame($cyr, $t);\n'
            else:
                yield '$t = $this->tr->encode($cyr);\n'
                yield '$this->assertSame($lat, $t);\n'

    def _emit_testset(data, table):
        tpl = '''
        /**
         * @dataProvider data_&{table}_&kind
         */
        public function test_&{cname}_&kind(string $cyr, string $lat): void {
            &tests
        }
        '''
        for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
            xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
            if not xs: continue
            ctx = dict(table=table, cname=table, kind=kind)
            ctx['tests'] = _emit_tests(kind, table)
            yield template.format(tpl, ctx)
            if table == default_table:
                ctx['tests'] = _emit_tests_default(kind)
                yield template.format(tpl, ctx, cname=table + '_default')

        tpl = '''
        public function data_&{table}_&kind(): array {
            return [
            &data
            ];
        }
        '''
        for kind in ('c2lr', 'l2cr', 'c2l', 'l2c'):
            xs = [(cyr,lat) for k,cyr,lat in data if k == kind]
            if not xs: continue
            ctx = dict(table=table, kind=kind)
            ctx['data'] = _emit_testdata(kind, xs, table)
            yield template.format(tpl, ctx)

    def _test_cases():
        for fn in fns:
            logger.info(f'processing {fn!s}')
            name = fn.stem
            table = table_name(name)
            data = _parse_tests(fn)
            yield from _emit_testset(data, table)

    context = dict()
    context['test_cases'] = _test_cases

    tpl = r'''<?php declare(strict_types=1);

/* Note: generated code, do not edit. */

namespace Paiv\Tests;

use PHPUnit\Framework\TestCase;
use Paiv\UkrainianLatin;

final class UkrainianLatinTest extends TestCase {
    private $tr;

    /**
     * @before
     */
    public function setUp(): void {
        $this->tr = new UkrainianLatin();
    }
    &test_cases
}
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
    def _j(s):
        return json.dumps(s, ensure_ascii=False)
    def _srx(s):
        s = re.sub(r'\\u([0-9A-Fa-f]{4})', r'\\x{\1}', s)
        return f"'#{s}#u'"
    def _load_rules(data):
        return [s if isinstance(s, str) else [
            '|'.join(r['regex'] for r in s),
            [r['map'] for r in s]
        ] for s in data]

    def _emit_trdefs(rules):
        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                yield f'private $rx{sid};\n'
                yield f'private $tr{sid};\n'
                yield f'private $maps{sid};\n'

    def _emit_trrules(rules):
        tpl = '''\
        $this->rx&sid = &rx;
        $this->maps&sid = [
            &mappings
        ];
        $this->tr&sid = function(array $match): string {
            $s = array_shift($match);
            foreach($match as $i=>$v) {
                if ($v) {
                    $q = $this->maps&sid[$i][$v];
                    return is_null($q) ? $s : $q;
                }
            }
            return $s;
        };
        '''
        mpl = '''\
        array(
            &entries
        )'''

        def _ds(data):
            return ','.join(f'{_j(k)}=>{_j(v)}' for k,v in data.items()) + '\n'

        for sid, section in enumerate(rules):
            if not isinstance(section, str):
                rx, maps = section
                data = ',\n'.join(template.format(mpl, entries=_ds(d)) for d in maps) + '\n'
                yield template.format(tpl, sid=sid, rx=_srx(rx), mappings=data)

    def _emit_trbody(rules):
        for sid, section in enumerate(rules):
            if isinstance(section, str):
                if section not in ('NFC', 'NFD', 'NFKC', 'NFKD'):
                    raise Exception(f'invalid transform: {section!r}')
                yield f'$text = Normalizer::normalize($text, Normalizer::FORM_{section[2:]});\n'
            else:
                yield f'$text = preg_replace_callback($this->rx{sid}, $this->tr{sid}, $text);\n'

    def _emit_tr(cname, rules):
        context = dict(cname=cname)
        context['trdefs'] = _emit_trdefs(rules)
        context['trrules'] = _emit_trrules(rules)
        context['trbody'] = _emit_trbody(rules)
        tpl = '''

        final class &cname {
            &trdefs

            public function __construct() {
                &trrules
            }

            public function transform(string $text): string {
                &trbody
                return $text;
            }
        }
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
            for table, codec in tables.items():
                if codec[ar] is not None:
                    cname, rules = codec[ar]
                    yield _emit_tr(cname, rules)

    def _emit_tablemap():
        for table, codec in tables.items():
            enc,dec = codec
            enc = f'new {enc[0]}()' if enc else 'null'
            dec = f'new {dec[0]}()' if dec else 'null'
            yield f'{table!r} => [{enc}, {dec}],\n'

    tdoc = {
        'DSTU_9112_A': 'DSTU 9112:2021 System A',
        'DSTU_9112_B': 'DSTU 9112:2021 System B',
        'KMU_55': 'KMU 55:2010, not reversible',
    }
    def _emit_tenum():
        for i, t in enumerate(tables, 1):
            if (doc := tdoc.get(t, '')):
                doc = f'/** {doc} */\n'
            yield f'\n{doc}const {t} = {t!r};\n'

    context = dict()
    context['table_enum'] = _emit_tenum
    context['table_map'] = _emit_tablemap
    context['global_tables'] = _emit_tables
    context['default_table'] = default_table

    tpl = r'''<?php declare(strict_types=1);

/* Note: generated code, do not edit. */

namespace Paiv;

use Normalizer;


/**
* Ukrainian Cyrillic transliteration to and from Latin script.
*/
final class UkrainianLatin {
    private $tables;
    &{table_enum}

    /**
    * Transliterates a string of Ukrainian Cyrillic to Latin script.
    *
    * @param string $text the text to transliterate
    * @param string $table the transliteration system
    * @return string the transliterated text
    */
    public function encode(string $text, string $table = self::&{default_table}): string {
        $codec = $this->tables[$table];
        if ($codec) {
            $tr = $codec[0];
            if ($tr) {
                return $tr->transform($text);
            }
        }
        throw new Exception("invalid table $table");
    }

    /**
    * Re-transliterates a string of Ukrainian Latin to Cyrillic script.
    *
    * @param string $text the text to transliterate
    * @param string $table the transliteration system
    * @return string the transliterated text
    */
    public function decode(string $text, string $table = self::&{default_table}) {
        $codec = $this->tables[$table];
        if ($codec) {
            $tr = $codec[1];
            if ($tr) {
                return $tr->transform($text);
            }
        }
        throw new Exception("invalid table $table");
    }

    public function __construct() {
        $this->tables = array(
            &{table_map}
        );
    }
}
&{global_tables}
'''
    text = template.format(tpl, context)
    return text

