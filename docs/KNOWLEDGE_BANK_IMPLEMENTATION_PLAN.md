# Plan implementacije osobne baze znanja

## Implementirani čitateljski prototip — 2026-11-20

Mali tok čitanje → objašnjenje → točan izvor → povezana priča → povratak sada je
implementiran u postojećem lokalnom vieweru, s engleskim/bosanskim sučeljem i
spremanjem/uređivanjem privatnih bilježaka, isticanja i predloženih veza.
Pokretanje: `npm run reading:demo -- --synthetic`. Dva originalna izmišljena
prizora provjeravaju interakciju; John 9 ostaje planirana tema bez stvarnog teksta
ili izmišljenih tumačenja/dokaza. Prototip nije vlasnikova provjera uporabljivosti
niti popunjen istraživački dosje.

Ugovori reading-view/item v1 pohranjuju se kao privatni v3 article dokumenti kroz
postojeći Python writer, zaključavanje, povijest i backup. V3 vrste zapisa nisu
proširene. Detalji, granice i oporavak su u
[pilot dokumentu](JOHN_9_READING_DESK_PILOT.md). Početni zadatak definiranja ugovora
i spajanja viewer sloja dovršen je; ne započinjati ga ponovno prema starijem planu.
Sljedeći mali korak je opaženi prolazak vlasnika i ispravak prvog konkretnog
problema, uz zaseban plan točnog izvora i sadržaja za stvarni John 9.

## Aktualni produktni prioritet — 2026-11-19

Vlasnik traži jedno jasno mjesto za čitanje knjiga i istraživanje njihova
konteksta, objašnjenja, dokaza, likova i povezanih priča. Aktualni produktni
ugovor i pitanja su u [READING_DESK_PRODUCT_DIRECTION.md](READING_DESK_PRODUCT_DIRECTION.md).
U njemu su odvojene izričito navedene potrebe, prijedlozi dizajna i još
neodgovorene preferencije. Taj dokument određuje novi redoslijed isporuke.

Prva sljedeća korisnička cjelina je mali tok knjiga/odlomak → objašnjenje →
točan izvor → smislena povezana priča/lik → povratak na početno mjesto čitanja.
Vlasnik je odgovorio na svih osam početnih/follow-up pitanja: biblioteka i
istaknuta tražilica zajedno; desktop/laptop; tekst i objašnjenje usporedno;
kratak jasan prikaz pa atribuirana mišljenja i dokazi; preklop engleski /
bosanski-hercegovački; bilješke, isticanja i predložene veze u prvoj uporabljivoj
verziji. Odabran je [John 9 pilot](JOHN_9_READING_DESK_PILOT.md), sa zasebnim
tekstualnim svjedocima i neovisnim povijesnim dokazima gdje su dostupni.
Ne ponavljati ta pitanja niti odgađati osobne alate kao neodabranu mogućnost.
Postojeći mali lokalni viewer i Python provjere ostaju temelj;
ne uvodi se nova frontend platforma, opći raw-file server ili stvarni tekst bez
admission provjere. Dok nema dopuštenog stvarnog izvora, koristi se označeni
originalni sintetički primjer.

F0–F14 ispod ostaje tehnički backlog, a ne obvezan redoslijed prije poboljšanja
čitanja. F0/F1, upravljana pohrana/revizije, v3 claim/evidence, privatne bank kopije,
jednostavna pretraga i osnovni read-only viewer već imaju implementirane dijelove;
ne započinjati ih ponovno prema povijesnoj napomeni. Napredni indeks, procjene,
entity identity review, stvarni historical admission i cijeli reading-desk tok
nisu time dovršeni. Aktualno stanje provjeriti u PROGRESS/NEXT_STEPS i
[izvještaju o korisnosti](PROJECT_USEFULNESS_REPORT_2026-11-19.md).

Ni ova promjena prioriteta ni supporting-literature veza ne šire GEN/MAT/MRK/
LUK/JHN korpus, ne odobravaju izvore i ne stvaraju ljudske recenzije.

## Povijest početnog plana i implementacije

Datum: 2026-11-15. Status: prijedlog arhitekture i izvršiv razvojni backlog.
Ovo je plan, a ne potvrda da su opisane mogućnosti već implementirane.
Korisnik je zatražio opsežan plan kodiranja, ne objavu ili promjenu korpusa.

Naknadni početak implementacije, 2026-11-15: F0/minimalni read-only F1 sada postoje.
Implementirani su `jeb bank validate/show --bank-root ...`, početne sheme i testovi.
Točan implementirani format i ograničenja su u BANK_FORMAT.md i BANK_WORKFLOW.md.
Sve ostale opisane naredbe i mogućnosti ispod ostaju razvojni backlog.

