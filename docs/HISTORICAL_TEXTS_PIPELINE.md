# Historical Texts Pipeline — local processing and dossier queries

Product priority updated 2026-11-19: this pipeline supports the unified reading
and research desk described in
[READING_DESK_PRODUCT_DIRECTION.md](READING_DESK_PRODUCT_DIRECTION.md).
Processing counts and candidate lists are supporting machinery. The next
user-facing milestone is one clear path from book/passage to explanation,
exact evidence and a meaningful related story/character, with a route back.
The owner selected [John 9](JOHN_9_READING_DESK_PILOT.md), equal library/search
entry, desktop side-by-side text/explanation, expandable evidence/connections,
English/Bosnian-Herzegovinian switching and private notes/highlights/suggestions
in the first usable version. Textual witnesses and independent historical evidence
must be distinguishable. These are product requirements, not implemented reader
or note-writing features; current historical query APIs remain read-only.
This note changes priorities, not source gates or proposal statuses.

Ovaj projekt je osobni, lokalni alat za povezivanje knjiga i njihovih svjetova:
djela, izdanja, digitalnih artefakata, likova, osoba, mjesta, događaja, verzija,
motiva i predloženih sličnosti. Nije samo biblijski reader i nije samo claim
baza.

## Pipeline

```text
work → edition → artifact → extraction → entity/relation proposals →
evidence-bound review → dossiers and downstream AI tools
```

Obrada je lokalna, ograničena i nastavljiva. Nedostupan izvor ne zaustavlja druge
izvore: njegov zadatak ostaje `pending` ili `needs_review` s razlogom. Trenutno
je dovršen tok do dossier **prijedloga**; evidence-bound human review i povezivanje
s canonical bankom nisu dio ove implementacije.

## Registry granice

- `work` je apstraktno djelo, ne konkretna datoteka.
- `edition` čuva izdanje, autore/prevoditelje, jezik, verziju i prava.
- `artifact` je konkretan sken, OCR, transkripcija, web-capture ili metadata trag.
- `relation` je prijedlog veze; `similar_to`, `parallel_to` i `same_as_candidate`
  nisu automatska istina.
- V3 bank ostaje sloj za revizije, claim/evidence reference i exact provenance.

Versioned sheme pod `src/jeb/schemas` odvajaju registry, index, groups, dossiers,
extraction cache, pipeline checkpoint i snapshot manifest. One su ugovori za
lokalne podatke, ne prijem izvora u biblijski korpus. `version_of` nastao iz
kataloga ostaje metadata veza; njegovo polje `supported` nije ljudska potvrda
identiteta izdanja ili njegovih prava.

## Kako će raditi unos teme

Ulaz poput `Isus` prvo radi lokalni registry lookup. Rezultat je dossier koji
može povezati MAT/MRK/LUK/JHN, više izdanja i druge bibliotečke radove, ali svaka
veza zadržava izvor, status i nesigurnost. Kod osoba/likova, identitet se ne
spaja tiho; alias, istoimeni lik i teološko tumačenje ostaju odvojeni dok ih
evidence ne podrži.

## Downstream AI alati

Kasniji pipelineovi mogu tražiti `build_dossier`, `find_entities`,
`compare_editions`, `find_parallel_candidates` i `check_claim`. Alat vraća
strukturirane rezultate i evidence locatore, ne slobodan tekst bez porijekla.
Fact-checking i religijsko/duhovno grupiranje daju prijedloge za pregled; ne
donose ljudsko, pravno ili teološko odobrenje.

## Pokretanje izoliranog primjera

Koristi postojeću hash-locked Python 3.13 okolinu iz README-a. Ovaj primjer
stvara vlastiti katalog i izmišljene tehničke rečenice, obrađuje pet zadataka u
malim koracima i izvodi upit za izmišljenu oznaku `Luma`:

```powershell
.\.venv\Scripts\python.exe -m jeb --synthetic historical demo --workspace dist/historical-synthetic-demo
.\.venv\Scripts\python.exe -m jeb --synthetic historical status --workspace dist/historical-synthetic-demo/pipeline
.\.venv\Scripts\python.exe -m jeb --synthetic historical dossier --workspace dist/historical-synthetic-demo/pipeline --query Luma
```

