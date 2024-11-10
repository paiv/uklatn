#!/usr/bin/env node
import path from 'node:path';
import * as uklatn from './uklatn.js';


const _Usage = '[-h] [-t TABLE] [-c] [-l] text [text ...]\n';

const _HelpPage = _Usage + `
arguments:
  text            text to transliterate
  -               read text from stdin

options:
  -h, --help            show this help message and exit
  -t, --table {DSTU_9112_A,DSTU_9112_B,KMU_55}
                        transliteration system (default: DSTU_9112_A)
  -l, --lat, --latin    convert to Latin script (default)
  -c, --cyr, --cyrillic convert to Cyrillic script
`;


function parse_args(argv) {
    const valid_tables = new Set(['DSTU_9112_A', 'DSTU_9112_B', 'KMU_55']);
    const args = {};
    args.executable = argv[0];
    args.script = argv[1];
    args.script_name = path.basename(args.script);
    let state = 0;
    for (let iarg = 2; iarg < argv.length; ++iarg) {
        const arg = argv[iarg];
        switch (state) {
            case 0:
                if (arg[0] === '-') {
                    if (arg === '-') {
                        if (args.text) {
                            args.text.push(arg);
                        }
                        else {
                            args.text = [arg];
                        }
                    }
                    else if (arg === '-h' || arg === '-help' || arg === '--help') {
                        args.print_help = true;
                        return args;
                    }
                    else if (arg === '-l' || arg === '--lat' || arg === '--latin') {
                        args.to_lat = true;
                    }
                    else if (arg === '-c' || arg === '--cyr' || arg === '--cyrillic') {
                        args.to_cyr = true;
                    }
                    else if (arg === '-t' || arg === '--table') {
                        state = 1;
                    }
                    else {
                        args.parse_error = `unrecognized arguments: ${arg}`;
                        return args;
                    }
                }
                else {
                    if (args.text) {
                        args.text.push(arg);
                    }
                    else {
                        args.text = [arg];
                    }
                }
                break;
            case 1:
                if (valid_tables.has(arg)) {
                    args.table_name = arg;
                    state = 0;
                }
                else {
                    const valid = [...valid_tables].map((s) => JSON.stringify(s));
                    args.parse_error = `invalid table name: ${arg} (choose from ${valid})`;
                    return args;
                }
                break;
        }
    }

    switch (state) {
        case 1:
            args.parse_error = `argument -t/--table expected table name`;
            return args;
    }

    if (!args.text || !args.text.length) {
        args.parse_error = 'missing required arguments: text';
        return args;
    }
    return args;
}


async function main(argv) {
    const args = parse_args(argv);

    if (args.parse_error) {
        process.stderr.write(`usage: ${args.script_name} ` + _Usage);
        process.stderr.write(`error: ${args.parse_error}\n`);
        return 1;
    }

    if (args.print_help) {
        process.stdout.write(`usage: ${args.script_name} ` + _HelpPage);
        return 0;
    }

    let tr = uklatn.encode;
    if (args.to_cyr && !args.to_lat) {
        tr = uklatn.decode;
    }

    if (args.text.length === 1 && args.text[0] === '-') {
        for await (const buf of process.stdin) {
            const text = buf.toString('utf-8');
            const s = tr(text, args.table_name);
            process.stdout.write(s);
        }
    }
    else {
        for (const [i, text] of args.text.entries()) {
            let s = tr(text, args.table_name);
            if (i) { s = ' ' + s; }
            process.stdout.write(s);
        }
        process.stdout.write('\n');
    }

    return 0;
}


process.exitCode = await main(process.argv);

