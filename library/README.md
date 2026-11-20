# Osobna istraživačka biblioteka

Vlasnikov zahtjev od 2026-11-14: pronaći i uredno spremiti navedene knjige,
uz jezični prioritet **hercegovački/regionalni → bosanski → hrvatski →
crnogorski → srpski na latinici**. Biblioteka je zasebna od izdanja
GEN/MAT/MRK/LUK/JHN. Ne mijenja konfiguraciju kolekcije, source lock,
urednička odobrenja, pravila prava niti sadržaj sintetičkog primjera.

## Otvori biblioteku

Iz korijena projekta pokreni `npm run dev`, zatim otvori
http://127.0.0.1:5187/#collection. Nije potreban npm install. Dostupni su
pretraga naslova/autora/prevodilaca, filtri zbirke i statusa, podaci o izdanju,
izvorne poveznice i odvojeni nepotvrđeni tragovi pretrage.

## Šta je sačuvano

- `requested-books.md`: svih **291 stavki u 14 skupina**, s vlasnikovim naslovima
  i atribucijama. Atribucije nisu predstavljene kao nezavisno potvrđene činjenice.
- `catalog.json`: izvedeni inventar sa zasebnim stabilnim ID-jem za svaku stavku.
  Istoimeni izbori/pisma/haiku različitih autora nisu spojeni.
- `findings.json`: **153 pregledana nalaza za 138 stavki**. Pregledan nalaz može
  biti stranica prvog poglavlja, indeks, izbor ili kataloški zapis, ne nužno puna
  knjiga. Cjelovitost i kvalitet prijevoda nisu time potvrđeni.
- `research/searches.json`: **73 početne pretrage sa po najviše četiri upita**,
  ukupno 291 upit i 1,595 pohranjenih rezultatskih poveznica. Rezultati su skupni
  za upite u istoj grupi, ne automatski dodijeljeni pojedinom djelu. Ima šuma,
  stranih jezika i nepovezanih djela; to nisu potvrđena izdanja ni preporuke.
  Naslovi u drugim pismima imaju neutralnu latiničnu oznaku uz izvorni URL;
  nisu preslovljeni niti se prikazuju kao odabrani latinični prijevodi.
- `research/downloads.json`: zapis stvarnog privatnog preuzimanja, URL, veličina,
  SHA-256, prevodilac i domaćinova izričita oznaka besplatne distribucije.
- `private/dhammapada-veljacic.html`: originalni puni HTML sa Srednjeg puta,
  **236,222 bajta**, SHA-256
  `45a11d52548e9b7a189f9e431616dcb68a601a1c4e45b6beb3dae18e15a3b72c`.
  Prevod i uvod Čedomil Veljačić. Domaćin navodi „Samo za besplatnu distribuciju,
  kao dar Dhamme”. Datoteka sadrži i navigaciju weba; nije samostalni EPUB/PDF,
  nije kolacionirana s tiskanim izdanjem i nije corpus input. Sačuvani izvorni
  HTML može upućivati na udaljene resurse; nije izvršavan ni javno poslužen.

Privatna mapa je ignorirana u Gitu i nije dostupna kroz lokalni web server.
Katalog sadrži putanju kopije; original se može pregledati iz datoteka projekta.
Druga privatna kopija je `private/samkhya-antic-2017.pdf`: Ivan Antić, 2017.,
810182 bajta; receipt i SHA-256 u `research/downloads.json`. Osuvremenjena
prilagodba preko engleskih izvora, s dopuštenjem lične upotrebe bez izmjena.
Izdavački uzorak Upanišada ostaje samo dokaz sadržaja, bez tekstova upanišada.
Detalji: [treći pregled](research/batch-03-review.md).
Treća i četvrta kopija: Suttanipāta2022. i Udāna2019., prijevod s palija
Branislav Kovačević, javno ponuđeni PDF-ovi za besplatnu distribuciju. Putanje,
veličine i SHA-256 u `research/downloads.json`; obje ostaju pod `private/evidence/`.
Provjera: [osmi pregled](research/batch-08-review.md). Peta kopija je zajednički
PDF Udāna/Itivuttaka2022., računat jednom pod Itivuttakom. Krediti i hash:
[deveti pregled](research/batch-09-review.md). Ukupno pet privatnih datoteka izdanja.
Domaćinova oznaka distribucije sačuvana
je kao dokaz opsega pristupa, ne kao univerzalna pravna dozvola ili odobrenje objave.

## Kako tumačiti statuse

Najnovije: [šesnaesti pregled, dvadeset naslova 146–165](research/batch-16-review.md).
Šesnaest novih nalaza za petnaest novih stavki; Mesnevija i Hafizov Divan
dopunjeni bez duplikata. Tri cilja još bez potvrđenog nalaza. Pet privatnih
datoteka; bez novih punih preuzimanja. Izbori i nepotvrđena cjelovitost označeni.

Prethodno: [petnaesti pregled, dvadeset naslova 126–145](research/batch-15-review.md).
Sedamnaest novih nalaza za šesnaest stavki, od kojih je petnaest ranije bilo
bez nalaza. Četiri cilja ostaju otvorena. Musonije je časopisni izbor, Senekina
Pisma zasad samo prvi svezak. Pet privatnih datoteka; bez novih punih preuzimanja.

Prethodno: [četrnaesti pregled, dvadeset naslova 106–125](research/batch-14-review.md).
Petnaest novih nalaza za petnaest stavki, uključujući tri autora u jednoj
haiku antologiji, Takuanov uzorak i grčka djela. Pet ciljeva još nema potvrđen
nalaz. Ukupno pet privatnih datoteka; nema novih punih lokalnih kopija.

