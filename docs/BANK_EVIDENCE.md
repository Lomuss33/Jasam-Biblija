# Nacrti tvrdnji i dokaza: F3A

Naknadno je implementiran zasebni trajni format3.0: [F3B upute](BANK_PERSISTENT_EVIDENCE.md).
Ovaj F3A paket ostaje vezan uz2.0 i nije prešutno nadograđen ili uvezen u3.0.
Odjeljak o budućem formatu dolje čuva izvorni ugovor; trajno spremanje je sada
implementirano, dok uvoz/migracija i ljudska procjena još nisu.

Implementirano 2026-11-15: izdvojeni paketi koji vežu tvrdnje, predmet i dokaze
uz točnu potvrđenu snimku upravljane baze 2.0. Paket ima svoj format 1.0.
Ovo nije primanje novih vrsta zapisa u bazu, ljudski pregled ili dokaz istinitosti.

## Naredbe

```powershell
.venv/Scripts/python.exe -m jeb bank evidence prepare --bank-root C:/moja-baza --input C:/rad/tvrdnje.json --output C:/rad/paket.json --actor vlasnik --actor-kind human
.venv/Scripts/python.exe -m jeb bank evidence validate --bank-root C:/moja-baza --input C:/rad/paket.json
.venv/Scripts/python.exe -m jeb bank evidence inspect --bank-root C:/moja-baza --input C:/rad/paket.json
```

Sve radi offline i bez biblijskog Project okruženja. Actor je stvarni pripremač
ili alat; AI koristi agent/tool, nikad human reviewer. Paket je uvijek unreviewed
i approval_authority none. Priprema ne mijenja bank workspace, HEAD ili zapise.
Output mora biti nova datoteka izvan upravljane baze, s postojećim roditeljem.
Postojeći output se ne prepisuje; objava koristi no-clobber hard link.

## Ulaz i značenje

Draft ima schema_version 1.0, neprazni claims popis i evidence popis koji može
biti prazan. Svaka tvrdnja ima:

- id: novi lowercase UUID4, jedinstven među svim tvrdnjama i dokazima paketa;
- subject_id: postojeći entity zapis u ovoj bazi;
- statement: navod koji se želi dokumentirati;
- category: source_statement, historical_claim, interpretation,
  personal_reflection ili fiction;
- limitations: eksplicitne granice, nepoznanice ili napomena o izvornosti testa.

Svaki evidence zapis ima id, claim_id, source_id, relation, locator, rationale i
limitations. Source mora biti source zapis, a claim_id jedna od tvrdnji u draftu.
Odnos je supports, contradicts, contextualizes ili mentions. Različiti odnosi
ostaju sačuvani: alat ne izabire pobjednika niti pretvara tumačenje u činjenicu.
Claim/evidence ID-jevi ne smiju se sudariti s identitetima bank zapisa.

Tvrdnje bez ikakve evidence veze vraćaju se u claims_without_evidence.
Postojanje supports veze nije potvrda da dokaz doista podupire zaključak.
Source_statement opisuje što izvor kaže; historical_claim je navod o prošlosti.

## Lokatori

| type | Obvezna polja | Što je stvarno provjereno |
| --- | --- | --- |
| text_span | start, end, exact | Doslovni tekst u lokalno vezanom source body.md |
| page | pdf_page, printed_page, note | Struktura; barem jedan page podatak nije null |
| section | label, note | Struktura i neprazna oznaka odjeljka |
| time_range | start_ms, end_ms, note | Struktura, nenegativan početak i kraj nakon početka |

Text span je poluotvoreni interval [start,end) izražen Python Unicode codepoint
indeksima, ne UTF-8 bajtovima ili vizualnim grafemima. Broje se iz točnog body.md
teksta nakon UTF-8 dekodiranja, bez LF/CRLF ili Unicode normalizacije. exact mora
doslovno odgovarati rasponu; lokalni body je već vezan svojim SHA-256 hashom.
Takav lokator dobiva local_text_match, ali ostaje nepregledan dokaz.

PDF stranica je pozitivni broj; printed_page je odvojena tekstualna oznaka,
npr. iv ili 17. Odjeljci, stranice i vremenski intervali dobivaju declared_only:
u bazi još nema vezanog PDF/audio/video artifact objekta koji bi ih verificirao.
Ne tvrdi se da stranica postoji, da je PDF pregledan ili da je snimka preslušana.
Ne izmišljati OCR, citat ili vrijeme kako bi lokator prošao validaciju.

## Vezivanje i zastarjelost

Paket sadrži workspace_id, base_head, datum, pripremača, kopiju drafta, schema
hashove i sortirane bindings. Svaki binding veže record_id, revision_id, raw
record.json SHA-256 i body_sha256 ili null. Metapodaci izdanja i prevodioca ne
kopiraju se nagađanjem: inspect vraća točne vezane source zapise iz baze.
Cijeli envelope, uključujući točan tekst tvrdnji, veže packet_sha256.

Validate i inspect zahtijevaju da base_head i svi binding podaci odgovaraju
uhvaćenoj aktualnoj snimci. Svaka promjena HEAD-a, čak i nepovezanog zapisa,
čini paket zastarjelim. Nema allow-stale prekidača ili automatskog rebindanja.
Nakon novog pregleda podloge može se eksplicitno pripremiti novi paket pod novim
imenom. Raniji paket ostaje sačuvan kao radni trag, ali nije aktualno verificiran.