Prva naredba zahtijeva **novu putanju**. Ako direktorij već postoji, koristi
status/upit nad njim ili odaberi novu putanju za demo; nema brisanja ili
prepisivanja postojećeg workspacea. Očekivani red: `complete: 3`, `pending: 1`
(namjerno nedostaje datoteka), `needs_review: 1` (namjerno nevaljan UTF-8).
`Luma` ima četiri lokatora: tri u dvama MAT izdanjima i jedan u MRK izdanju.
Oznake MAT/MRK ovdje su samo testne oznake djela, bez biblijskog teksta.

Demo i sve njegove naredbe zahtijevaju `--synthetic`, čuvaju `synthetic: true`
i `releasable: false` te ne stvaraju ljudske odluke. `--synthetic` smije se
koristiti samo za vlastite izmišljene fixture podatke, nikad za zaobilaženje
prava stvarnog artefakta.

## Inkrementalna obrada i oporavak

Za odvojenu provjeru koraka može se uzeti registry i izmišljene input datoteke
iz prethodnog demoa. Ciljni workspace opet mora biti nov:

```powershell
.\.venv\Scripts\python.exe -m jeb --synthetic historical pipeline init --registry dist/historical-synthetic-demo/registry.json --root dist/historical-synthetic-demo/inputs --workspace dist/historical-synthetic-steps
.\.venv\Scripts\python.exe -m jeb --synthetic historical pipeline step --workspace dist/historical-synthetic-steps --max-artifacts 1 --max-seconds 5
.\.venv\Scripts\python.exe -m jeb --synthetic historical pipeline status --workspace dist/historical-synthetic-steps
```

Ponovi `step` dok `queued` i `processing` ne budu nula. `--max-artifacts`
prihvaća 1–100 (zadano 4), a `--max-seconds` više od 0 do 60 (zadano 10).
Budžet se provjerava prije svakog zadatka, a PDF proces dobiva preostali timeout.
Čitanje/obrada teksta u Pythonu, validacija, grupiranje, pisanje snapshota i ostali
završni poslovi mogu produžiti ukupno trajanje; to nije hard wall-clock limit.

- Prije i poslije svakog artefakta piše se atomski `pipeline.json` checkpoint.
  OS lock odbija drugog istodobnog writera. Prekinuti `processing` zadatak
  ponovno se obrađuje pri sljedećem `step` pozivu.
- Dovršena ekstrakcija ide u hash-addressed `cache/`. Snapshot u `snapshots/`
  veže četiri sloja i njihove ekstrakcije. `HEAD.json` mijenja se tek kada su
  sve datoteke novog snapshota zapisane. Stari snapshoti ostaju sačuvani.
- Ako objava ne uspije nakon checkpointa, posljednji snapshot ostaje čitljiv.
  Status prijavljuje `publication_pending: true`; sljedeći `step` koristi
  dovršeni cache bez ponovne ekstrakcije i pokušava objaviti snapshot.
- `--retry-pending` ponovno pokušava `pending` i `needs_review` zadatke nakon
  popravka dostupnosti/datoteke. `--refresh` ponovno provjerava dovršene inpute;
  nepromijenjeni UTF-8 izvori koriste cache. Pokušaji se rotiraju da jedan izvor
  ne zauzme svaku malu rundu. Queued/prekinuti poslovi imaju prednost.

Registry se kopira pri inicijalizaciji i hash-veže na checkpoint. Promijenjeni
katalog/registry zahtijeva **novi workspace**, bez tihe migracije. Izvorni input
se ne prepisuje. Novi sadržaj stvara novi cache/snapshot, uz očuvanje staroga.
Workspace ne prihvaća symlink/junction putanje; relativni put artefakta ne smije
izaći iz input roota.

Primjer ponovnog pokušaja i osvježavanja:

```powershell
.\.venv\Scripts\python.exe -m jeb --synthetic historical pipeline step --workspace dist/historical-synthetic-steps --retry-pending --max-artifacts 2
.\.venv\Scripts\python.exe -m jeb --synthetic historical pipeline step --workspace dist/historical-synthetic-steps --refresh --max-artifacts 2
```

## Lokatori i granice ekstrakcije

