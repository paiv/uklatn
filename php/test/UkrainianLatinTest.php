<?php declare(strict_types=1);

/* Note: generated code, do not edit. */

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

    /**
     * @dataProvider data_DSTU_9112_A_c2lr
     */
    public function test_DSTU_9112_A_c2lr(string $cyr, string $lat): void {
        $q = $this->tr->encode($cyr, 'DSTU_9112_A');
        $this->assertSame($lat, $q);
        $t = $this->tr->decode($lat, 'DSTU_9112_A');
        $this->assertSame($cyr, $t);
    }

    /**
     * @dataProvider data_DSTU_9112_A_c2lr
     */
    public function test_DSTU_9112_A_default_c2lr(string $cyr, string $lat): void {
        $q = $this->tr->encode($cyr);
        $this->assertSame($lat, $q);
        $t = $this->tr->decode($lat);
        $this->assertSame($cyr, $t);
    }

    /**
     * @dataProvider data_DSTU_9112_A_c2l
     */
    public function test_DSTU_9112_A_c2l(string $cyr, string $lat): void {
        $q = $this->tr->encode($cyr, 'DSTU_9112_A');
        $this->assertSame($lat, $q);
    }

    /**
     * @dataProvider data_DSTU_9112_A_c2l
     */
    public function test_DSTU_9112_A_default_c2l(string $cyr, string $lat): void {
        $q = $this->tr->encode($cyr);
        $this->assertSame($lat, $q);
    }

    /**
     * @dataProvider data_DSTU_9112_A_l2c
     */
    public function test_DSTU_9112_A_l2c(string $cyr, string $lat): void {
        $q = $this->tr->decode($lat, 'DSTU_9112_A');
        $this->assertSame($cyr, $q);
    }

    /**
     * @dataProvider data_DSTU_9112_A_l2c
     */
    public function test_DSTU_9112_A_default_l2c(string $cyr, string $lat): void {
        $q = $this->tr->decode($lat);
        $this->assertSame($cyr, $q);
    }

    public function data_DSTU_9112_A_c2lr(): array {
        return [
        [
            "Україна, Хмельницький",
            "Ukraïna, Xmeljnycjkyj"
        ],
        [
            "Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
            "Ŝastjam b'ješ žuk ïx ğlycju v fon j gedzj prič."
        ],
        [
            "ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
            "ĵ Ĵ lj ljje ljï ljju ljja lj'e lji lj'u lj'a ljjo ljo"
        ],
        [
            "Єл Їл Юл Ял",
            "Jel Ïl Jul Jal"
        ],
        [
            "бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
            "bj vj ğj gj dj žj zj kj lj mj nj pj rj sj tj fj xj cj čj šj ŝj"
        ],
        [
            "бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
            "bja vja ğja gja dja žja zja kja lja mja nja pja rja sja tja fja xja cja čja šja ŝja"
        ],
        [
            "б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
            "b'ja v'ja ğ'ja g'ja d'ja ž'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja x'ja c'ja č'ja š'ja ŝ'ja"
        ],
        [
            "бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
            "b'j b'jo v'j ğ'j g'j d'j ž'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j x'j c'j č'j š'j ŝ'j"
        ],
        [
            "ня ньа н’я нь'н ньн",
            "nja nj'a n'ja nj'n njn"
        ],
        [
            "рос дыня эзёдынъ. бр кроў.",
            "ros dȳnja ēzödȳnǒ. br kroŭ."
        ],
        [
            "А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́",
            "Á á É é JÉ jé Ý ý Í í Ḯ ḯ Ó ó Ú ú JÚ jú JÁ já"
        ],
        [
            "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            "Jés sJés jés sjés Ḯs sḮs ḯs sḯs Jús sJús jús sjús Jás sJás jás sjás"
        ],
        [
            "' ім’я 'жук' \"жук\" ' '",
            "' im'ja 'žuk' \"žuk\" ' '"
        ],
        [
            "Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.",
            "Sonce svitytj majže bilym svitlom, odnak čerez syljniše rozsijuvannja i poğlynannja korotkoxvyljovoï častyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverxni našoï planety nabuvaje pevnoğo žovtoğo vidtinku. Jakŝo nebo jasne, to blakytnyj vidtinok rozsijanoğo svitla skladajetjsja z žovtuvatym prjamym sonjačnym svitlom i zağaljne osvitlennja ob'jektiv na Zemli staje bilym."
        ],
        [
            "дуб!дуб\"дуб#дуб\$дуб%дуб&дуб'дуб(дуб)дуб*дуб+дуб,дуб-дуб.дуб/дуб:дуб;дуб<дуб=дуб>дуб?дуб@дуб[дуб\\дуб]дуб^дуб_дуб`дуб{дуб|дуб}дуб~дуб",
            "dub!dub\"dub#dub\$dub%dub&dub'dub(dub)dub*dub+dub,dub-dub.dub/dub:dub;dub<dub=dub>dub?dub@dub[dub\\dub]dub^dub_dub`dub{dub|dub}dub~dub"
        ],
        [
            "бод бод\tбод\nбод\rбод",
            "bod bod\tbod\nbod\rbod"
        ],
        [
            "об😎нап😘неп😭нєп🧐нїп😍нюп😀няп",
            "ob😎nap😘nep😭njep🧐nïp😍njup😀njap"
        ],
        ];
    }

    public function data_DSTU_9112_A_c2l(): array {
        return [
        [
            "в’я в'я",
            "v'ja v'ja"
        ],
        [
            "Ї ї Й й Ё ё Ў ў",
            "Ï ï J j Ö ö Ŭ ŭ"
        ],
        ];
    }

    public function data_DSTU_9112_A_l2c(): array {
        return [
        [
            "я є ю",
            "jA jE jU"
        ],
        [
            "Ї ї Ь ь Ч ч Г г Щ щ Ш ш Ж ж",
            "Ï ï Ĵ ĵ Č č Ğ ğ Ŝ ŝ Š š Ž ž"
        ],
        [
            "Ё ё Ў ў Ъ ъ Ы ы Э э",
            "Ö ö Ŭ ŭ Ǒ ǒ Ȳ ȳ Ē ē"
        ],
        [
            "А́ а́ Е́ е́ Є́ Є́ є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ Ю́ ю́ ю́ Я́ Я́ я́ я́",
            "Á á É é JÉ Jé jÉ jé Ý ý Í í Ḯ ḯ Ó ó Ú ú JÚ Jú jÚ jú JÁ Já jÁ já"
        ],
        [
            "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            "Jés sJés jés sjés Ḯs sḮs ḯs sḯs Jús sJús jús sjús Jás sJás jás sjás"
        ],
        ];
    }

    /**
     * @dataProvider data_DSTU_9112_B_c2lr
     */
    public function test_DSTU_9112_B_c2lr(string $cyr, string $lat): void {
        $q = $this->tr->encode($cyr, 'DSTU_9112_B');
        $this->assertSame($lat, $q);
        $t = $this->tr->decode($lat, 'DSTU_9112_B');
        $this->assertSame($cyr, $t);
    }

    /**
     * @dataProvider data_DSTU_9112_B_c2l
     */
    public function test_DSTU_9112_B_c2l(string $cyr, string $lat): void {
        $q = $this->tr->encode($cyr, 'DSTU_9112_B');
        $this->assertSame($lat, $q);
    }

    /**
     * @dataProvider data_DSTU_9112_B_l2c
     */
    public function test_DSTU_9112_B_l2c(string $cyr, string $lat): void {
        $q = $this->tr->decode($lat, 'DSTU_9112_B');
        $this->assertSame($cyr, $q);
    }

    public function data_DSTU_9112_B_c2lr(): array {
        return [
        [
            "Україна, Хмельницький",
            "Ukrajina, Khmeljnycjkyj"
        ],
        [
            "Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
            "Shchastjam b'jesh zhuk jikh ghlycju v fon j gedzj prich."
        ],
        [
            "ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
            "hj Hj lj ljje ljji ljju ljja lj'e lj'i lj'u lj'a ljjo ljo"
        ],
        [
            "Єл Їл Юл Ял",
            "Jel Jil Jul Jal"
        ],
        [
            "бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
            "bj vj ghj gj dj zhj zj kj lj mj nj pj rj sj tj fj khj cj chj shj shchj"
        ],
        [
            "бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
            "bja vja ghja gja dja zhja zja kja lja mja nja pja rja sja tja fja khja cja chja shja shchja"
        ],
        [
            "б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
            "b'ja v'ja gh'ja g'ja d'ja zh'ja z'ja k'ja l'ja m'ja n'ja p'ja r'ja s'ja t'ja f'ja kh'ja c'ja ch'ja sh'ja shch'ja"
        ],
        [
            "бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
            "b'j b'jo v'j gh'j g'j d'j zh'j z'j k'j l'j m'j n'j p'j r'j s'j t'j f'j kh'j c'j ch'j sh'j shch'j"
        ],
        [
            "ня ньа н’я нь'н ньн",
            "nja nj'a n'ja nj'n njn"
        ],
        [
            "рос дыня эзёдынъ. бр кроў.",
            "ros dywnja ehwzjowdywnoh. br krouh."
        ],
        [
            "А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́",
            "Á á É é JÉ jé Ý ý Í í JÍ jí Ó ó Ú ú JÚ jú JÁ já"
        ],
        [
            "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            "Jés sJés jés sjés Jís sJís jís sjís Jús sJús jús sjús Jás sJás jás sjás"
        ],
        [
            "' ім’я 'жук' \"жук\" ' '",
            "' im'ja 'zhuk' \"zhuk\" ' '"
        ],
        [
            "Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.",
            "Sonce svitytj majzhe bilym svitlom, odnak cherez syljnishe rozsijuvannja i poghlynannja korotkokhvyljovoji chastyny spektra atmosferoju Zemli prjame svitlo Soncja bilja poverkhni nashoji planety nabuvaje pevnogho zhovtogho vidtinku. Jakshcho nebo jasne, to blakytnyj vidtinok rozsijanogho svitla skladajetjsja z zhovtuvatym prjamym sonjachnym svitlom i zaghaljne osvitlennja ob'jektiv na Zemli staje bilym."
        ],
        [
            "дуб!дуб\"дуб#дуб\$дуб%дуб&дуб'дуб(дуб)дуб*дуб+дуб,дуб-дуб.дуб/дуб:дуб;дуб<дуб=дуб>дуб?дуб@дуб[дуб\\дуб]дуб^дуб_дуб`дуб{дуб|дуб}дуб~дуб",
            "dub!dub\"dub#dub\$dub%dub&dub'dub(dub)dub*dub+dub,dub-dub.dub/dub:dub;dub<dub=dub>dub?dub@dub[dub\\dub]dub^dub_dub`dub{dub|dub}dub~dub"
        ],
        [
            "бод бод\tбод\nбод\rбод",
            "bod bod\tbod\nbod\rbod"
        ],
        [
            "об😎нап😘неп😭нєп🧐нїп😍нюп😀няп",
            "ob😎nap😘nep😭njep🧐njip😍njup😀njap"
        ],
        ];
    }

    public function data_DSTU_9112_B_c2l(): array {
        return [
        [
            "в’я в'я",
            "v'ja v'ja"
        ],
        [
            "Ї ї Й й Ё ё Ў ў",
            "JI ji J j JOW jow UH uh"
        ],
        ];
    }

    public function data_DSTU_9112_B_l2c(): array {
        return [
        [
            "я ї є ю г ж х щ ш ч ь",
            "jA jI jE jU gH zH kH sHcH sH cH hJ"
        ],
        [
            "А́ а́ Е́ е́ Є́ Є́ є́ є́ И́ и́ І́ і́ Ї́ Ї́ ї́ ї́ О́ о́ У́ у́ Ю́ Ю́ ю́ ю́ Я́ Я́ я́ я́",
            "Á á É é JÉ Jé jÉ jé Ý ý Í í JÍ Jí jÍ jí Ó ó Ú ú JÚ Jú jÚ jú JÁ Já jÁ já"
        ],
        [
            "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            "Jés sJés jés sjés Jís sJís jís sjís Jús sJús jús sjús Jás sJás jás sjás"
        ],
        ];
    }

    /**
     * @dataProvider data_KMU_55_c2l
     */
    public function test_KMU_55_c2l(string $cyr, string $lat): void {
        $q = $this->tr->encode($cyr, 'KMU_55');
        $this->assertSame($lat, $q);
    }

    public function data_KMU_55_c2l(): array {
        return [
        [
            "Україна, Хмельницький",
            "Ukraina, Khmelnytskyi"
        ],
        [
            "Щастям б’єш жук їх глицю в фон й ґедзь пріч.",
            "Shchastiam biesh zhuk yikh hlytsiu v fon y gedz prich."
        ],
        [
            "згин зГ зГин Згин Зг ЗГ ЗГИН",
            "zghyn zGH zGhyn Zghyn Zgh ZGH ZGHYN"
        ],
        [
            "ь Ь ль льє льї лью лья лье льі льу льа льйо льо",
            "  l lie li liu lia le li lu la lio lo"
        ],
        [
            "Єл Їл Юл Ял",
            "Yel Yil Yul Yal"
        ],
        [
            "бь вь гь ґь дь жь зь кь ль мь нь пь рь сь ть фь хь ць чь шь щь",
            "b v h g d zh z k l m n p r s t f kh ts ch sh shch"
        ],
        [
            "бя вя гя ґя дя жя зя кя ля мя ня пя ря ся тя фя хя ця чя шя щя",
            "bia via hia gia dia zhia zia kia lia mia nia pia ria sia tia fia khia tsia chia shia shchia"
        ],
        [
            "б’я в’я г’я ґ’я д’я ж’я з’я к’я л’я м’я н’я п’я р’я с’я т’я ф’я х’я ц’я ч’я ш’я щ’я",
            "bia via hia gia dia zhia zia kia lia mia nia pia ria sia tia fia khia tsia chia shia shchia"
        ],
        [
            "бй бйо вй гй ґй дй жй зй кй лй мй нй пй рй сй тй фй хй цй чй шй щй",
            "bi bio vi hi gi di zhi zi ki li mi ni pi ri si ti fi khi tsi chi shi shchi"
        ],
        [
            "А́ а́ Е́ е́ Є́ є́ И́ и́ І́ і́ Ї́ ї́ О́ о́ У́ у́ Ю́ ю́ Я́ я́",
            "Á á É é YÉ yé Ý ý Í í YÍ yí Ó ó Ú ú YÚ yú YÁ yá"
        ],
        [
            "Є́с сЄ́с є́с сє́с Ї́с сЇ́с ї́с сї́с Ю́с сЮ́с ю́с сю́с Я́с сЯ́с я́с ся́с",
            "Yés sIés yés siés Yís sÍs yís sís Yús sIús yús siús Yás sIás yás siás"
        ],
        [
            "' ім’я 'жук' \"жук\" ' '",
            "' imia 'zhuk' \"zhuk\" ' '"
        ],
        [
            "Сонце світить майже білим світлом, однак через сильніше розсіювання і поглинання короткохвильової частини спектра атмосферою Землі пряме світло Сонця біля поверхні нашої планети набуває певного жовтого відтінку. Якщо небо ясне, то блакитний відтінок розсіяного світла складається з жовтуватим прямим сонячним світлом і загальне освітлення об’єктів на Землі стає білим.",
            "Sontse svityt maizhe bilym svitlom, odnak cherez sylnishe rozsiiuvannia i pohlynannia korotkokhvylovoi chastyny spektra atmosferoiu Zemli priame svitlo Sontsia bilia poverkhni nashoi planety nabuvaie pevnoho zhovtoho vidtinku. Yakshcho nebo yasne, to blakytnyi vidtinok rozsiianoho svitla skladaietsia z zhovtuvatym priamym soniachnym svitlom i zahalne osvitlennia obiektiv na Zemli staie bilym."
        ],
        [
            "в’я в'я",
            "via via"
        ],
        [
            "дуб!дуб\"дуб#дуб\$дуб%дуб&дуб'дуб(дуб)дуб*дуб+дуб,дуб-дуб.дуб/дуб:дуб;дуб<дуб=дуб>дуб?дуб@дуб[дуб\\дуб]дуб^дуб_дуб`дуб{дуб|дуб}дуб~дуб",
            "dub!dub\"dub#dub\$dub%dub&dubdub(dub)dub*dub+dub,dub-dub.dub/dub:dub;dub<dub=dub>dub?dub@dub[dub\\dub]dub^dub_dub`dub{dub|dub}dub~dub"
        ],
        [
            "бод бод\tбод\nбод\rбод",
            "bod bod\tbod\nbod\rbod"
        ],
        [
            "об😎нап😘неп😭нєп🧐нїп😍нюп😀няп",
            "ob😎nap😘nep😭niep🧐nip😍niup😀niap"
        ],
        ];
    }
}