F2 napredak, 2026-11-15: upravljani format 2.0 dodaje init/create/edit/history/diff/
recover, OS single-writer lock, expected-revision sukobe i pune nepromjenjive
snimke s atomskim HEAD pokazivačem. Format 1.0 ostaje read-only. Detalji, recovery
granice i zaštitni limiti su u BANK_FORMAT.md; migracija i indeks ne postoje.

Rani F13 korak, 2026-11-15: privatni backup/backup-verify/restore potvrđenog v2
lanca sada postoje. BANK_BACKUPS.md opisuje točan obuhvat, limite i vraćanje u
novu mapu. Nema media object kopije, javnog izvoza, migracije ili rasporeda kopiranja.

F3A, 2026-11-15: bank evidence prepare/validate/inspect radi s izdvojenim
nepregledanim paketima, exact-revision bindings i tipiziranim lokatorima. V2 sheme
i kopije ostaju nepromijenjene. BANK_EVIDENCE.md opisuje granice i ugovor prije
budućeg F3B spremanja claim/evidence zapisa u novu verziju glavne baze.

F3B, 2026-11-15: eksplicitno inicijaliziran format3.0 sada trajno sprema claim/
evidence s exact-revision referencama na ranije potvrđene zapise. Reference i
links izvještaj razlikuju povijesnu potporu od aktualne tvrdnje. V3 ima zasebne
backup sheme; v2 je sačuvan. Nema migracije, uvoza paketa, procjena ili odobrenja.

## 1. Namjera i mjerilo uspjeha

Primarno korisničko iskustvo sada je objedinjeni stol za čitanje i istraživanje:
razumjeti knjigu/odlomak, otvoriti podlogu objašnjenja, pratiti korisnu vezu i
vratiti se bez gubitka konteksta. Brz unos, verzije i indeksi podupiru taj tok.
Napredak mjeriti razumljivošću i stvarnim prolaskom odabranog čitateljskog
scenarija, uz evidenciju nejasnih oznaka i izgubljenih navigacijskih koraka.

Izgraditi trajnu osobnu bazu znanja za jednog čovjeka: prikupljanje, istraživanje,
čitanje, ispravljanje, stvaranje i dijeljenje. Ljudi i agenti trebaju moći uzeti
odabrani dio baze, razumjeti odakle dolazi i koristiti ga u drugim projektima.
Wiki je čitljiv prikaz; baza mora ostati korisna bez određene web stranice ili AI-ja.

Temeljna načela:

- Brzo spremanje bez obveznog detaljnog katalogiziranja.
- Otvorene lokalne datoteke i dokumentiran format razmjene.
- Trajni identiteti, provjerljive veze i točno podrijetlo.
- Sačuvani izvornici i prethodne procjene; ispravci ne brišu povijest.
- Razlikovanje dokaza, tvrdnje, tumačenja, osobne refleksije i kreativnog rada.
- AI predlaže i obrađuje; ne postaje ljudski recenzent.
- Dubina obrade raste s potrebom, ne s brojem spremljenih datoteka.
- Svaki veći korak završava lokalno upotrebljivim rezultatom.

Praktični pokazatelji za pilot, kao ciljevi koje tek treba izmjeriti:

- Poveznicu ili kratku bilješku spremiti u manje od 30 sekundi.
- Poznat sadržaj pronaći među desetak tisuća zapisa bez ručnog obilaska mapa.
- Od tvrdnje do konkretne lokacije dokaza doći u najviše nekoliko radnji.
- Izvesti temu s podlogom jednom naredbom, uz objašnjenje izostavljenih datoteka.
- Obnoviti prikaz i pretragu iz izvornih zapisa bez stare baze indeksa.
- Vratiti sigurnosnu kopiju u praznu mapu i provjeriti sadržaj.

## 2. Zatečeno stanje i granice

Pregledano: AGENTS.md, PROGRESS.md, NEXT_STEPS.md, pyproject.toml, package.json,
web/server.mjs, početci src/jeb/knowledge.py i cli.py te pravila prava.

- Jedan instalabilni Python paket, Python 3.13.x, CLI `jeb`.
- PyYAML i jsonschema postoje; koristiti postojeći hash-locked postupak instalacije.
- Biblijski knowledge/review/curation/narrative postupci već postoje.
- Opcionalni Node server i plain HTML/CSS/JS preglednik već postoje i samo čitaju.
- library/ sadrži odvojeni katalog, nalaze, pretraživanja i privatne kopije.
- Tijekom ovog pregleda katalog istraživanja ima 93 nalaza za 83 od 291 djela;
  to nisu 83 potvrđena cjelovita izvora. Brojevi se dalje čitaju iz podataka.
- Postoje nezabilježene lokalne promjene; sačuvati ih bez prepisivanja.

