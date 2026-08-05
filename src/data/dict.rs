#[derive(Debug, Default)]
#[allow(dead_code)]
pub struct Rijec {
    pub rijec:              Option<&'static str>,
    pub keywords:           Option<Vec<&'static str>>,
    pub display_rijec:      Option<&'static str>,
    pub vrsta:              Option<&'static str>,
    pub gramatika:          Option<Vec<&'static str>>,
    pub definicija:         Option<Vec<&'static str>>,
    pub primjer_uporabe:    Option<Vec<&'static str>>,
    pub sintagma:           Option<Vec<&'static str>>,
    pub frazeologija:       Option<Vec<&'static str>>,
    pub onomastika:         Option<Vec<&'static str>>,
    pub etimologija:        Option<&'static str>,
    pub izvedeni_oblici:    Option<Vec<&'static str>>,
    pub najranija_pojava:   Option<&'static str>,
    pub dodatno:            Option<Vec<&'static str>>,
}

pub fn rijecnik() -> Vec<Rijec> {
    vec![
        Rijec {
           rijec:               Some("rijec"),
           keywords:            Some(vec!["rijec", "rjec", "rec"]),
           display_rijec:       Some("riječ"),
           vrsta:               None,
           gramatika:           None,
           definicija:          Some(vec!["Definicija 1", "Definicija 2"]),
           primjer_uporabe:     None,
           sintagma:            None,
           frazeologija:        None,
           onomastika:          None,
           etimologija:         None,
           izvedeni_oblici:     None,
           najranija_pojava:    None,
           dodatno:             None,
           ..Default::default()
        },

        Rijec {
           rijec:               Some("ajde bok"),
           keywords:            Some(vec!["ajde bok", "ajd bok"]),
           display_rijec:       Some("àjde bȏk"),
           vrsta:               Some("fraz."),
           definicija:          Some(vec!["odgovor na nečiji niz tipfelera ili lapsusa u govoru, često kao prijedlog da govornik odustane od daljnjeg pisanja/govorenja", "uzvik nakon niza tipfelera ili lapsusa u govoru kojim govornik odustaje od pravilnog izgovora/pisanja"]),
           primjer_uporabe:     Some(vec!["A: \"Driver failiure... failiure... f... Ajde bok.\""]),
           najranija_pojava:    Some("https://discord.com/channels/1281587348139802624/1281595194365710406/1400378907005419561"),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("BDO/OBD"),
           keywords:            Some(vec!["BDO", "OBD"]),
           display_rijec:       Some("BDO/OBD"),
           vrsta:               Some("im. m."),
           definicija:          Some(vec!["WhatsApp grupa starija od Betona, dijeli puno članova s Betonom", "članovi istoimene grupe"]),
           etimologija:         Some("pokrata za razne izraze (Bjedujem Daske Oralno i sl.), ubrzo se slova premještavaju (OBD) te se gubi smisao pokrate (šansa za kišu)"),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("beat off"),
           keywords:            Some(vec!["beatoff", "beat off"]),
           display_rijec:       Some("beat off"),
           vrsta:               Some("im. m."),
           definicija:          Some(vec!["spontan natječaj glazbenog stvaranja u Betonu, najčešće preko programa FL Studio, čijeg pobjednika biraju ostali članovi Betona"]),
           etimologija:         Some("engl. beat + off --> natječaj ritmova"),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("Betonjanin"),
           keywords:            Some(vec!["betonjanin", "betonljanin"]),
           display_rijec:       Some("Bètōnjanin"),
           vrsta:               Some("im. m."),
           gramatika:           Some(vec!["<ž Betonjanka>"]),
           definicija:          Some(vec!["član Betona; Povjesničar/Povjesničarka; Betonac/Betonka"]),
           etimologija:         Some("pokrata za razne izraze (Bjedujem Daske Oralno i sl.), ubrzo se slova premještavaju (OBD) te se gubi smisao pokrate (šansa za kišu)"),
           dodatno:             Some(vec!["nekada i Betonljanin"]),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("Betonska Šaka"),
           keywords:            Some(vec!["betonska saka"]),
           display_rijec:       Some("Bètōnskā Šȁka"),
           vrsta:               Some("im. ž."),
           definicija:          Some(vec!["nominalna uloga u Betonu, imaju ju samo korisnici koji vide #sigmas-only", "vrhovno izvršno, sudbeno i zakonodavno tijelo u Betonu", "korisnici s istoimenom ulogom"]),
           etimologija:         Some("engl. iron fist"),
           dodatno:             Some(vec!["nekada i samo Šaka"]),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("big and gassy"),
           keywords:            Some(vec!["big and gassy", "b&g"]),
           display_rijec:       Some("big and gassy"),
           vrsta:               Some("prid."),
           definicija:          Some(vec!["sintagma koja je postala toliko neodvojiva od Mihaela da je izgubila sadržaj i smislenu funkciju"]),
           etimologija:         Some("big and round --> I'm so big and round --> I'm so big and gassy (Mihaelova izjava koju je, alkoholiziran, uz geste, neprestano ponavljao na jednom druženju"),
           frazeologija:        Some(vec!["I'm so big and gassy --> zbog neprestane uporabe, besadržajna izjava"]),
           dodatno:             Some(vec!["još i B&G, velik i plinovit, često samo napuhan, ili napuhnuti kao postati big and gassy"]),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("briši beton"),
           keywords:            Some(vec!["brisi beton"]),
           display_rijec:       Some("briši beton"),
           vrsta:               Some("gl. imp."),
           definicija:          Some(vec!["izjava rečena kao negativan komentar na trenutno stanje Betona, nečiji postupak ili neki događaj"]),
           dodatno:             Some(vec!["v. trenutci slabosti"]),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("Chudpush"),
           keywords:            Some(vec!["chudpush", "chud push"]),
           display_rijec:       Some("Chudpush"),
           vrsta:               Some("im. m."),
           definicija:          Some(vec!["idk gang nešto o due processu"]),
           etimologija:         Some("engl. chud + push"),
           dodatno:             Some(vec!["Zvjezdana do this one"]),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("Dr. Nightmare"),
           keywords:            Some(vec!["dr. nightmare", "dr nightmare", "drnightmare", "dr.nightmare"]),
           display_rijec:       Some("Dr. Nightmare"),
           vrsta:               Some("im. m."),
           definicija:          Some(vec!["Hrvojevo bivše korisičko ime", "zla persona Hrvoja, često ga se njome imenuje kada nepromišljeno postupa"]),
           onomastika:          Some(vec!["Nightmare SMP --> skupina kratkotrajnih Minecraft servera i Discord servera koje je Hrvoje napravio"]),
           dodatno:             Some(vec!["nenamjerno, ovo ime čini se kao antonim Minecraft youtubera Dreama (isto tako i s Nightmare SMP i DreamSMP)", "često se koristi nakon ponoći ili nakon uobičajnog vremena spavanja zbog šale da tada Hrvoje spava, a Dr. Nightmare se budi"]),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("Entobetonologija"),
           keywords:            Some(vec!["entobetonologija"]),
           display_rijec:       Some("Entobètōnologija"),
           vrsta:               Some("im. ž."),
           definicija:          Some(vec!["slanje fotografija raznih životinja (najčešće kukaca) u #bube-u-povijesti-betona kanalu, u njoj najviše sudjeluju Entobetonologičari (članovi s istoimenom ulogom)"]),
           etimologija:         Some("entomologija + Beton --> znanost koja proučava kukce u Betonu"),
           dodatno:             Some(vec!["v. buge"]),
           ..Default::default()
        },
        Rijec {
           rijec:               Some("gasi"),
           keywords:            Some(vec!["gasi"]),
           display_rijec:       Some("gási"),
           vrsta:               Some("gl. imp."),
           definicija:          Some(vec!["v. palji", "nekada fonološki napisano gassy, v. big and gassy"]),
           ..Default::default()
        },
    ]
}