`.txt` i `.md` čitaju se kao strogi UTF-8, bez promjene CRLF-a ili Unicode
znakova. PDF koristi postojeći lokalni `pdftotext` ako je dostupan; alat se ne
instalira ni preuzima. Provenance bilježi SHA-256 izvornih bajtova i projekcije,
vrstu projekcije te adapter (za PDF i hash izvršne datoteke). Rasponi su
`[start, end)` u **Unicode code pointovima**, ne UTF-8 bajtovima ili JavaScript
UTF-16 indeksima. PDF lokatori odnose se na `pdftotext_utf8`, bez izmišljenog
broja stranice. Novi managed pipeline zadržava točne PDF projekcijske bajtove
prema ugovoru ispod; stariji v1 cachevi i odvojeni `entity-index` builder i dalje
imaju samo hash, bez zadržane projekcije.

Kapitalizirani latinični tokeni ostaju `entity_type: unknown`, `status: proposed`.
NFC/whitespace/casefold služe samo za grupni ključ; izvorni zapis i dijakritika
ostaju u površinskim oblicima i lokatorima. To nije NER klasifikacija, alias,
transliteracija ili dokaz da ista oznaka u različitim djelima znači istu osobu.

Granice: 16 MiB input/projekcija, 10.000 kandidata po artefaktu, 100.000 ukupno,
5.000 pipeline zadataka, 64 MiB po sloju i 128 MiB za četiri snapshot sloja.
Jedan snapshot dodatno može referencirati najviše 128 MiB jedinstvenih zadržanih
projekcija. Isti hash broji se jednom. Stari snapshoti/cachevi i nepotpuno
zapisane nereferencirane datoteke nemaju automatsko brisanje ili ukupnu disk kvotu.
Nevaljan UTF-8, nedostupan PDF adapter, prevelik input/projekcija, krivi hash,
timeout i nepodržan format imaju razloge po artefaktu. HTML/OCR/slike nemaju
adapter; nedostatak teksta nikad se ne popunjava iz memorije.

## Trajno zadržana sintetička PDF projekcija — v2

Novi uspješni PDF zadatak u managed workspaceu piše:

```text
projections/<projection_sha256>.txt    exact UTF-8 bytes, including CRLF/form feed
cache/<cache_sha256>.json             historical-extraction-v2 metadata + candidates
snapshots/<snapshot_id>/manifest.json reference to that immutable cache hash
```

V2 cache ima `schema_version: "2.0"`, `synthetic: true`, `releasable: false` i
`projection_file` s hashom i veličinom. Putanja se izvodi iz provjerenog hasha;
cache ne može zadati proizvoljnu putanju. Bajtovi se pišu atomski prije cachea,
complete checkpointa i objave HEAD-a. Postojeći blob s drugim sadržajem ne
prepisuje se. Kvar pisanja ostavlja `processing` checkpoint i prethodni snapshot,
pa se posao može ponovno pokušati. Nereferencirani blob nakon prekida nije dokaz
da je zadatak dovršen.

Čitanje v2 cachea provjerava schema, cache hash, projection hash/veličinu, strogi
UTF-8 i svaki doslovni kandidat kroz `text[start:end] == surface`. Nedostajuća,
prevelika, izmijenjena ili nevaljana projekcija zaustavlja upit. Čitanje ne
pokreće `pdftotext`, ne otvara trenutni PDF i ne pokušava popraviti dokaz.
Hash PDF alata provjerava se prije i nakon ekstrakcije; promjena alata tijekom
obrade ostaje `needs_review/adapter_changed_during_projection`.

Query provenance sada uključuje `extraction_cache_sha256`, `projection_retained`
i `locator_verification`. Vrijednost `retained_projection` znači da su rasponi
uspoređeni sa zadržanim bajtovima; ne potvrđuje PDF page alignment, povijesnu
vjernost, identitet osobe ili ljudski review. PDF candidate ID sada uključuje i
hash projekcije, tako da drukčiji tekst na istom offsetu nije ista ekstrakcijska
pojava. Plain-text ID-evi ostaju u dosadašnjem obliku.

Stari `historical-extraction-v1`, checkpoint i snapshot ugovori ostaju
nepromijenjeni. Novi reader čita v1 i v2; čitanje ne migrira ni reseala stare
datoteke. V1 provenance označen je `projection_retained: false` i
`locator_verification: not_retained`. Eksplicitni `step --refresh` može stvoriti
novi v2 cache iz trenutno dostupnog sintetičkog PDF-a; on ne popunjava stari
cache i ne rekonstruira izgubljenu projekciju. Za nove v2 zapise sačuvaj i
odgovarajući engine; stariji engine ne razumije novi extraction ugovor.