Nova baza koristi zasebni namespace `bank`, izvan `data/knowledge` i korpusa.
Predloženi ulaz je `jeb bank`; to nije drugi paket niti zamjena postojećeg CLI-ja.
Scope GEN/MAT/MRK/LUK/JHN ostaje nepromijenjen. Veza na biblioteku nije primanje
knjige u korpus. Postojeći procesi odobrenja i prava ostaju zasebni.

Plan ne uvodi model API-je, chat scraping, plaćene servise ili cloud ovisnosti.
Ne implementirati veliki frontend. Napredne mogućnosti ispod su kasnije faze,
a ne razlog za proširenje prve verzije.

## 3. Arhitekturna odluka

Tri sloja s jasnim vlasništvom:

1. Autoritativni lokalni zapisi: JSON metapodaci, Markdown tijela, revizije,
   transakcijski manifesti i reference na medijske objekte.
2. Izvedeni indeks: SQLite iz standardne biblioteke, uključujući full-text ako
   dostupna SQLite verzija podržava FTS5. Indeks se uvijek može ponovo izgraditi.
3. Adapteri: CLI, mali web preglednik, kasniji lokalni editor i izvoz za agente.

Python je jedini vlasnik validacije i pisanja trajnih zapisa. Ne implementirati
drugi zapisivač u Nodeu. Node ostaje opcionalni adapter/prikaz dok se posebno
ne procijeni kako čitati Python indeks. Nikad ne pokretati shell iz korisničkog teksta.

Dok se ne uvede mali lokalni Python servis, web čita ograničenu generiranu projekciju.
CLI omogućuje pisanje i pretraživanje. Kasniji servis koristi isti Python sloj,
ne zaseban model podataka. Ne pretpostaviti da statična stranica može pisati na disk.

## 4. Predloženi raspored datoteka

```text
bank/
  workspace.json                 # verzija, identitet i konfiguracija prostora
  records/<id>/record.json       # trenutni metapodaci
  records/<id>/body.md           # opcionalni čitljiv članak
  history/<id>/<revision>/       # prethodne nepromjenjive verzije
  transactions/<transaction>/    # manifesti dovršenih promjena
  proposals/<proposal>/         # neprimijenjene dopune; privatno po zadanim pravilima
  private/                      # privatni zapisi; nikad generički web-root
  objects/sha256/<prefix>/<hash> # lokalni binarni sadržaj; nije automatski za Git
  derived/                      # indeks, izdvojeni tekst, projekcije; obnovljivo
  exports/                      # lokalni paketi; izvoz nije objava
src/jeb/bank/
  __init__.py
  models.py
  storage.py
  validation.py
  revisions.py
  links.py
  sources.py
  assets.py
  index.py
  search.py
  proposals.py
  packets.py
  export.py
  backup.py
src/jeb/schemas/bank-*.schema.json
tests/test_bank_*.py
docs/BANK_FORMAT.md
docs/BANK_WORKFLOW.md
```

Raspored je cilj, ne zadatak da se sve prazne mape odmah naprave. Prije prve
implementacije provjeriti postojeća imenovanja shema. Ne mijenjati globalni
.gitignore prije klasifikacije pojedinih putanja. Privatni sadržaj ne smije
završiti u Gitu samo zato što je tekst, a generirani izvozi nisu javni po zadanim pravilima.

Za upravljani par record.json/body.md promjene prolaze kroz transakciju.
Vanjsko uređivanje tijela je dopušten ulaz, ali mora biti otkriveno i prihvaćeno
kao nova revizija prije indeksiranja/izvoza. Ne održavati dvije neovisne istine.

## 5. Model zapisa

Zajednička omotnica: schema_version, workspace_id, id, kind, title, created_at,
recorded_by, revision_id, parent_revision, body_sha256, visibility, processing_state.
Koristiti stabilan UUID iz standardne biblioteke; naslov i slug nisu identitet.
Polja s nepoznatom vrijednošću ostaju nepoznata, bez AI popunjavanja nagađanjem.

### 5.1 Predmet i članak

- Entity: osoba, mjesto, događaj, organizacija, pojam ili djelo.
- Article: čitljiva sinteza vezana uz jedan ili više predmeta.
- Alias: zabilježeni alternativni naziv s podrijetlom, bez automatskog preslovljavanja.
- Kolekcije i oznake su neisključivi pogledi; predmet može pripadati više zbirki.
- Spajanje duplikata je eksplicitno; stari ID dobiva preusmjerenje i povijest.

### 5.2 Izvor i izdanje

- Work: identitet djela, kada je poznat.
- Edition: točan jezik, prevodilac, urednik, izdavač, datum i izdanje.
- Source artifact: određena mrežna stranica ili datoteka, URL, pristup, hash,
  veličina, medijski tip i uvjeti korištenja.
- Snapshot/retrieval receipt: što je stvarno preuzeto i kada, uz rezultat i granice.
- Ne poistovjećivati djelo, prijevod, izdanje i mrežnu kopiju.
- Dvije stranice koje prepisuju isti izvor ne računati kao nezavisnu potvrdu.

