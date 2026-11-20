# Ugovor za budući v2→v3 dry-run

Ovaj dokument definira granicu prije bilo kakvog alata za kopiranje. Trenutno
ne postoji naredba koja migrira bazu. Dostupna je samo read-only naredba koja
izrađuje plan. Čitanje v2 baze i dalje je read-only, a
`bank init --format 3.0` stvara novi prazan prostor.

```powershell
.venv/Scripts/python.exe -m jeb bank migrate-plan `
  --bank-root C:/moja-baza-v2 `
  --output D:/planovi/moja-baza-v2-to-v3.json
```

Izlaz mora biti izvan `bank-root`, a postojeća datoteka se ne prepisuje.

Spremljeni plan se može ponovno provjeriti prije bilo kakvog budućeg writer
koraka:

```powershell
.venv/Scripts/python.exe -m jeb bank migrate-plan-verify `
  --bank-root C:/moja-baza-v2 `
  --input D:/planovi/moja-baza-v2-to-v3.json
```

Provjera uspijeva samo ako se workspace ID, HEAD manifest i digest trenutnih
zapisa točno podudaraju s planom. Nakon bilo kojeg novog commita plan je stale i
mora se ponovno generirati.

## Cilj i nepromjenjivi ulazi

Migracija bi kasnije mogla napraviti novu lokalnu mapu formata3.0 iz valjanog
upravljanog prostora2.0. U dry-run fazi ne piše se cilj, izvor, Git, arhiva niti
vanjski draft paket. Izvorni `workspace.json`, `HEAD.json`, sve aktivne snimke,
body datoteke i postojeći backup ostaju bajtovski nepromijenjeni. Dry-run ne
stvara claim/evidence zapise i ne čita F3A packet kao kandidata za uvoz.

Ulaz se prvo učita i validira kao cijeli committed chain s trenutnim readerom.
Neaktivne snimke, staging, lockovi, proizvoljne datoteke, legacy1.0 i prostor
drugog workspacea odbijaju se. Bilo koja greška zaustavlja izvještaj prije
planiranja kopija.

## Eksplicitna mapa identiteta

Svaki postojeći record zadržava isti `record_id`, `kind`, `created_at`,
`workspace_id` i sve postojeće `revision_id` vrijednosti. Svaka povijesna
revizija dobiva novi3.0 transportni zapis samo ako se njezini podaci mogu
validno prekodirati. Budući da se mijenja envelope `schema_version`, ciljna
`record.json` hash vrijednost može biti nova; izvještaj zato čuva izvorni raw
hash uz eksplicitni identity map. `body_sha256` i bajtovi `body.md` ostaju isti.
`parent_revision` se ne smije preskočiti ili preusmjeriti.

Plan mora sadržavati redak za svaki v2 record, u stabilnom kronološkom redoslijedu:

```json
{
  "record_id": "<uuid>",
  "kind": "entity|source|article",
  "source_revision_ids": ["<uuid>"],
  "target_record_id": "<isti uuid>",
  "target_revision_ids": ["<isti uuid redoslijed>"],
  "action": "copy",
  "blockers": []
}
```

Nema skraćenih ID-jeva, implicitnog uparivanja po naslovu ili prepisivanja
tekstualnog sadržaja. Ako v2 zapis ne prolazi strožu3.0 provjeru, akcija je
`blocked`, ciljna polja ostaju prazna, a izvještaj navodi točan razlog.

## Izvještaj dry-runa

Izvještaj bi bio deterministički JSON izvan obje baze, bez tijela izvora i bez
novih odobrenja:

```json
{
  "report_version": "1.0",
  "mode": "dry_run",
  "source_format": "2.0",
  "target_format": "3.0",
  "source_workspace_id": "<uuid>",
  "source_head": {"transaction_id": "<uuid>", "manifest_sha256": "<hash>"},
  "source_records_sha256": "<hash>",
  "counts": {"copy": 0, "blocked": 0, "claims": 0, "evidence": 0},
  "records": [],
  "external_inputs": {"f3a_packets": "excluded"},
  "approvals_created": 0,
  "writable": false
}
```

`source_head` i `source_records_sha256` sprečavaju da se plan kasnije predstavi
kao plan za drugu bazu. Ako se izvor promijeni, plan se mora ponovno napraviti;
ne postoji nastavak koji bi automatski presložio identitete.