Prethodno: [trinaesti pregled, dvadeset naslova 086–105](research/batch-13-review.md).
Devet novih nalaza za osam stavki: kineska i japanska djela, uz odvojene
edicije, izbore i jedan izdavački uzorak. Dvanaest ciljeva još nema potvrđen
nalaz; nema novih punih lokalnih kopija. Ukupno pet privatnih datoteka.

Drugi pregled: [Pirkei Avot i gnostički spisi](research/batch-02-review.md).
Osam novih nalaza potvrđuje samo unos u sadržaju; jedan potvrđuje početni ulomak.
Ti nalazi nisu predstavljeni kao potpuna identificirana izdanja.

- **Privatna kopija spremljena**: postoji zapis o stvarnom preuzimanju. Katalog
  nije provjera prisutnosti datoteke na drugom računalu; provjeri receipt i hash.
- **Online čitanje**: pregledana je poveznica na tekst/indeks. Ne tvrdi se da je
  svaka stranica dostupna ili da je knjiga potpuna.
- **Izdanje identificirano**: postoji konkretan katalog ili izdavačka stranica;
  može zahtijevati posudbu/kupnju. Kupnja nije obavljena.
- **Online ulomak**: pregledan je samo dio traženog djela.
- **Sadržaj pronađen · izdanje otvoreno**: spis je naveden u pregledanom sadržaju,
  ali identitet tiskanog izdanja/prevodioca nije potvrđen; nije puna knjiga.
- **Nalazi čekaju pregled**: upit je izvršen, ali relevantno izdanje nije
  potvrđeno. To nije dokaz da prijevod ne postoji.

Prvi krug pretrage koristio je kombinirane jezične pojmove radi otkrivanja.
Nije sistematski iscrpio svaki od pet jezičnih prioriteta za svako djelo.
Nijedno izdanje nije označeno kao konačno odabrani ili najbolji prijevod.
Oznaka regionalnog jezika iz pregledanog teksta ostaje opis procjene, ne nova
urednička norma. Prazna jezična polja nisu popunjena iz zemlje izdavanja.
Ćirilični i drugi neprikladni nalazi ostaju nepotvrđeni tragovi; nema preslovljavanja.

Posebno razlikovati cijelo djelo od izbora (npr. Kerubinski putnik), komentirano
izdanje od izvornog teksta (Bhagavad-gītā kakva jest) i zbirku od pojedinog spisa
(Koptski gnostički tekstovi). Ne preuzimati zbirku pod pretpostavkom da sadrži
svaki traženi naslov. Više mrežnih kopija nije više nezavisnih prijevoda.

## Održavanje

Uređuj pregledane nalaze u `findings.json`, zatim pokreni:

```text
npm run library:catalog
npm run test:web
```

`build-catalog.mjs` rekonstruira samo izvedeni katalog iz popisa, nalaza i zapisa
pretrage; nema mrežnih poziva niti pisanja u jeb podatke. Za novu istraživačku
stavku dodaj je na kraj postojeće skupine samo uz plan očuvanja ID-jeva: trenutni
ID-jevi ovise o redoslijedu popisa. Nemoj preuređivati postojeće retke.

`download-dhammapada.mjs --private` je zaseban, eksplicitan jednokratni download
tačno navedene stranice. Postojeću datoteku/receipt odbija prepisati. Nije dio
pokretanja servera ni automatskog pribavljanja drugih knjiga.

Četvrti pregled: [četiri vedantska djela](research/batch-04-review.md).
Peti pregled: [četiri indijska djela](research/batch-05-review.md).
Šesti pregled: [Bhartrhari i Bijak](research/batch-06-review.md); zbirni
prijevod još traži potvrdu obuhvata i pisma, Bijak ima samo ulomak uvoda.
Sedmi pregled: [Vačane i džainističke sutre](research/batch-07-review.md).
Za te četiri stavke nije potvrđen regionalni prijevod; broj nalaza nije povećan.
Osmi pregled potvrdio je dvije edicije Matišićine Pančatantre i spremio dva PDF-a;
Hitopadeša ostaje neriješena. Deveti pregled spremio je Itivuttaku i potvrdio
da su online Theragatha/Therigatha izbori. Sljedeće: Milindapanha i tri
Nagarjunina djela. Mundaka, puni
Pirkei Avot i Himna biseru ostaju otvoreni, kao i cjelovite verzije petog pregleda.
Potvrditi tačne sadržaje zbirki i provjeravati jezične prioritete. Puni prijevod
traži odvojenu provjeru od članka o njemu. Bez automatskog javnog dijeljenja.
Dvanaesti pregled: [zen/chan spisi](research/batch-12-review.md).
Dva izdanja Huangboa i Oshov komentar; Platforma/Linji ostaju otvoreni.
Sljedeće: Vrata bez vrata, Dao de jing, Zhuangzi i Liezi.

Jedanaesti pregled: [Bodhicaryavatara i sutre](research/batch-11-review.md).
Tri nova kandidata, bez novih punih kopija; Vimalakirti ostaje otvoren.
Sljedeće: Sutra platforme, Xinxin Ming, Huangbo i Linji.

Deseti pregled: [Milindapanha i Nagarjuna](research/batch-10-review.md).
Milindapanha je skraćena verzija; Ratnavali PDF završava na400; potvrđen je
bibliografski trag za prvo poglavlje Temeljnih strofa. Pismo prijatelju ostaje otvoreno.