### 5.3 Tvrdnja, dokaz i procjena

- Claim: predmet, odnos i vrijednost; tekstualno obrazloženje kada formalizacija
  nije prikladna. Različite tvrdnje zadržavaju različite identitete.
- Evidence link: povezuje točnu reviziju tvrdnje s dokazom i odnosom
  supports / contradicts / contextualizes / mentions.
- Locator: tiskana stranica i PDF stranica odvojeno; odjeljak, stih, vremenski
  interval, područje slike ili objekt u modelu prema tipu materijala.
- Assessment: autor procjene, razlozi, ograničenja, vrijeme i veze na dokaze.
- Selection: eksplicitni trenutačni izbor među procjenama, s razlogom i poviješću.
- Povučena procjena ne proizvodi automatski povratak na stariju prihvaćenu tvrdnju.
- Nema globalnog broja koji izjednačuje pouzdanost izvora u svim pitanjima.
- Ljudski pregled nije dokaz istinitosti; shema ne dokazuje povijesnu tvrdnju.

Datumi podržavaju preciznost, raspon, približnost, kalendar i BCE/CE bez lažne
preciznosti. Izvorno iskazan datum čuva se uz eventualnu izvedenu normalizaciju.
Vrijeme događaja razlikuje se od vremena bilježenja i promjene procjene.

### 5.4 Materijali i izvedeni radovi

- Asset: identitet datoteke, autor, izvor, tip, sadržajni hash, prava i dostupnost.
- Derivation: ulazi s točnim revizijama, postupak, alat/verzija i izlazni hash.
- Output: članak, prezentacija, videoscenarij, titlovi, snimka, 3D scena ili paket.
- Sačuvati izvorni format i uređivu podlogu gdje postoje; konverzija ih ne zamjenjuje.
- AI ilustracija/rekonstrukcija nije povijesni dokaz. Označiti način nastanka.
- Nije nužan preglednik za svaki tip: identitet, provjera i preuzimanje prvo.

### 5.5 Povijest i pristup

- Razlikovati processing_state (inbox/organized/researched), stanje tvrdnje i
  stvarni review zapis. Jedno se ne smije izvoditi iz drugoga.
- Visibility i dopuštena uporaba su odvojeni: private/shared/public_candidate
  nije licencija i ne daje pravo objave.
- Akter može biti čovjek, alat ili agent. AI nikad ne dobiva ulogu human reviewer.
- Brisanje iz aktivnog prikaza koristi tombstone; eksplicitno uklanjanje osjetljivog
  sadržaja mora imati zaseban postupak. Ne obećavati vječno čuvanje privatnih podataka.

## 6. Pisanje, integritet i povijest

Svaka promjena ima očekivanu baznu reviziju. Zastarjela izmjena daje sukob i diff,
ne prepisivanje. Spremiti prethodnu verziju, pripremiti nove datoteke u stagingu,
provjeriti sve reference, pa završiti commit protokol s manifestom.

Atomski rename jedne datoteke ne znači atomsku promjenu više datoteka. Čitači
moraju prepoznati samo dovršene transakcije. Testirati prekid na svakom koraku,
ponovno pokretanje i oporavak bez gubitka prihvaćene verzije. Prvi pilot je
single-writer; drugi writer dobiva jasnu poruku. Stale lock nije dozvola za brisanje.

SHA-256 provjerava identitet i integritet, ne autorstvo ni istinitost. Git bilježi
dio povijesti, ali procjena mora sama sadržavati razlog promjene.

## 7. Razvojne faze i kriteriji dovršenosti

### F0 — Arhitekturni ugovor i početno stanje

Zadaci:
- Popisati postojeće validatore, putanje, sheme i ponovno upotrebljive funkcije.
- Napisati BANK_FORMAT.md: identiteti, verzije, putanje, javno/privatno i nepoznato.
- Dokumentirati granicu bank / library / corpus i zabranu implicitne promocije.
- Provjeriti Python 3.13 i hash-locked okruženje prema README-u.

Gotovo: ugovor ima mali potpuno originalan primjer; config/sources nisu promijenjeni;
zabilježeni stvarni rezultati početnih provjera ili precizno objašnjena nedostupnost.

### F1 — Najmanja pohrana i validator

Zadaci:
- Uvesti omotnicu, entity, source i article sheme pod src/jeb/schemas.
- Dodati storage/validation i `jeb bank init`, `validate`, `show`.
- Odbiti traversal, nepoznate verzije, duple ID-jeve i reference izvan prostora.
- Uvesti ograničenja veličine ulaza i strogo UTF-8 čitanje.

Gotovo: mali originalni primjer prolazi; pokvareni JSON, dupli ključevi i nepoznata
polja daju korisne greške s putanjom/poljem; banka ne mijenja biblijske podatke.