## Što ovaj ugovor još ne odlučuje

Ne odlučuje hoće li vlasnik uopće prihvatiti novu bazu, kako se rješavaju ručni
konflikti, kako se uvoze F3A paketi, niti daje ljudsko odobrenje. Za F3A treba
poseban ugovor koji čuva originalni packet hash, točan v2 HEAD i odluku vlasnika.
Ne smije se nagađati da draft claim odgovara novom3.0 claimu, niti se smije
automatski dodijeliti `review_state` osim početnog `unreviewed` za eksplicitno
napisani novi zapis.

Tek nakon zasebnog pregleda ovog izvještaja može se razmatrati writer koji stvara
novu mapu, provjerava cijeli lanac i objavljuje novi HEAD. Taj budući writer ne
smije prepisivati postojeću mapu, postojeću arhivu ili već postojeći cilj.

## Dizajn reviewed writera

Decision zapis ima shemu `bank-migration-decision-v1` i provjerava se read-only
naredbom:

```powershell
.venv/Scripts/python.exe -m jeb bank migrate-decision-validate `
  --bank-root C:/moja-baza-v2 `
  --plan D:/planovi/moja-baza-v2-to-v3.json `
  --input D:/odluke/moja-baza-v2-to-v3-decision.json
```

Validator provjerava shemu, ljudskog owner aktera, hash plana, source HEAD,
workspace i digest zapisa, odsutnost blokera, isključenost F3A paketa i to da je
ciljna putanja izvan izvora i još ne postoji. Rezultat je samo provjera veze;
`approvals_created` je uvijek `0` i ne nastaje ciljna mapa.

Za razvojni test postoji samo eksplicitna sintetička simulacija:

```powershell
.venv/Scripts/python.exe -m jeb bank migrate-simulate `
  --synthetic `
  --bank-root C:/sinteticka-v2 `
  --plan C:/planovi/sinteticka.json `
  --input C:/odluke/sinteticka-decision.json
```

Simulacija zahtijeva `--synthetic`, ciljnu putanju čije ime sadrži
`synthetic`, dodaje oznaku `[SYNTHETIC MIGRATION]` u naslov i vraća
`releasable:false`. Kopira povijest u novi3.0 lanac i validira ga privatno, ali
ne predstavlja stvarnu migraciju, odobrenje ili izvor očišćen za objavu.

Writer smije biti zasebna naredba tek nakon što vlasnik izvan alata pregleda
plan. Njegov ulaz mora biti:

1. valjan plan učitan iz vanjske datoteke;
2. trenutni v2 `bank-root`;
3. unaprijed nepostojeći ciljni direktorij;
4. zaseban, ljudski potpisan ili ručno potvrđen decision zapis koji navodi
   `source_workspace_id`, `source_head`, `source_records_sha256`, točan hash
   plana, ciljnu putanju, datum i identitet vlasnika.

Alat ne smije sam stvoriti taj decision zapis, pretpostaviti da je korisnik
vlasnik ili pretvoriti `approval_authority: none` u odobrenje. Ako decision
zapis nedostaje, ima drugi HEAD/hash, navodi blocked zapis ili uključuje F3A
packet, writer mora stati prije stvaranja ciljne mape.

Objava bi imala četiri odvojena koraka:

1. ponovno zaključati i validirati cijeli izvorni lanac;
2. ponovno usporediti plan i decision s tim istim HEAD-om;
3. izgraditi potpunu ciljnu3.0 mapu u sibling staging direktoriju, uključujući
   sve povijesne snimke, prekodirane record omotnice i nepromijenjene body bajtove;
4. validirati cilj privatno, zatim ga objaviti jednim no-clobber renameom na
   ranije rezerviranu novu putanju.

Izvorni v2 prostor i arhiva ne smiju biti odredište renamea. Prekid prije objave
smije ostaviti samo označeni staging materijal koji se može sigurno ukloniti ili
pregledati; ne smije promijeniti HEAD izvora. Nakon objave writer treba vratiti
sažetak s ciljanim workspace ID-jem, HEAD-om, brojem zapisa, brojem blokera
`0` i nula novostvorenih odobrenja.
