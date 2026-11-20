# Osobna baza znanja: formati 1.0, 2.0 i 3.0

Nova eksplicitna verzija3.0 dodaje trajne nepregledane claim/evidence zapise i
točne povijesne reference. Vidi [v3 specifikaciju](BANK_PERSISTENT_EVIDENCE.md).
Sheme i ponašanje čitanja postojećih1.0/2.0 prostora ostaju verzionirani, bez
automatske migracije. Protokol snimki/locka/HEAD-a opisan za2.0 vrijedi i za3.0.
Prije eventualnog kopiranja pogledati [dry-run ugovor v2→v3](BANK_MIGRATION.md);
trenutno nema migracijske naredbe.

## Implementirani upravljani format 2.0

F2, 2026-11-15: sigurno lokalno pisanje, povijest i oporavak. Raniji opis 1.0
ispod ostaje specifikacija read-only formata; njegova shema nije olabavljena.
Ne postoji automatska migracija 1.0 u 2.0 niti mijenjanje postojeće baze pri čitanju.

```text
<bank-root>/
  workspace.json             # bank-workspace-v2, schema_version 2.0
  HEAD.json                  # transaction_id + manifest_sha256
  .writer.lock               # trajna datoteka, OS drži zaključavanje
  snapshots/<transaction>/
    workspace.json           # isti opis prostora, transportna omotnica 1.0
    records/<id>/record.json # bank-record-v2, schema_version 2.0
    records/<id>/body.md
    manifest.json            # bank-transaction, roditeljski HEAD i hash sadržaja
  staging/                   # nepotpune/pripremljene transakcije i HEAD temp datoteke
```

V2 zapis proširuje omotnicu s revised_at i reason, a parent_revision može biti
ID prethodne revizije. Sve ostalo, uključujući ID-jeve, latinični prikaz i tipove
članak/izvor/predmet, zadržava pravila dolje. created_at je vrijeme nastanka zapisa;
revised_at vrijeme konkretne revizije; recorded_by iskazani akter te revizije.
Prethodni akter i tekst ostaju u prethodnoj snimci. Nema ljudskog approval polja.

### Protokol spremanja

1. Dobiti neblokirajući OS lock. Drugi writer dobiva poruku busy. Ne uklanjati
   .writer.lock: lock se oslobađa zatvaranjem procesa, a datoteka ostaje.
2. Pročitati HEAD jednom i provjeriti cijeli njegov lanac. Edit mora navesti
   točan expected-revision; zastarjeli ulaz ne stvara pripremljenu snimku.
3. Napisati potpunu novu snimku u staging/<novi UUID>, uz flush i file fsync.
   Neizmijenjeni JSON i Markdown bajtovi prenose se nepromijenjeni.
4. Manifest napisati posljednji. On veže raw hash workspacea, raw hashove svih
   record.json datoteka i provjerene hashove tijela. Provjeriti cijelu kandidatsku
   snimku, tipizirane veze i prijelaz iz roditelja prije objave.
5. Preimenovati dovršenu staging mapu u snapshots/<UUID>. Još nije aktualna.
6. Napisati privremeni HEAD u staging i jednim os.replace zamijeniti HEAD.json.
   To je točka vidljivosti nove verzije; ranije snimke writer ne mijenja.

Čitač pamti jednom pročitani HEAD i slijedi samo njegov hash-vezani lanac.
Neaktivne snimke ne ulaze u rezultate. Svaki prijelaz smije promijeniti samo
imenovani zapis: bez brisanja drugih zapisa, ponavljanja revision_id, promjene
kind/id/workspace_id/created_at ili preskakanja parent_revision. Genesis je prazan.
Vrijeme revizije i transakcije ne može ići unazad.

### Oporavak i granice jamstava