### F2 — Revizije i sigurne izmjene

Zadaci:
- Implementirati single-writer, expected-revision i transakcijski manifest.
- Dodati `create`, `edit`, `history`, `diff`, `recover`.
- Spremiti točne prethodne bajtove; prikazati vanjske neprihvaćene promjene.

Gotovo: simulirani prekid i konkurentni zapisivač ne uništavaju podatke;
neuspjela promjena ne pojavljuje se kao dovršena revizija.

### F3 — Dokazi, neslaganja i promjene razumijevanja

Zadaci:
- Dodati claim/evidence/assessment/selection sheme i validaciju lokatora.
- Implementirati `assess`, `select`, `withdraw` uz eksplicitno autorstvo.
- Prikazati trenutačno stanje i slijed ranijih procjena.
- Dodati tipizirane datume bez nametanja suvremenog kalendara.

Gotovo: originalan primjer s dvije konkurentne tvrdnje i novim dokazom pokazuje
zašto se procjena promijenila; stare tvrdnje ostaju dostupne; nema AI potvrde čovjeka.

### F4 — Veze, nazivi i postojeća biblioteka

Zadaci:
- Uvesti eksplicitne veze, backlinkove, redirekcije i provjeru dangling referenci.
- Dodati read-only adapter za library katalog/nalaze s identitetom i hashom ulaza.
- Mapirati book_id i finding identitete bez prepisivanja izvornog library zapisa.
- Uvoz metapodataka ne preuzima privatne datoteke i ne podiže status provjere.

Gotovo: ponovljen uvoz je idempotentan; promjena upstream nalaza daje preglednu
razliku; izbor, ulomak i zbirka ostaju različiti od cjelovite knjige.

### F5 — Lokalna pretraga i pregled

Zadaci:
- Izgraditi SQLite indeks naslova, članaka, vrsta, oznaka, referenci i backlinkova.
- Provjeriti dostupnost FTS5; dokumentirati ograničeni fallback bez nove ovisnosti.
- Dodati filtre: tip, zbirka, vrijeme, obrada, dostupnost, izvor i pristup.
- `jeb bank index build/check`, `search`, `links`, `related`.
- Rangiranje prvo po doslovnom naslovu/ID-u, zatim tekstu; razlog povezanosti vidljiv.

Gotovo: indeks se briše i identično obnavlja; neaktualan indeks je označen;
privatni sadržaj ne ulazi u projekciju za dijeljenje ni njezine isječke/brojila.

### F6 — Mala crno-bijela wiki

Aktualizacija 2026-11-19: povijesni naziv faze ne određuje novu vizualnu temu.
Raspored je sada desktop-first, tekst i objašnjenje usporedno, sa zajedničkom
bibliotekom/tražilicom i preklopom engleski / bosanski-hercegovački. Postojeći
popisi i record detail nisu kriterij dovršetka reading-desk iskustva. Ovu fazu
voditi malom U1 John 9 cjelinom iz produktnog ugovora; biblioteka, tekst,
objašnjenje, dokazi i povezane priče trebaju biti jasna korisnička putanja.
Uključiti prvi mali F7 reading-tools korak jer ga je vlasnik izričito odabrao.

Zadaci:
- Dopuniti postojeći viewer ograničenom bank projekcijom, bez nove frontend platforme.
- Početni prikazi: tražilica, članak, izvor/dokaz, povijest i zbirka.
- Prikazati reference uz navode, povezane zapise i povratne veze.
- Omogućiti duboke poveznice i označiti nedostupnu privatnu podlogu.
- Sigurno prikazati Markdown; raw HTML nije izvršiv ulaz.
- Tipkovnica, vidljiv fokus, kontrast, uski ekran, jasna prazna stanja.

Gotovo: stvarno pregledan lokalni prikaz; privatne putanje nisu web-rute;
postojeća biblioteka i deset dopuštenih dokumenata i dalje rade.

### F7 — Brzi inbox i ljudsko uređivanje

Aktualizacija 2026-11-19: privatne bilješke, isticanja i predložene veze dio su
prve uporabljive U1 verzije. Najprije definirati mali verzionirani ugovor za
reading anchors i trajno spremanje kroz postojeći Python writer; nema tihog
proširenja postojećih v3 enumova ili miješanja osobne bilješke s odobrenjem.
Potpuno uređivanje objašnjenja i autoritativna kuracija ostaju kasniji backlog.

Zadaci:
- CLI capture za URL, bilješku i lokalnu datoteku; URL unos ne znači mrežni fetch.
- Spremanje traži minimum polja; organizacija može pričekati.
- Dodati mali Python lokalni servis tek kada je potreban web unos; koristi isti writer.
- Urednik prikazuje baznu reviziju, diff, otkazivanje i oporavak nacrta.
- Zadržati postojeći Node server read-only ili njegovu ulogu jasno zamijeniti;
  ne otvarati mu proizvoljan zapis na disk.

