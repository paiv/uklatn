// Generated by gentests.py, do not edit.

use {uklatn::decode, uklatn::encode, uklatn::Table};

#[test]
fn dstu9112a_t1() {
    let cyr = "Україна, Хмельницький";
    let lat = "Ukraïna, Xmeljnycjkyj";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t1_default() {
    let cyr = "Україна, Хмельницький";
    let lat = "Ukraïna, Xmeljnycjkyj";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t2() {
    let cyr = "Щастям б’єш жук їх глицю в фон й ґедзь пріч.";
    let lat = "Ŝastjam b'ješ žuk ïx ğlycju v fon j gedzj prič.";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t2_default() {
    let cyr = "Щастям б’єш жук їх глицю в фон й ґедзь пріч.";
    let lat = "Ŝastjam b'ješ žuk ïx ğlycju v fon j gedzj prič.";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t3() {
    let cyr = "ь Ь ль льє льї лью лья лье льі льу льа льйо льо";
    let lat = "ĵ Ĵ lj ljje ljï ljju ljja lj'e lji lj'u lj'a ljjo ljo";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t3_default() {
    let cyr = "ь Ь ль льє льї лью лья лье льі льу льа льйо льо";
    let lat = "ĵ Ĵ lj ljje ljï ljju ljja lj'e lji lj'u lj'a ljjo ljo";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t4() {
    let cyr = "Єл Їл Юл Ял";
    let lat = "Jel Ïl Jul Jal";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t4_default() {
    let cyr = "Єл Їл Юл Ял";
    let lat = "Jel Ïl Jul Jal";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t5() {
    let cyr = "бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь";
    let lat = "bj vj ğj gj dj žj zj kj lj mj nj pj rj sj tj fj xj cj čj šj ŝj";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t5_default() {
    let cyr = "бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь";
    let lat = "bj vj ğj gj dj žj zj kj lj mj nj pj rj sj tj fj xj cj čj šj ŝj";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t6() {
    let cyr = "бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя";
    let lat = "bja vja ğja gja dja žja zja kja lja mja nja pja rja sja tja fja xja cja čja šja ŝja";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t6_default() {
    let cyr = "бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя";
    let lat = "bja vja ğja gja dja žja zja kja lja mja nja pja rja sja tja fja xja cja čja šja ŝja";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t7() {
    let cyr = "б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я";
    let lat = "b'ja v'ja ğ'ja g'ja d'ja ž'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja x'ja c'ja č'ja š'ja ŝ'ja";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t7_default() {
    let cyr = "б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я";
    let lat = "b'ja v'ja ğ'ja g'ja d'ja ž'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja x'ja c'ja č'ja š'ja ŝ'ja";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t8() {
    let cyr = "бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй";
    let lat =
        "b'j b'jo v'j ğ'j g'j d'j ž'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j x'j c'j č'j š'j ŝ'j";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t8_default() {
    let cyr = "бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй";
    let lat =
        "b'j b'jo v'j ğ'j g'j d'j ž'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j x'j c'j č'j š'j ŝ'j";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t9() {
    let cyr = "ня ньа н’я нь'н ньн";
    let lat = "nja nj'a n'ja nj'n njn";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t9_default() {
    let cyr = "ня ньа н’я нь'н ньн";
    let lat = "nja nj'a n'ja nj'n njn";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t10() {
    let cyr = "рос дыня эзёдынъ. бр кроў.";
    let lat = "ros dȳnja ēzödȳnǒ. br kroŭ.";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t10_default() {
    let cyr = "рос дыня эзёдынъ. бр кроў.";
    let lat = "ros dȳnja ēzödȳnǒ. br kroŭ.";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t11() {
    let cyr = "А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́";
    let lat = "Á á É é JÉ jé Ý ý Í í Ḯ ḯ Ó ó Ú ú JÚ jú JÁ já";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t11_default() {
    let cyr = "А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́";
    let lat = "Á á É é JÉ jé Ý ý Í í Ḯ ḯ Ó ó Ú ú JÚ jú JÁ já";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t12() {
    let cyr = "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с";
    let lat = "Jés sJés jés sjés Ḯs sḮs ḯs sḯs Jús sJús jús sjús Jás sJás jás sjás";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t12_default() {
    let cyr = "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с";
    let lat = "Jés sJés jés sjés Ḯs sḮs ḯs sḯs Jús sJús jús sjús Jás sJás jás sjás";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t13() {
    let cyr = "' ім’я 'жук' \"жук\" ' '";
    let lat = "' im'ja 'žuk' \"žuk\" ' '";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t13_default() {
    let cyr = "' ім’я 'жук' \"жук\" ' '";
    let lat = "' im'ja 'žuk' \"žuk\" ' '";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t14() {
    let cyr = "Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.";
    let lat = "Sonce svitytj majže bilym svitlom, odnak čerez syljniše rozsijuvannja i poğlynannja korotkoxvyljovoï častyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverxni našoï planety nabuvaje pevnoğo žovtoğo vidtinku. Jakŝo nebo jasne, to blakytnyj vidtinok rozsijanoğo svitla skladajetjsja z žovtuvatym prjamym sonjačnym svitlom i zağaljne osvitlennja ob'jektiv na Zemli staje bilym.";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t14_default() {
    let cyr = "Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.";
    let lat = "Sonce svitytj majže bilym svitlom, odnak čerez syljniše rozsijuvannja i poğlynannja korotkoxvyljovoï častyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverxni našoï planety nabuvaje pevnoğo žovtoğo vidtinku. Jakŝo nebo jasne, to blakytnyj vidtinok rozsijanoğo svitla skladajetjsja z žovtuvatym prjamym sonjačnym svitlom i zağaljne osvitlennja ob'jektiv na Zemli staje bilym.";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t22() {
    let cyr = "дуб!дуб\"дуб#дуб$дуб%дуб&дуб'дуб(дуб)дуб*дуб+дуб,дуб-дуб.дуб/дуб:дуб;дуб<дуб=дуб>дуб?дуб@дуб[дуб\\дуб]дуб^дуб_дуб`дуб{дуб|дуб}дуб~дуб";
    let lat = "dub!dub\"dub#dub$dub%dub&dub'dub(dub)dub*dub+dub,dub-dub.dub/dub:dub;dub<dub=dub>dub?dub@dub[dub\\dub]dub^dub_dub`dub{dub|dub}dub~dub";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t22_default() {
    let cyr = "дуб!дуб\"дуб#дуб$дуб%дуб&дуб'дуб(дуб)дуб*дуб+дуб,дуб-дуб.дуб/дуб:дуб;дуб<дуб=дуб>дуб?дуб@дуб[дуб\\дуб]дуб^дуб_дуб`дуб{дуб|дуб}дуб~дуб";
    let lat = "dub!dub\"dub#dub$dub%dub&dub'dub(dub)dub*dub+dub,dub-dub.dub/dub:dub;dub<dub=dub>dub?dub@dub[dub\\dub]dub^dub_dub`dub{dub|dub}dub~dub";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t23() {
    let cyr = "бод бод\tбод\nбод\rбод";
    let lat = "bod bod\tbod\nbod\rbod";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t23_default() {
    let cyr = "бод бод\tбод\nбод\rбод";
    let lat = "bod bod\tbod\nbod\rbod";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t24() {
    let cyr = "об😎нап😘неп😭нєп🧐нїп😍нюп😀няп";
    let lat = "ob😎nap😘nep😭njep🧐nïp😍njup😀njap";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112A);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t24_default() {
    let cyr = "об😎нап😘неп😭нєп🧐нїп😍нюп😀няп";
    let lat = "ob😎nap😘nep😭njep🧐nïp😍njup😀njap";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
    let t = decode(lat, Table::default());
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112a_t15() {
    let cyr = "в’я в'я";
    let lat = "v'ja v'ja";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
}

#[test]
fn dstu9112a_t15_default() {
    let cyr = "в’я в'я";
    let lat = "v'ja v'ja";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
}

#[test]
fn dstu9112a_t16() {
    let cyr = "Ї ї Й й Ё ё Ў ў";
    let lat = "Ï ï J j Ö ö Ŭ ŭ";
    let q = encode(cyr, Table::Dstu9112A);
    assert_eq!(q, lat);
}

#[test]
fn dstu9112a_t16_default() {
    let cyr = "Ї ї Й й Ё ё Ў ў";
    let lat = "Ï ï J j Ö ö Ŭ ŭ";
    let q = encode(cyr, Table::default());
    assert_eq!(q, lat);
}

#[test]
fn dstu9112a_t17() {
    let cyr = "я є ю";
    let lat = "jA jE jU";
    let q = decode(lat, Table::Dstu9112A);
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t17_default() {
    let cyr = "я є ю";
    let lat = "jA jE jU";
    let q = decode(lat, Table::default());
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t18() {
    let cyr = "Ї ї Ь ь Ч ч Г г Щ щ Ш ш Ж ж";
    let lat = "Ï ï Ĵ ĵ Č č Ğ ğ Ŝ ŝ Š š Ž ž";
    let q = decode(lat, Table::Dstu9112A);
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t18_default() {
    let cyr = "Ї ї Ь ь Ч ч Г г Щ щ Ш ш Ж ж";
    let lat = "Ï ï Ĵ ĵ Č č Ğ ğ Ŝ ŝ Š š Ž ž";
    let q = decode(lat, Table::default());
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t19() {
    let cyr = "Ё ё Ў ў Ъ ъ Ы ы Э э";
    let lat = "Ö ö Ŭ ŭ Ǒ ǒ Ȳ ȳ Ē ē";
    let q = decode(lat, Table::Dstu9112A);
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t19_default() {
    let cyr = "Ё ё Ў ў Ъ ъ Ы ы Э э";
    let lat = "Ö ö Ŭ ŭ Ǒ ǒ Ȳ ȳ Ē ē";
    let q = decode(lat, Table::default());
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t20() {
    let cyr = "А́ а́ Е́ е́ Є́ Є́ є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ Ю́ ю́ ю́ Я́ Я́ я́ я́";
    let lat = "Á á É é JÉ Jé jÉ jé Ý ý Í í Ḯ ḯ Ó ó Ú ú JÚ Jú jÚ jú JÁ Já jÁ já";
    let q = decode(lat, Table::Dstu9112A);
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t20_default() {
    let cyr = "А́ а́ Е́ е́ Є́ Є́ є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ Ю́ ю́ ю́ Я́ Я́ я́ я́";
    let lat = "Á á É é JÉ Jé jÉ jé Ý ý Í í Ḯ ḯ Ó ó Ú ú JÚ Jú jÚ jú JÁ Já jÁ já";
    let q = decode(lat, Table::default());
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t21() {
    let cyr = "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с";
    let lat = "Jés sJés jés sjés Ḯs sḮs ḯs sḯs Jús sJús jús sjús Jás sJás jás sjás";
    let q = decode(lat, Table::Dstu9112A);
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112a_t21_default() {
    let cyr = "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с";
    let lat = "Jés sJés jés sjés Ḯs sḮs ḯs sḯs Jús sJús jús sjús Jás sJás jás sjás";
    let q = decode(lat, Table::default());
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112b_t1() {
    let cyr = "Україна, Хмельницький";
    let lat = "Ukrajina, Khmeljnycjkyj";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t2() {
    let cyr = "Щастям б’єш жук їх глицю в фон й ґедзь пріч.";
    let lat = "Shchastjam b'jesh zhuk jikh ghlycju v fon j gedzj prich.";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t3() {
    let cyr = "ь Ь ль льє льї лью лья лье льі льу льа льйо льо";
    let lat = "hj Hj lj ljje ljji ljju ljja lj'e lj'i lj'u lj'a ljjo ljo";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t4() {
    let cyr = "Єл Їл Юл Ял";
    let lat = "Jel Jil Jul Jal";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t5() {
    let cyr = "бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь";
    let lat = "bj vj ghj gj dj zhj zj kj lj mj nj pj rj sj tj fj khj cj chj shj shchj";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t6() {
    let cyr = "бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя";
    let lat = "bja vja ghja gja dja zhja zja kja lja mja nja pja rja sja tja fja khja cja chja shja shchja";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t7() {
    let cyr = "б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я";
    let lat = "b'ja v'ja gh'ja g'ja d'ja zh'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja kh'ja c'ja ch'ja sh'ja shch'ja";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t8() {
    let cyr = "бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй";
    let lat = "b'j b'jo v'j gh'j g'j d'j zh'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j kh'j c'j ch'j sh'j shch'j";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t9() {
    let cyr = "ня ньа н’я нь'н ньн";
    let lat = "nja nj'a n'ja nj'n njn";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t10() {
    let cyr = "рос дыня эзёдынъ. бр кроў.";
    let lat = "ros dywnja ehwzjowdywnoh. br krouh.";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t11() {
    let cyr = "А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́";
    let lat = "Á á É é JÉ jé Ý ý Í í JÍ jí Ó ó Ú ú JÚ jú JÁ já";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t12() {
    let cyr = "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с";
    let lat = "Jés sJés jés sjés Jís sJís jís sjís Jús sJús jús sjús Jás sJás jás sjás";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t13() {
    let cyr = "' ім’я 'жук' \"жук\" ' '";
    let lat = "' im'ja 'zhuk' \"zhuk\" ' '";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t14() {
    let cyr = "Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.";
    let lat = "Sonce svitytj majzhe bilym svitlom, odnak cherez syljnishe rozsijuvannja i poghlynannja korotkokhvyljovoji chastyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverkhni nashoji planety nabuvaje pevnogho zhovtogho vidtinku. Jakshcho nebo jasne, to blakytnyj vidtinok rozsijanogho svitla skladajetjsja z zhovtuvatym prjamym sonjachnym svitlom i zaghaljne osvitlennja ob'jektiv na Zemli staje bilym.";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t20() {
    let cyr = "дуб!дуб\"дуб#дуб$дуб%дуб&дуб'дуб(дуб)дуб*дуб+дуб,дуб-дуб.дуб/дуб:дуб;дуб<дуб=дуб>дуб?дуб@дуб[дуб\\дуб]дуб^дуб_дуб`дуб{дуб|дуб}дуб~дуб";
    let lat = "dub!dub\"dub#dub$dub%dub&dub'dub(dub)dub*dub+dub,dub-dub.dub/dub:dub;dub<dub=dub>dub?dub@dub[dub\\dub]dub^dub_dub`dub{dub|dub}dub~dub";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t21() {
    let cyr = "бод бод\tбод\nбод\rбод";
    let lat = "bod bod\tbod\nbod\rbod";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t22() {
    let cyr = "об😎нап😘неп😭нєп🧐нїп😍нюп😀няп";
    let lat = "ob😎nap😘nep😭njep🧐njip😍njup😀njap";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
    let t = decode(lat, Table::Dstu9112B);
    assert_eq!(t, cyr);
}

#[test]
fn dstu9112b_t15() {
    let cyr = "в’я в'я";
    let lat = "v'ja v'ja";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
}

#[test]
fn dstu9112b_t16() {
    let cyr = "Ї ї Й й Ё ё Ў ў";
    let lat = "JI ji J j JOW jow UH uh";
    let q = encode(cyr, Table::Dstu9112B);
    assert_eq!(q, lat);
}

#[test]
fn dstu9112b_t17() {
    let cyr = "я ї є ю г ж х щ ш ч ь";
    let lat = "jA jI jE jU gH zH kH sHcH sH cH hJ";
    let q = decode(lat, Table::Dstu9112B);
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112b_t18() {
    let cyr = "А́ а́ Е́ е́ Є́ Є́ є́ є́ И́ и́ І́ і́ Ї́ Ї́ ї́ ї́ О́ о́ У́ у́ Ю́ Ю́ ю́ ю́ Я́ Я́ я́ я́";
    let lat = "Á á É é JÉ Jé jÉ jé Ý ý Í í JÍ Jí jÍ jí Ó ó Ú ú JÚ Jú jÚ jú JÁ Já jÁ já";
    let q = decode(lat, Table::Dstu9112B);
    assert_eq!(q, cyr);
}

#[test]
fn dstu9112b_t19() {
    let cyr = "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с";
    let lat = "Jés sJés jés sjés Jís sJís jís sjís Jús sJús jús sjús Jás sJás jás sjás";
    let q = decode(lat, Table::Dstu9112B);
    assert_eq!(q, cyr);
}

#[test]
fn kmu55_t1() {
    let cyr = "Україна, Хмельницький";
    let lat = "Ukraina, Khmelnytskyi";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t2() {
    let cyr = "Щастям б’єш жук їх глицю в фон й ґедзь пріч.";
    let lat = "Shchastiam biesh zhuk yikh hlytsiu v fon y gedz prich.";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t3() {
    let cyr = "згин зГ зГин Згин Зг ЗГ ЗГИН";
    let lat = "zghyn zGH zGhyn Zghyn Zgh ZGH ZGHYN";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t4() {
    let cyr = "ь Ь ль льє льї лью лья лье льі льу льа льйо льо";
    let lat = "  l lie li liu lia le li lu la lio lo";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t5() {
    let cyr = "Єл Їл Юл Ял";
    let lat = "Yel Yil Yul Yal";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t6() {
    let cyr = "бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь";
    let lat = "b v h g d zh z k l m n p r s t f kh ts ch sh shch";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t7() {
    let cyr = "бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя";
    let lat = "bia via hia gia dia zhia zia kia lia mia nia pia ria sia tia fia khia tsia chia shia shchia";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t8() {
    let cyr = "б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я";
    let lat = "bia via hia gia dia zhia zia kia lia mia nia pia ria sia tia fia khia tsia chia shia shchia";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t9() {
    let cyr = "бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй";
    let lat = "bi bio vi hi gi di zhi zi ki li mi ni pi ri si ti fi khi tsi chi shi shchi";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t10() {
    let cyr = "А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́";
    let lat = "Á á É é YÉ yé Ý ý Í í YÍ yí Ó ó Ú ú YÚ yú YÁ yá";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t11() {
    let cyr = "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с";
    let lat = "Yés sIés yés siés Yís sÍs yís sís Yús sIús yús siús Yás sIás yás siás";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t12() {
    let cyr = "' ім’я 'жук' \"жук\" ' '";
    let lat = "' imia 'zhuk' \"zhuk\" ' '";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t13() {
    let cyr = "Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.";
    let lat = "Sontse svityt maizhe bilym svitlom, odnak cherez sylnishe rozsiiuvannia i pohlynannia korotkokhvylovoi chastyny spektra atmosferoiu Zemli priame svitlo Sontsia bilia poverkhni nashoi planety nabuvaie pevnoho zhovtoho vidtinku. Yakshcho nebo yasne, to blakytnyi vidtinok rozsiianoho svitla skladaietsia z zhovtuvatym priamym soniachnym svitlom i zahalne osvitlennia obiektiv na Zemli staie bilym.";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t14() {
    let cyr = "в’я в'я";
    let lat = "via via";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t15() {
    let cyr = "дуб!дуб\"дуб#дуб$дуб%дуб&дуб'дуб(дуб)дуб*дуб+дуб,дуб-дуб.дуб/дуб:дуб;дуб<дуб=дуб>дуб?дуб@дуб[дуб\\дуб]дуб^дуб_дуб`дуб{дуб|дуб}дуб~дуб";
    let lat = "dub!dub\"dub#dub$dub%dub&dubdub(dub)dub*dub+dub,dub-dub.dub/dub:dub;dub<dub=dub>dub?dub@dub[dub\\dub]dub^dub_dub`dub{dub|dub}dub~dub";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t16() {
    let cyr = "бод бод\tбод\nбод\rбод";
    let lat = "bod bod\tbod\nbod\rbod";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
fn kmu55_t17() {
    let cyr = "об😎нап😘неп😭нєп🧐нїп😍нюп😀няп";
    let lat = "ob😎nap😘nep😭niep🧐nip😍niup😀niap";
    let q = encode(cyr, Table::Kmu55);
    assert_eq!(q, lat);
}

#[test]
#[should_panic]
fn kmu55_decode_panic() {
    decode(" ", Table::Kmu55);
}