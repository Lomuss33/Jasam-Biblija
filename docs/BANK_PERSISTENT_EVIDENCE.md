# Trajne tvrdnje i dokazi: upravljani format 3.0

Implementirano 2026-11-15. Nova, eksplicitno odabrana verzija podržava entity,
source, article, claim i evidence zapise kroz isti writer, povijest i oporavak.
Trajno spremljeno ne znači pregledano ili istinito: claim/evidence imaju isključivo
review_state unreviewed. Ne stvaraju se ljudska odobrenja ili procjene.

## Nova baza i postojeći podaci

```powershell
.venv/Scripts/python.exe -m jeb bank init --bank-root C:/moja-baza-v3 --title "Moja baza znanja" --format 3.0
```

Bez --format zadana vrijednost ostaje2.0. Init odbija postojeći direktorij.
Postojeće1.0/2.0 baze, njihove sheme i sigurnosne kopije nisu promijenjene niti
nadograđene pri čitanju. Još nema migration/copy naredbe ili uvoza vanjskog
evidence paketa. V2 ne prima nove claim/evidence vrste. Reference su lokalne
istom prostoru i ne mogu upućivati na proizvoljnu drugu bazu.

U V3 svaka snimka koristi bank-record-v3 i bank-transaction-v3, vanjski workspace
bank-workspace-v3. Raspored snapshot/staging/HEAD ostaje kao u2.0. Unutarnji opis
prostora u snimci i dalje koristi strogu transportnu omotnicu1.0; to nije migracija.
Nema miješanog2.0/3.0 lanca. Limiti pune povijesti ostaju128 snimki/128MiB.

## Točna referenca

```powershell
.venv/Scripts/python.exe -m jeb bank reference --bank-root C:/moja-baza-v3 <record-id>
.venv/Scripts/python.exe -m jeb bank reference --bank-root C:/moja-baza-v3 <record-id> --revision <revision-id>
```

Izlaz sadrži record_id, revision_id, raw record.json SHA-256 i body_sha256 ili
null. Bez --revision vraća aktualnu reviziju; uz argument mora postojati baš ta
revizija u potvrđenoj povijesti tog zapisa. Ne birati po naslovu ili skraćenom hashu.

## Claim i evidence ulazi

Create/edit imaju ista obvezna polja kind, title, data, visibility i
processing_state te eksplicitnog aktera i razlog. Za claim:

- data.subject je točna referenca na raniju entity reviziju;
- data.statement je tekst tvrdnje;
- data.category je source_statement, historical_claim, interpretation,
  personal_reflection ili fiction;
- data.limitations i review_state unreviewed su obvezni.

Za evidence:

- data.claim je točna referenca na raniju claim reviziju;
- data.source je točna referenca na raniju source reviziju;
- relation je supports, contradicts, contextualizes ili mentions;
- locator ima tip text_span/page/section/time_range kao u BANK_EVIDENCE.md;
- rationale, limitations i review_state unreviewed su obvezni.

Claim/evidence nemaju dodatni body.md: sav strukturirani sadržaj je u data.
Ne koristiti --body za njih. Izvorni tekst može biti vezan uz source zapis.

Referenca mora biti već potvrđena prije transakcije koja je koristi. Validator
gradi registar revizija kronološki, razrješava nove veze samo prema ranijim
commitovima i uspoređuje sva četiri polja reference. Nedostajuće, pogrešnog tipa,
strane, samoreferencijalne i buduće reference ne prolaze. Ne traži se uvijek
najnovija revizija: to bi izbrisalo značenje povijesnog dokaza.

## Kada se podloga promijeni

Naknadno uređivanje source zapisa ne mijenja evidence. Njegov locator i dalje
se provjerava prema točnoj starijoj body reviziji. Čak i ako aktualni izvor više
nema body, stariji doslovni raspon ostaje provjerljiv iz povijesti.

Naknadno uređivanje claim zapisa ne prenosi stare evidence veze na novu tvrdnju.
Nova evidence revizija može se eksplicitno vezati uz novi claim nakon pregleda
podloge, uz sačuvan prethodni zapis i razlog promjene. Nema automatskog rebindanja.

```powershell
.venv/Scripts/python.exe -m jeb bank evidence links --bank-root C:/moja-baza-v3 <claim-id>
```