Gotovo: čovjek može spremiti i doraditi bilješku bez JSON-a; dva otvorena editora
ne prepisuju jedan drugog; otkazivanje ne stvara lažnu prihvaćenu reviziju.

### F8 — Mediji i najbolje dostupne kopije

Zadaci:
- Dodati lokalni object store, hash/size provjeru, deduplikaciju i manifest.
- Razlikovati nedostupnu, vanjsku i lokalno provjerenu kopiju.
- Uvesti priključke za izdvojeni tekst i thumbnail s verzijom alata i ulaznim hashom.
- OCR/transkript ostaje izveden zapis, ne zamjena za izvornik i ne ljudski pregled.
- Prvo podržati PDF/sliku/audio/video kao datoteke; 3D pregled i transkodiranje kasnije.

Gotovo: identične datoteke dijele sadržaj bez gubitka različitih izvora i prava;
nedostajući alati daju razumljiv status; privatni sadržaj nije automatski poslužen.

### F9 — Paketi za ljude, projekte i agente

Zadaci:
- Definirati manifest paketa: ID-jevi, revizije, hashovi, prava i ovisnosti.
- `export --profile private|collaboration|public-candidate` uz eksplicitne razlike.
- Računati zatvoren skup ovisnosti; izostavljene zapise navesti kao nedostupne.
- Odbiti javni kandidat kada bitna podloga nema odgovarajuću procjenu uporabe.
- Import u quarantine; pregled sukoba, zatim eksplicitna primjena.
- Isti ID/ista revizija/različiti bajtovi predstavljaju kvar ili sukob.
- Pripremiti mapiranje prema RO-Crate; usklađenost tvrditi tek nakon provjere.

Gotovo: izvoz/uvoz u prazni prostor čuva identitete, navode i povijest; zip-slip,
symlink, zip bomb i prekoračenje limita odbijeni; izvoz nikad ne šalje podatke.

### F10 — Ugovor za rad AI agenata

Zadaci:
- `packet create` iz točnih revizija i izabranog zadatka.
- Dokumentirati search/read/propose ugovor i male primjere.
- Odgovor agenta sadrži bazne revizije, promjene, dokaze, nepoznanice i alat.
- `proposal validate/show/apply/reject` uz stanje sukoba i ljudsko obrazloženje.
- Primjena sadržaja ne stvara owner approval ili neovisnu potvrdu izvora.
- Spremljene upute u izvorima tretirati kao podatke; prijedlog ne smije izvršavati
  programe, preuzimanja ili proizvoljne putanje.

Gotovo: cijeli ciklus radi offline s originalnim testnim odgovorom; zastarjeli
paket se odbija; nema ugrađenog model API-ja ili automatskog razgovora s platformom.

### F11 — Izvedeni radovi i ponovno korištenje

Zadaci:
- Dodati output/derivation modele i popis ulaza s točnim revizijama.
- Izvesti Markdown članak, predavački paket i neutralni tekst slajdova.
- Čuvati video scenarij, scene, titlove i reference na vizualne materijale.
- Opcionalni konverteri otkrivaju alat/verziju; osnovni rad ne ovisi o njima.
- Promjene podloge označavaju izlaz kao needs_recheck, ne prepisuju završni rad.

Gotovo: može se objasniti podrijetlo svakog izlaza i ponovno složiti njegov ulazni
paket. Ne tvrditi bajt-po-bajt reproduktivnost nedeterminističkog alata.

### F12 — Održavanje zbirke

Zadaci:
- `doctor`: pokvarene veze, duplikati, nepoznati izvori, nestale datoteke,
  neusuglašene revizije i zastarjeli izvedeni radovi.
- Sačuvane pretrage i redovi za pregled umjesto stalnih obavijesti.
- Eksplicitno spajanje predmeta uz preusmjerenja i provjeru posljedica.
- Detekcija utjecaja promjene; AI kasnije može predlagati grupu dopuna.

Gotovo: izvještaj razlikuje grešku, upozorenje i nepotpun podatak; ništa ne
popravlja niti odbacuje automatski bez odabrane operacije.

### F13 — Sigurnosne kopije, restore i migracije

Zadaci:
- Manifest sigurnosne kopije obuhvaća trajne zapise i izabrane medije.
- Razlikovati metapodatkovnu kopiju od pune kopije; nedostajuće objekte navesti.
- Restore u novu mapu, provjera hashova, novi indeks i usporedba referenci.
- Migracije verzionirane, s dry-run izvještajem i kopijom prije promjene.
- Bez tihog prepisivanja starog formata; nepodržane verzije jasno odbiti.

Gotovo: offline restore provjeren u praznom direktoriju. Git i object store na
istom disku nisu predstavljeni kao dvije nezavisne sigurnosne kopije.