recover bez transaction argumenta popisuje neaktivne materijale: prepared kada
su potpuni, provjereni i još odgovaraju HEAD-u; conflict kada je roditelj zastario;
incomplete kada nisu spremni za aktivaciju. Ne briše niti popravlja njihove bajtove.
recover --transaction ponovno provjerava kandidata i, ako roditelj odgovara,
dovršava premještanje i promjenu HEAD-a. Ponavljanje već aktualne transakcije je
idempotentno. Nepotpun zapis se ne dopunjava nagađanjem; ostaje za inspekciju.

Ako naredba vrati grešku nakon zamjene HEAD-a (npr. kvar directory fsync), prvo
pročitati validate/show/history: promjena možda već jest aktualna. Ne ponavljati
create naslijepo. Nema idempotency ključa za create u ovoj fazi.

Init odbija svaku postojeću ciljnu mapu. Prekid nakon pripremljenog genesis
manifesta može se oporaviti. Prekid ranije tijekom stvaranja osnovnih mapa ili
workspace.json nije automatski popravljiv; nepotpun prostor ostaje vidljiv i
ne predstavlja valjanu bazu. Nikakvi postojeći korisnički podaci nisu prepisani.

Lockovi koordiniraju suradničke lokalne procese; ne štite od ručnog mijenjanja
datoteka ili neprijateljskog filesystem procesa. Snimke su nepromjenjive kroz
ovaj writer, a nisu OS read-only ili digitalno potpisane. Hash nije dokaz autorstva.
Ne obećava se otpornost na nestanak napajanja na svakom filesystemu: na POSIX-u
koristi se i directory fsync, na Windowsu nema prijenosne ekvivalentne garancije.
Testirani su procesni prekidi i greške pisanja, ne fizički kvar diska.
Koristiti lokalni filesystem; mrežni/sinkronizirani filesystem nije provjeren.

V2 prvo koristi pune kopije radi jednostavnog oporavka. Ograničenja su128 snimki
u aktivnom lancu i128 MiB zbrojenog history payloada, uz dolje navedene limite
po snimci. Ovo nije konačno skalabilno skladište. Kompakcija još ne postoji.
Dodani su zasebni [backup/verify/restore](BANK_BACKUPS.md) aktivnog lanca, bez
staginga i lock datoteka. Ne brisati povijest radi zaobilaženja limita.

## Sačuvana specifikacija početnog formata 1.0

Implementirano 2026-11-15: strogo read-only čitanje i validacija početnih snapshotova.
Ovo nije novi biblijski knowledge format. Opći razvojni plan je u
[KNOWLEDGE_BANK_IMPLEMENTATION_PLAN.md](KNOWLEDGE_BANK_IMPLEMENTATION_PLAN.md).

## Autoritativni podaci

Zaseban direktorij sadrži točno `workspace.json` i `records/`. Svaki zapis ima
mapu imenovanu svojim stalnim ID-jem, s `record.json` i opcionalnim `body.md`.
Putanja se uvijek zadaje eksplicitno; nema traženja baze po roditeljskim mapama.
Za ovaj početni format druge datoteke i poddirektoriji predstavljaju grešku.
Nikad ne zadavati korijen ovog Git repozitorija kao korijen baze.

```text
<bank-root>/
  workspace.json
  records/
    <uuid4>/
      record.json
      body.md
```

UUID4 je lowercase, bez naslova u identitetu. ID prostora, zapisa i početne
revizije nastaju zasebno. Promjena naslova ne mijenja ID. Svaki record pripada
jednom workspace_id. revision_id je jedinstven u snapshotu.

Workspace sadrži schema_version, workspace_id, title i created_at. Zapis sadrži
schema_version, workspace_id, id, kind, title, created_at, recorded_by,
revision_id, parent_revision, body_sha256, visibility, processing_state i data.
Sheme su isporučene u paketu, pod src/jeb/schemas/bank-*.json.

## Početna revizija i budući writer

Trenutno je parent_revision obvezno null: implementiran je samo početni snapshot.
Validator ne obećava povijest ili transakcijsko pisanje. Ručno izmijenjena datoteka
kojoj je ručno promijenjen hash može ponovno proći; ovo nije potpis niti dokaz
autentičnosti. Ne predstavljati rezultat validacije kao potvrdu istinitosti.