Priprema i čitanje koriste nepromjenjivu snimku, bez writer locka. Ako drugi
proces u međuvremenu spremi promjenu, pripremljeni paket može odmah postati
zastario. Rezultat se odnosi na točno uhvaćeni HEAD, ne na globalni trenutak.
Hashovi nisu digitalni potpisi i ne autentificiraju autora ili dokaz.

## Privatnost i sigurnosne kopije

Paket i inspect rezultat mogu sadržavati privatne navode, citate i bibliografiju.
Nisu šifrirani niti javni izvozi. Spremljeni tekst je podatak, nikakve upute se
ne izvršavaju i URL-ovi se ne otvaraju. Ne dodavati pakete automatski u Git.

Bank backup i dalje čuva samo potvrđeni 2.0 lanac; ovi vanjski radni paketi
nisu uključeni. Čuvati ih zasebno uz podlogu. Paket nije samostalan prenosivi
paket svih dokaza: validate/inspect trebaju odgovarajuću bazu i aktualni HEAD.
Nakon točnog restorea te baze isti vanjski paket ostaje provjerljiv.

Limiti: 1 MiB po ulaznoj/izlaznoj datoteci, najviše100 tvrdnji,500 evidence veza
i600 vezanih zapisa. Polja imaju dodatne shematske limite. Ne mijenjati ih radi
prolaska stvarnog sadržaja bez zasebne procjene potreba i provjera.

## Izvršiv originalni primjer

Ovaj primjer koristi izmišljeni tehnički tekst; nema historijskog navoda, stvarnog
owner odobrenja ili dopuštenja za objavu. Privremena mapa ostaje za ručni pregled.

```python
import tempfile
from pathlib import Path
from uuid import uuid4
from jeb.bank import evidence, storage
from jeb.core import canonical

base = Path(tempfile.mkdtemp(prefix="jeb-evidence-example-"))
root = base / "bank"
storage.initialize(root, "Originalni tehnicki primjer, nije historijski izvor")
common = {"visibility": "private", "processing_state": "inbox"}
subject = storage.save_record(root, {
    **common, "kind": "entity", "title": "Probni pojam",
    "data": {"entity_type": "concept"},
}, "example-tool", "tool", "Originalni probni predmet")
body = "Probni zapis.\nsvjet vrjeme covik razumit\n"
source = storage.save_record(root, {
    **common, "kind": "source", "title": "Originalni probni dokument",
    "data": {"source_type": "document", "creator": "Autor tehnickog primjera",
             "translator": None, "edition": "Probno prvo izdanje", "url": None,
             "accessed_at": None, "limitations": "Izmisljeni test, nije historijski dokaz."},
}, "example-tool", "tool", "Originalni probni izvor", body)
claim_id = str(uuid4())
start = body.index("svjet")
draft = {
    "schema_version": "1.0",
    "claims": [{"id": claim_id, "subject_id": subject["id"],
                "statement": "Probni dokument sadrzi rijec svjet.",
                "category": "source_statement", "limitations": "Samo tehnicki primjer."}],
    "evidence": [{"id": str(uuid4()), "claim_id": claim_id, "source_id": source["id"],
                  "relation": "supports",
                  "locator": {"type": "text_span", "start": start,
                              "end": start + len("svjet"), "exact": "svjet"},
                  "rationale": "Doslovni raspon u originalnom probnom tekstu.",
                  "limitations": "Ne potvrdjuje nikakav historijski dogadjaj."}],
}
input_path, packet_path = base / "draft.json", base / "packet.json"
input_path.write_bytes(canonical(draft))
print(evidence.prepare(root, input_path, packet_path, "example-tool", "tool"))
print(evidence.validate(root, packet_path))
print(base)
```

## Ugovor prije buduće promjene formata baze

F3A ne mijenja bank-workspace-v2, bank-record-v2, bank-transaction ili bank-backup
sheme. Te sheme i postojeći backup hashovi ostaju isti. Claim/evidence su lokalni
ID-jevi unutar paketa, vezani njegovim hashom, a nisu kanonski bank record ID-jevi.

F3B treba zasebno implementirati eksplicitnu novu verziju koja podržava trajne
claim/evidence zapise. Prije koda definirati: exact-revision reference za tvrdnju
i izvor, rješavanje povijesnih revizija bez tihog prijelaza na aktualnu, provenance
uvoza paketa, impact izvještaj i pravila validacije/backup za novu verziju.
Postojeće baze ne mijenjati pri čitanju; nikad samo proširiti enum u v2 shemi.
Ako će biti potreban prijenos v2 podataka, napraviti dry-run i zaseban novi cilj
uz sačuvanu staru bazu i eksplicitno mapiranje identiteta. Taj prijenos još ne postoji.

Procjene, prihvaćanje, povlačenje i odabir najbolje potpore dolaze nakon trajnog
modela. Iz ovog koraka se ne izvodi ljudska recenzija ili automatska istinitost.

## Provjere

```powershell
.venv/Scripts/python.exe -m unittest tests.test_bank_evidence -v
```

Testovi rade offline s originalnim podacima: rasponi/CRLF/UTF-8 indeksi, pogrešni
lokatori i tipovi, dupli/sudareni ID-jevi, zastarjelost, izmijenjeni hashovi i
revizije, nedopuštena approval polja, siguran output i provjera nakon bank restorea.
