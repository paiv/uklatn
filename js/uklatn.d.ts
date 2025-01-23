/**
* Transliterates a string of Ukrainian Cyrillic to Latin script.
*
* @param {string} text - the text to transliterate
* @param {string} [table] - transliteration system, one of:
*  - "DSTU_9112_A": DSTU 9112:2021 System A
*  - "DSTU_9112_B": DSTU 9112:2021 System B
*  - "KMU_55": KMU 55:2010
* @returns {string} transliterated text
*/
export function encode(text: string, table?: string): string;
/**
* Re-transliterates a string of Ukrainian Latin to Cyrillic script.
*
* @param {string} text - the text to transliterate
* @param {string} [table] - transliteration system, one of:
*  - "DSTU_9112_A": DSTU 9112:2021 System A
*  - "DSTU_9112_B": DSTU 9112:2021 System B
* @returns {string} transliterated text
*/
export function decode(text: string, table?: string): string;
declare namespace _default {
    export { encode };
    export { decode };
}
export default _default;