### F14 — Dugoročne mogućnosti nakon stvarne uporabe

- OCR i lokalni transkripti s preciznim lokatorima.
- Dodatni adapteri izvoza, statična javna zbirka i povratne primjedbe suradnika.
- Veći batch uvozi uz ponavljanje/oporavak i kontrolu prostora na disku.
- Semantička pretraga samo ako doslovna pretraga i veze pokažu stvaran nedostatak;
  odvojeni prijedlog, bez model API-ja ili nove cloud ovisnosti.
- Višekorisnički rad i sinkronizacija tek uz zasebno projektiranje autentikacije,
  sukoba i pristupa; vidljivost u JSON-u sama ne osigurava autorizaciju.
- Napredni graf, vremenska crta i 3D viewer samo kada pomažu konkretnom radu.

Ovo nisu preduvjeti za dovršenu prvu verziju.

## 8. Predloženi CLI, kao specifikacija budućeg rada

```text
jeb bank init
jeb bank validate
jeb bank capture --url <url>
jeb bank capture --file <path>
jeb bank show <id>
jeb bank edit <id> --expected-revision <revision>
jeb bank history <id>
jeb bank diff <id> --from <revision> --to <revision>
jeb bank search <query>
jeb bank index build
jeb bank links <id>
jeb bank library import --dry-run
jeb bank packet create --subject <id>
jeb bank proposal validate --input <path>
jeb bank proposal apply --input <path>
jeb bank export --subject <id> --profile collaboration --output <path>
jeb bank import --input <path> --dry-run
jeb bank doctor
jeb bank backup --output <path>
jeb bank restore --input <path> --destination <new-path>
```

Osim naknadno implementiranih validate/show s obveznim --bank-root, naredbe još
ne postoje. Precizne argumente odrediti u odgovarajućoj fazi; ne uvoditi
sve podnaredbe unaprijed. Destruktivne radnje ne pretpostavljaju pristanak kroz
nepovezanu naredbu. Obrada argumenata ostaje unutar postojećeg CLI-ja.

## 9. Sigurnost lokalnog sučelja i granice privatnosti

- Loopback, Host/Origin provjere, zahtjevi ograničene veličine i strogo tipizirani ID-jevi.
- Za buduće write rute: session token/CSRF zaštita, bez permisivnog CORS-a.
- Nikad generički file endpoint koji prihvaća proizvoljnu putanju.
- Zaštita od Windows junction/symlink bijega, relativnih putanja i arhivskih trikova.
- HTML, SVG i 3D/audio/video sadržaj ne izvršavati kao pouzdan kod.
- Ekstrakcija datoteka i vanjski alati: timeout, limiti, bez shell interpolacije.
- Bez automatskog mrežnog dohvaćanja pri otvaranju članka ili paketa.
- Kasniji fetch mora provjeravati svaki redirect, blokirati lokalne adrese i
  čuvati receipt; prijava ili zaštitna prepreka ne zaobilazi se.
- Dijeljena projekcija i indeks grade se iz dopuštenih zapisa, uključujući
  privatne naslove, backlinkove i transitive metapodatke kao moguće curenje.

## 10. Provjere i testne skupine

Za svaku fazu testirati ponašanje i rizik, ne preslikavati implementaciju.

1. Schema/identitet: nepoznata verzija, krivi tip, dupli ID, nevaljana referenca.
2. Povijest: konflikt, prekid, oporavak, vanjska izmjena i povučena selekcija.
3. Dokazi: pogrešan lokator, sukob tvrdnji, odvojeno vrijeme i nepoznata vrijednost.
4. Granice: bank ne prima korpus niti mijenja config/sources/review stanja.
5. Indeks: rebuild, deterministički poredak, stale stanje i privatna projekcija.
6. Mediji: izmijenjeni bajtovi, nestali objekt, duplikat s različitim pravima.
7. Paketi: round-trip, nedostajuće ovisnosti, identitetski sukob i opasna arhiva.
8. Agent: prompt injection kao podatak, nedopuštena putanja, lažna ljudska uloga.
9. Web: pristup tipkovnicom, siguran tekst, Host/Origin/CSRF i konflikt uređivanja.
10. Oporavak: puna i metapodatkovna kopija, nedostupan alat i migracija dry-run.

Testovi rade offline, bez povijesnog teksta i bez stvarnih ljudskih odobrenja.
Za mjerenje indeksa generirati originalne skupove 1k/10k/100k zapisa, a rezultate
zapisati s hardverom i SQLite verzijom. Latenciju ne proglašavati garancijom
na temelju jednog računala. Optimizirati tek izmjerena uska grla.

Obvezne provjere za Python/schema promjene:

```text
python -m ruff check src tests
python -m ruff format --check src tests
python -m jeb validate --stage schemas
python -m unittest discover -s tests -v
```