Za provjeru starog ili aktualnog cachea koristi samo read-only CLI:

```powershell
$pdfWorkspace = 'dist/historical-projection-synthetic-2026-11-19/pipeline'
$pdfHead = Get-Content (Join-Path $pdfWorkspace 'HEAD.json') -Raw | ConvertFrom-Json
$pdfManifest = Get-Content (Join-Path $pdfWorkspace "snapshots/$($pdfHead.snapshot_id)/manifest.json") -Raw | ConvertFrom-Json
$pdfCacheHash = $pdfManifest.extractions[0].cache_sha256
.\.venv\Scripts\python.exe -m jeb --synthetic historical projection-verify --workspace $pdfWorkspace --cache-sha256 $pdfCacheHash
```

Navedena putanja je lokalni originalni PDF smoke primjer zabilježen u PROGRESS-u;
za vlastiti fixture postavi njegov managed workspace. U naredbu možeš umjesto
aktualnog hasha unijeti sačuvani stari `extraction_cache_sha256` iz dossier-a ili
starog manifesta. Rezultat sadrži hashove, veličinu i broj provjerenih kandidata,
bez ispisivanja cijelog teksta. V1 vraća `projection_not_retained` i exit 2,
bez tihog dohvaćanja PDF-a. Nema HTTP rute za puni tekst projekcije.

Zadržava se tekstualna projekcija, ne cijeli izvorni PDF, fontovi ili OCR dokaz.
Izvorni SHA-256 identificira PDF bajtove, ali ih ne arhivira. Ovo ostaje isključivo
sintetički, izolirani, unreleasable tok; stvarni izvori i dalje zahtijevaju zaseban
neimplementirani admission ugovor i postojeće rights/review gates.

## CLI i read-only API

Python paket sadrži sve provjere i upite; Node bridge samo prilagođava GET
zahtjev CLI-ju. Ne postoji poziv model API-ju ili automatska AI obrada.

| CLI `historical ...` | GET endpoint | Sadržaj |
| --- | --- | --- |
| `status` | `/api/historical/status` | counts, blockers, queue i snapshot |
| `dossiers` | `/api/historical/dossiers` | filtrirani sažeci prijedloga |
| `detail --id ...` | `/api/historical/dossier/<id>` | izdanje, krediti, provenance i lokatori |
| `lookup --query ...` | `/api/historical/lookup` | broj pojava po djelu, bez višestrukog brojanja |
| `relations` | `/api/historical/relations` | metadata/relation prijedlozi |
| `dossier --query ...` | `/api/historical/build-dossier` | objedinjeni dossier za temu ili djelo |

Naredbe primaju `--workspace` i, za demo, globalni `--synthetic`. Upitni
argumenti su `--query` (API `q`), `--work`, `--status`, `--availability`,
`--relation`, `--limit`, `--offset`, `--locator-limit` i `--locator-offset`
(u API-ju zadnja dva koriste underscore). Dossier traži temu ili djelo. Limit
je najviše 1.000 za sažetke, 100 za lookup/combined i 500 za relations; detalji
imaju do 100 lokatora, combined do 20 po entitetu. Sources detalji prikazuju
najviše 50 artefakata uz eksplicitni `sources_truncated`.

`total`/`*_total`, `offset` i `truncated` opisuju stranice. Works, entities i
relations u combined odgovoru koriste isti offset/limit nad svojim nizovima.
Odgovor veći od 4 MiB vraća `response_limit_exceeded`; smanji limit ili broj
lokatora i ponovi **isti offset**, umjesto da tiho preskočiš retke.

`proposal_only: true`, `authoritative: false` i `releasable: false` ostaju
obavezni u upitima. Relacije u combined dossieru imaju
`selection_basis: work_context`: veza pripada djelu, nije dokaz tvrdnje o
traženom liku. Nepoznata tema daje prazne rezultate, ne tuđe relacije.

Status `ready` znači da se slojevi mogu usklađeno čitati; ne znači da je red
prazan ili da je izvor odobren. `integrity: verified` provjerava dostavljene
slojeve/snapshot, ne prava ili stvarni identitet entiteta. Svaki workspace upit
veže rezultate i status na jedan pročitani HEAD. Queued/status podaci mogu
odražavati checkpoint koji još čeka objavu; to pokazuje `publication_pending`.