Sljedeća faza treba uvesti verzionirano proširenje formata, očekivanu baznu reviziju,
nepromjenjive prethodne verzije i manifest dovršene transakcije. Ne otpuštati
ograničenje parent_revision bez stvarne provjere lanca povijesti.
Čitači trebaju prepoznavati samo dovršene promjene, a oporavak nakon prekida mora
biti testiran prije rada s vrijednim osobnim podacima. Trenutni format namjerno
ne prihvaća buduće mape history/transactions/proposals.

## Tri vrste zapisa

- entity: data.entity_type je person, place, event, organization, concept ili work.
- source: data čuva source_type, creator, translator, edition, url, accessed_at i
  limitations. Nepoznate vrijednosti su null. limitations je obvezan opis granica.
- article: data.subjects je neprazan popis entity ID-jeva, a data.sources popis
  source ID-jeva. Sve veze moraju postojati u istom snapshotu i imati pravi tip.

Source je u ovoj fazi osnovni bibliografski zapis. Zasebni work/edition/artifact,
tvrdnje, lokatori dokaza i procjene još nisu implementirani. Veza članka prema
izvoru ne dokazuje pojedinu rečenicu u članku. Markdown poveznice nisu automatski
validirane reference i ne pokreću dohvat sadržaja.

## Markdown i podrijetlo

body_sha256 je null kada nema tijela. U suprotnom body.md mora postojati i njegov
SHA-256 mora odgovarati točnim UTF-8 bajtovima, uključujući završetke redaka.
Članak uvijek ima vezano tijelo. Prazno tijelo je dopušteno; semantička kvaliteta
nije predmet ove provjere. Markdown se vraća kao podatak, ne renderira se u HTML.

recorded_by ima id i kind human/agent/tool. To bilježi iskazano podrijetlo, ne
autentificira čovjeka. Nema polja human_attestation niti stvaranja odobrenja.
Datumi su eksplicitni date-time zapisi s vremenskom zonom. Vrijeme događaja i
preciznost povijesnih datuma pripadaju budućem modelu tvrdnji.

Prikazni naslovi, autorski tekst i Markdown moraju poštovati latiničnu granicu
projekta. Izvorni dokument na drugom pismu ostaje privatna evidencija izvan ovog
početnog formata. Nema preslovljavanja niti zamjene svjet/vrjeme/covik/razumit.

## Privatnost, pristup i prava

visibility je private, shared ili public_candidate. processing_state je inbox,
organized ili researched. Nijedno od tih polja nije licencija, odobrenje, dokaz
ili kontrola pristupa. CLI eksplicitno otvara lokalni prostor i može pročitati
privatni zapis; nema web rute, objave, sinkronizacije ili izvoza u ovoj fazi.
Ne stavljati osobni prostor u Git bez prethodne klasifikacije njegovih podataka.

URL je inertna HTTPS referenca bez korisničkih credentials ili whitespacea.
Validator ga ne otvara i ne potvrđuje dostupnost ili prava. Ne spremati tajne
u URL-ove ili metapodatke. SHA-256 potvrđuje identitet bajtova, ne njihovu kvalitetu.

## Operativna ograničenja

Najviše 10.000 zapisa, 1 MiB po datoteci i ukupno 64 MiB učitanih datoteka.
Ovo su zaštitni limiti početnog čitača, ne ciljna veličina buduće baze.
Dupli JSON ključevi, nepoznata polja/verzije, nevaljani tipovi, neispravan UTF-8,
nepovezano tijelo i nepostojeće reference odbijaju se prije uspješnog rezultata.
Symlink i Windows junction putanje odbijaju se. Čitač nije zaštita od napadača
koji istodobno mijenja filesystem između provjere i čitanja; budući writer i
snapshot indeks trebaju riješiti i koordinaciju promjena.