Za zahvaćeni postojeći viewer/library:

```text
npm run library:catalog
npm run test:web
git diff --check
```

Nove provjere dodavati postojećem offline postupku; ne uvoditi drugi sustav pakiranja.
Stvarne komande, rezultati i ograničenja idu u PROGRESS.md nakon svake faze.

## 11. Redoslijed isporuke i veličina zahvata

Aktualni redoslijed: U0 odgovori su zapisani; definirati minimalni reader/private
tools ugovor i isporučiti mali U1 John 9-oblikovani tok s privatnim bilješkama,
isticanjima i predloženim vezama. Zatim proširivati otkrivanje i naprednu kuraciju
prema stvarnoj uporabi. Veze
F0–F14 ispod opisuju tehničke ovisnosti svojih mogućnosti, ne zabranu ranijeg
read-only usability poboljšanja postojećeg preglednika.

Zavisnosti: F0 → F1 → F2 → F3 → F4 → F5 → F6.
F7 slijedi stabilan writer i preglednik. F8 može početi nakon F2; F9 zahtijeva
stabilne veze i medijske manifeste. F10 koristi F2/F3/F9. F11 koristi F8/F9.
F12/F13 rastu postupno; osnovni backup i provjera integriteta potrebni su prije
uvoza vrijednih osobnih podataka, ne tek na kraju projekta.

Predloženi mali pregledljivi zahvati:

1. Format i originalni primjer, bez novih naredbi.
2. Minimalne sheme i validacija.
3. Čitanje i prikaz.
4. Sigurno stvaranje i revizije.
5. Dokazi i povijest procjena.
6. Veze i library adapter.
7. Obnovljivi indeks i pretraga.
8. Mali read-only wiki prikaz.
9. Brzo spremanje i uređivanje.
10. Medijski objekti i osnovni backup/restore.
11. Izvoz/uvoz odabranog povezanog skupa.
12. Paketi za AI prijedloge.
13. Izvedeni radovi i praćenje zastarjelosti.

Nema pouzdane kalendarske procjene prije F0–F2. Za svaki sljedeći zahvat nakon
pilota procijeniti trud, ne davati obećanje za cijeli sistem unaprijed.
Ne stvarati commit, PR, push ili izdanje samo zato što plan koristi pojam zahvata.

## 12. Što čini prvu stvarno korisnu verziju

Aktualni U1 kriterij: knjižnica/pretraga → usporedni tekst/objašnjenje → točan
dokaz → smislena veza → povratak, plus sva tri osobna alata i dvojezični preklop.
Read-only interni korak nije dovršena prva verzija. Izvoz i bogati medijski alati
iz ranijeg šireg bank plana nisu preduvjet tog malog reading-desk pilota.

Prva verzija obuhvaća stabilnu pohranu, povijest, izvore i dokaze, veze, pretragu,
mali preglednik, CLI capture, lokalne datoteke te osnovni izvoz i restore.
Web uređivanje može doći poslije CLI-ja. Agent, bogati medijski preglednici i
automatske pretvorbe nisu uvjet da baza bude korisna.

Korisnik može spremiti materijal, pronaći ga, pročitati povezani članak, vidjeti
podlogu i prethodne procjene, pa izvesti razumljiv paket za drugu osobu ili alat.
Isti podaci ostaju dostupni kada su web server i AI isključeni.

## 13. Sljedeći neposredni coding zadatak

Povijesni F0/F1 zadatak iz početnog plana već je implementiran, a U0 vlasnikovi
odgovori sada su zapisani. Sljedeći rad slijedi U1 u
[produktnom ugovoru](READING_DESK_PRODUCT_DIRECTION.md) i
[John 9 scenariju](JOHN_9_READING_DESK_PILOT.md): minimalni verzionirani ugovor
reader projekcije i privatnih alata, zatim mali povezani tok u postojećem vieweru.
Ne započinjati novi krug istih osam produktnih pitanja.

Prije kodiranja mapirati postojeće identitete, dostupnost teksta, objašnjenje,
njegov točan dokaz i razlog povezane priče. Ne uvoditi novu pohranu zato što
je željen objedinjeni prikaz. Za stvarno nedostajuće highlight/note/suggestion
reference definirati kompatibilni ugovor, trajnost, sukobe i backup obuhvat.
Objasniti prazna/stale/private stanja; koristiti
originalne sintetičke fixture podatke bez novih odobrenja ili proširenja korpusa.

## 14. Referentni standardi za kasnije mapiranje

- W3C PROV: https://www.w3.org/TR/prov-overview/
- RO-Crate: https://www.researchobject.org/ro-crate/specification/1.2/introduction.html

Reference služe za konceptualnu kompatibilnost. Ovaj dokument ne tvrdi PROV ili
RO-Crate usklađenost i ne uvodi obvezne dodatne biblioteke.
