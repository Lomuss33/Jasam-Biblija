# Privatne sigurnosne kopije baze znanja

Implementirano 2026-11-15 za upravljane formate 2.0 i 3.0. Backup, provjera i restore
rade offline kroz isti Python paket/CLI. Nije potrebno biblijsko Project okruženje.
Format3.0 koristi zaseban bank-backup-v3 descriptor i njegove sheme; stare2.0
sheme/hashovi ostaju isti. Trajni v3 claim/evidence zapisi i vezana povijest su
uključeni, dok vanjski F3A draft paketi i dalje nisu. Vidi BANK_PERSISTENT_EVIDENCE.md.

## Naredbe

```powershell
.venv/Scripts/python.exe -m jeb bank backup --bank-root C:/moja-baza --output D:/kopije/moja-baza-2026-11-15.zip
.venv/Scripts/python.exe -m jeb bank backup-verify --input D:/kopije/moja-baza-2026-11-15.zip
.venv/Scripts/python.exe -m jeb bank restore --input D:/kopije/moja-baza-2026-11-15.zip --destination C:/vracena-baza
.venv/Scripts/python.exe -m jeb bank validate --bank-root C:/vracena-baza
```

Roditeljske mape trebaju postojati. Backup mora biti izvan bank-root prostora.
Postojeća izlazna datoteka ili odredišna mapa odbijaju se, čak i ako je mapa prazna.
Nema overwrite opcije. Restore ne mijenja izvornu bazu niti arhivu. Vraćena baza
ima iste identitete, HEAD i revizije, pa podržava daljnji normalan create/edit.

## Što je obuhvaćeno

- Točni bajtovi workspace.json i HEAD.json.
- Sve snimke u lancu jednom pročitanog aktualnog HEAD-a, od genesisa do danas.
- Manifesti snimki, svi metapodaci i sva vezana Markdown tijela u tom lancu.
- backup.json s hashom i veličinom svake datoteke te identitetima relevantnih shema.

Izostavljeni su staging, lock datoteke, neaktivne snimke i lokalni privremeni
HEAD fajlovi. Kopija nije cijeli Git projekt: ne uključuje library/private,
vanjske knjige, URL odredišta, budući media object store ili proizvoljne datoteke.
Čuvanje poveznice nije čuvanje njezina sadržaja. Verzija 1.0 se ne migrira i
nije podržana ovim backup naredbama.
Izdvojeni bank evidence nacrti/paketi također nisu dio potvrđenog lanca:
čuvaju se zasebno. Njihova provjera nakon restorea koristi točno vraćenu bazu.

Arhiva je **privatna, nešifrirana kopija**. Uključuje i ranije privatne tekstove
iz povijesti. visibility public_candidate ne pretvara je u javni izvoz niti daje
prava na distribuciju. Ne slati arhivu drugima kao odabranu javnu temu. Za takvu
razmjenu tek treba implementirati odvojene projekcije i export profile.

## Izrada i provjera

Backup drži isti neblokirajući OS writer lock kao edit: drugi writer dobiva busy,
a čitanje može nastaviti. Time suradnički writer ne može pomaknuti HEAD tijekom
kopiranja. Podaci se pišu u privremenu mapu uz odabrani output. Prije objave
ponovno se provjerava arhiva i iz nje rekonstruira cijela baza u izoliranoj mapi.

Izlaz se objavljuje atomskim hard-linkom koji ne može zamijeniti postojeći fajl.
Privremeni fajl je na istom filesystemu. Ako filesystem ne podržava hard link,
operacija vraća grešku; nema slabijeg fallbacka koji bi mogao prepisati podatke.
Ako objava uspije, a naknadni fsync/checksum ne uspije, output može već postojati:
provjeri ga s backup-verify prije ponovnog pokušaja s drugim nazivom.

Provjera obuhvaća allowlist putanja, jedinstven popis, file size, CRC/dekompresiju,
SHA-256 svake datoteke, schema identitete, unutarnje manifeste i cijeli niz revizija.
Ponovno zapečaćeni vanjski popis ne može sakriti neslaganje unutarnjih snapshot
hashova. To nije potpis: netko tko promijeni sve podatke i hashove može stvoriti
drugu strukturno valjanu bazu. Provjera ne dokazuje povijesne činjenice ili prava.

## Vraćanje i prekidi

Prvo se cijela arhiva provjeri u privremenom direktoriju. Tek nakon uspjeha
restore ekskluzivnim mkdir rezervira novo odredište. Pod novim writer lockom
kopira podatke, a HEAD objavljuje posljednji. Ne pokušava atomsku zamjenu
postojeće mape. Sve dotad ne postoji čitljiva potvrđena verzija te nove baze.

Kod obrađene greške uklanjaju se samo poznati fajlovi i prazne mape koje je ovaj
restore stvorio. Nema rekurzivnog brisanja proizvoljnog direktorija. Neočekivani
sadržaj ili symlink/junction zaustavlja čišćenje i ostaje za inspekciju.
Postojeće odredište, uključujući mapu stvorenu konkurentnim procesom, ostaje netaknuto.

Nagli izlazak procesa ili nestanak napajanja može ostaviti nepotpuno novo odredište
ili privremenu mapu. Ne predstavljati to kao uspješan restore; ponovno provjeri
arhivu i odaberi drugo novo odredište. Nema automatskog nastavka djelomičnog
restorea, zamjene aktivne baze ili povratka HEAD-a na stariju procjenu. Privremene
izdvojene kopije također mogu sadržavati privatni tekst. Pri normalnom završetku
privremene mape se čiste. Granice lokalnog filesystema i power-loss jamstava iz
BANK_FORMAT.md ostaju na snazi.

## Limiti i kompatibilnost

- 50.000 payload datoteka i jedan backup.json.
- 1 MiB po payload datoteci, 16 MiB za backup.json.
- Ukupno 130 MiB payload podataka i 160 MiB fizičke ZIP arhive.
- Ostaju limiti upravljane povijesti:128 snimki i128 MiB history payloada.
- ZIP32, stored/deflate, bez lozinke, ZIP komentara ili direktorijskih stavki.
- Symlinkovi, posebne datoteke, putanje izvan allowliste i duplikati se odbijaju.
- Broj i duljine central-directory stavki provjeravaju se prije ZIP alokacija.

Kopija veže hashove šest relevantnih isporučenih shema. Ako se one razlikuju,
alat odbija vraćanje; čuvaj odgovarajući instalacijski wheel i hash-locked
okruženje uz dugoročne kopije. Nema automatske migracije ili prešućivanja razlika.
Ovo ne veže svaku liniju engine koda i ne obećava proizvoljnu buduću kompatibilnost.

Kopija na istom disku pomaže kod pogrešne izmjene, ali ne rješava kvar tog diska.
Ove naredbe ništa ne šalju niti raspoređuju: raspored, drugi medij i eventualna
enkripcija ostaju korisnikov operativni izbor. Povremeno provjeri stvarni restore
u novu mapu; sama prisutnost ZIP fajla nije dokaz upotrebljive sigurnosne kopije.

## Testovi

```powershell
.venv/Scripts/python.exe -m unittest tests.test_bank_backup -v
```

Originalni offline testovi provjeravaju točne bajtove i ranije revizije nakon
restorea, praznu bazu, nastavak pisanja, izostavljanje neaktivnog privatnog rada,
oštećene arhive, metadata/HEAD/schema neslaganja, prepisivanje i race situacije,
opasne ZIP stavke, zaštitne limite i čišćenje nakon djelomičnog pisanja.