Izvještaj navodi aktualne evidence zapise za identitet tvrdnje, njihove točne
reference i odnos. applies_to_current_claim označava odgovara li claim revizija
aktualnoj tvrdnji. source_revision_matches_current označava je li korišten aktualni
ili povijesni izvor. local_text_match potvrđuje samo doslovni raspon; ostali
lokatori ostaju declared_only. Nijedna zastavica ne određuje istinitost ili
prednost među dokazima. Supports i contradicts mogu istodobno postojati.

Links prikazuje aktualne evidence glave, ne sve njihove prošle odnose. Za stare
evidence/claim revizije koriste se history, diff i reference --revision. Nema
odabira najbolje tvrdnje, prihvaćanja, povlačenja ili korisničkog sučelja u ovoj fazi.

## Izvršiv originalni primjer

Ovo je izmišljeni tehnički tekst, nije historijski dokaz. Privremena mapa ostaje
za inspekciju; podaci su privatni i nisu odobreni za objavu.

```python
import tempfile
from pathlib import Path
from jeb.bank import backup, references, storage
from jeb.bank.validation import validate_bank

base = Path(tempfile.mkdtemp(prefix="jeb-bank-v3-example-"))
root = base / "bank"
storage.initialize(root, "Originalni probni v3 prostor, nije historijski izvor", "3.0")
common = {"visibility": "private", "processing_state": "inbox"}
def save(kind, title, data, body=None):
    return storage.save_record(root, {**common, "kind": kind, "title": title, "data": data},
                               "example-tool", "tool", "Originalni tehnicki primjer", body)
def ref(item):
    return references.record_reference(root, item["id"], item["revision_id"])

subject = save("entity", "Probni predmet", {"entity_type": "concept"})
body = "svjet vrjeme covik razumit\n"
source = save("source", "Originalni probni tekst", {
    "source_type": "document", "creator": "Autor tehnickog primjera",
    "translator": None, "edition": "Originalno probno izdanje", "url": None,
    "accessed_at": None, "limitations": "Izmisljeni test, nije historijski dokaz.",
}, body)
claim = save("claim", "Probna tvrdnja", {
    "subject": ref(subject), "statement": "Probni tekst pocinje rijecju svjet.",
    "category": "source_statement", "limitations": "Samo tehnicki primjer.",
    "review_state": "unreviewed",
})
item = save("evidence", "Probna potpora", {
    "claim": ref(claim), "source": ref(source), "relation": "supports",
    "locator": {"type": "text_span", "start": 0, "end": 5, "exact": "svjet"},
    "rationale": "Doslovni raspon u originalnom probnom tekstu.",
    "limitations": "Ne potvrdjuje historijsku cinjenicu.", "review_state": "unreviewed",
})
print(validate_bank(root))
print(references.evidence_links(root, claim["id"]))
backup.create(root, base / "bank-v3.zip")
backup.restore(base / "bank-v3.zip", base / "restored")
assert references.evidence_links(root, claim["id"]) == references.evidence_links(base / "restored", claim["id"])
print(base)
```

## Kopije, draft paketi i kompatibilnost

Backup/backup-verify/restore automatski biraju strogi descriptor prema verziji
izvorne baze. V3 koristi bank-backup-v3 i šest odgovarajućih schema hashova.
V2 descriptor i njegovih šest hashova ostaju isti. Sve stare granice privatnosti,
no-clobber, točnih bajtova, opasnih ZIP stavki i novog restore cilja ostaju.
V3 backup uključuje trajne claim/evidence zapise i njihove potrebne revizije,
jer su dio potvrđenog lanca. Vanjski nacrti nisu dio te kopije.

F3A evidence prepare/validate/inspect i dalje radi samo s bazom2.0; paket deklariran
za2.0 ne smije se neprimjetno pripremiti nad3.0. Nema uvoza starog paketa ili
novog owner review postupka u ovom koraku. Dodavanje trajnih zapisa nije njihovo
odobravanje i ne mijenja prava izvora ili biblijski korpus.

## Provjere

```powershell
.venv/Scripts/python.exe -m unittest tests.test_bank_persistent_evidence -v
```

Testovi su offline i izvorno napisani: trajne veze, promjene izvora i tvrdnje,
eksplicitne nove evidence revizije, krive reference/hashovi/lokatori, zabrana
odobrenja, v2 granice, v3 backup/restore, prekid/recover i CLI pregled.