Stale hash vraća `stale_pipeline_inputs` (HTTP 409); nevaljan JSON/schema,
konfiguracijski sukob ili workspace daje `invalid_historical_input` (422), uz
logički sloj i bez privatne putanje. Nevaljan upit daje 400, nepostojeći ID 404,
a nedostupan Python ili zauzet bridge 503. Upitne CLI greške izlaze kodom 2.
`status` ispisuje blockers kao dijagnostiku, bez promjene podataka.

## Lokalni viewer

Nakon izrade demoa, u PowerShellu bez starih četiriju `JEB_HISTORICAL_*` layer
putanja postavi:

```powershell
$env:JEB_HISTORICAL_WORKSPACE = (Resolve-Path dist/historical-synthetic-demo/pipeline).Path
$env:JEB_HISTORICAL_SYNTHETIC = '1'
npm run dev
```

Otvori `http://127.0.0.1:5187`, zatim **Entiteti i svjetovi**. Upiši `Luma`,
po želji filtriraj `MAT` i otvori dossier. Popis ima paginaciju; osvježavanje
statusa samo ponovno čita snapshot i ne pokreće obradu. Za daljnje lokatore
koristi CLI/API pagination argumente. Viewer ostaje loopback, GET-only,
isključen bez konfiguracije i bez merge/approval/write/export operacija.

Postojeći layer-file način i dalje prima `JEB_HISTORICAL_REGISTRY`,
`JEB_HISTORICAL_INDEX`, `JEB_HISTORICAL_GROUPS`, `JEB_HISTORICAL_DOSSIERS`.
CLI prima odgovarajuće `--registry/--index/--groups/--dossiers`. Nedostajući
sloj navodi se eksplicitno; stale hashovi se provjeravaju i kod djelomične
konfiguracije. Bez ekstrakcijskog workspacea nema dodatnih source/projection
hashova iz cachea. Ne kombiniraj layer-file način s `--workspace`/workspace
environment varijablom; takva konfiguracija se odbija.

## Stvarni izvori i provjere

Metadata registry može se izgraditi bez čitanja sadržaja:

```powershell
.\.venv\Scripts\python.exe -m jeb historical registry-build --input library/catalog.json --output dist/historical-registry.json
```

Bez `--synthetic`, ekstrakcija stvarnog artefakta trenutno uvijek ostaje
`needs_review: source_review_required` **prije otvaranja izvora**. Ni private
status ni provider label ne otključavaju obradu. Stariji istraživački broj od
18.230 kandidata nije cleared corpus i ne koristi se kao demo input. Budući
stvarni adapter treba zasebno rights/edition review povezivanje; taj put još
nije implementiran. `entity-index/entity-groups/entity-dossiers` ostaju dostupni
kao odvojeni builderi, uz istu ekstrakcijsku granicu.

Offline provjere iz korijena repozitorija:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_historical -v
npm run test:web
```

Python testovi koriste isključivo izmišljene privremene podatke. Projection
testovi pokrivaju byte/UTF-8/span provjere, stare cacheve, deduplikaciju, granice,
kvar pisanja i nepromijenjene stare snapshote. Jedan test gradi vlastiti mali PDF
bez novih ovisnosti i stvarno koristi lokalni `pdftotext` ako je instaliran; samo
taj test preskače se kad alat nedostaje. Ostali PDF testovi koriste stubove.
Pokreni ih s `python -m unittest tests.test_historical_projection -v`.
HTTP testovi stvarno stvaraju neprazan sintetički pipeline
Python CLI-jem, provjeravaju CLI/API paritet, točne kredite/lokatore, stale i
malformed greške te nepromijenjene checkpoint/HEAD bajtove nakon GET upita.
Provjere ne zahtijevaju povijesni tekst ili mrežu. Puni Ruff,
schema i unittest skup ostaje naveden u README-u.

## Sigurnosne granice

Nema popunjavanja povijesnog teksta iz memorije, automatskog rights clearancea,
silent transliterationa, tihog spajanja različitih likova ili automatske odluke
da su dva izvora „ista”. Sintetički demo ostaje izoliran, označen i
unreleasable. Biblijski produkcijski opseg ostaje GEN/MAT/MRK/LUK/JHN.
