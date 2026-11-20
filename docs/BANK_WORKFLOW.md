# Početni rad s bazom znanja

Za trajne tvrdnje/dokaze u novoj bazi sada postoji izričiti `init --format 3.0`,
`bank reference` i `bank evidence links`. Vidi [trajni v3 model](BANK_PERSISTENT_EVIDENCE.md).
Postojeći prostori se ne nadograđuju automatski.

Za izdvojene nacrte tvrdnji, odnose potpore/proturječja i lokatore sada postoje
`bank evidence prepare/validate/inspect`. Vidi [dokaze i primjer](BANK_EVIDENCE.md).
To ne dodaje claim/evidence vrste u upravljani format2.0 i nije human review.

U istom instalabilnom paketu i CLI-ju sada postoje init/create/edit, history/diff,
recover te validate/show s eksplicitnim --bank-root. Dodani su backup,
backup-verify i restore: vidi [sigurnosne kopije](BANK_BACKUPS.md). Restore i
provjera kopije koriste --input, a restore i --destination. Stari 1.0 primjeri
ostaju read-only. Novi writer radi samo s upravljanim formatom 2.0.

## Novi prostor i prvi zapis

Odaberi novu mapu izvan javnog repozitorija. Njezin roditeljski direktorij mora
postojati; init odbija postojeći cilj.

```powershell
.venv/Scripts/python.exe -m jeb bank init --bank-root C:/moja-baza --title "Moja baza znanja"
```

Pripremi ulazni JSON (npr. C:/unos.json), bez ID-jeva i revizijskih polja:

```json
{
  "kind": "entity",
  "title": "Moj istraživački pojam",
  "data": {"entity_type": "concept"},
  "visibility": "private",
  "processing_state": "inbox"
}
```

```powershell
.venv/Scripts/python.exe -m jeb bank create --bank-root C:/moja-baza --input C:/unos.json --actor vlasnik --actor-kind human --reason "Dodajem svoj istrazivacki pojam"
```

actor-kind je iskaz podrijetla, ne autentifikacija i ne odobrenje. Agent koristi
agent ili tool, ne human. Rezultat sadrži id, revision_id i HEAD. Za članak ulaz
ima kind article te data.subjects i data.sources; --body upućuje na UTF-8 Markdown.
Za source slijediti obvezna polja bank-record-v2 sheme, uključujući nepoznate null
vrijednosti i limitations. Referencirani zapisi moraju već postojati u toj bazi.

## Izmjena i pregled povijesti

Edit prima potpunih istih pet ulaznih polja kao create. Ako nema --body, nova
revizija nema tijelo: kod entity/source to uklanja prethodno opcionalno tijelo,
a kod article je nevaljano. Za očuvanje postojećeg tijela predati njegovu datoteku.
Ne radi se o parcijalnom patchu. Vrsta zapisa ne može se promijeniti.

```powershell
.venv/Scripts/python.exe -m jeb bank edit --bank-root C:/moja-baza <id> --expected-revision <revision-id> --input C:/unos.json --actor vlasnik --actor-kind human --reason "Dopunjujem opis"
.venv/Scripts/python.exe -m jeb bank history --bank-root C:/moja-baza <id>
.venv/Scripts/python.exe -m jeb bank diff --bank-root C:/moja-baza <id> --from-revision <stari-id> --to-revision <novi-id>
```

Konflikt traži ponovno čitanje i usporedbu; ne koristi se sila ili automatski merge.
History vraća točne zapise i tekstove revizija, najstarije prvo. Diff vraća odvojeni
tekstualni diff metapodataka i tijela.

## Prekinuto spremanje

```powershell
.venv/Scripts/python.exe -m jeb bank recover --bank-root C:/moja-baza
.venv/Scripts/python.exe -m jeb bank recover --bank-root C:/moja-baza --transaction <transaction-id>
```

Prva naredba samo izvještava pod writer lockom; druga eksplicitno aktivira provjereni
prepared kandidat čiji roditelj još odgovara HEAD-u. Nepotpune i konfliktne snimke
ostaju sačuvane. Nema automatskog biranja kandidata, brisanja ili vraćanja HEAD-a.
Ako je sam aktualni HEAD/povijest oštećen, recover odbija rad umjesto nagađanja.

## Čitanje i validacija

```powershell
.venv/Scripts/python.exe -m jeb bank validate --bank-root C:/putanja/do/baze
.venv/Scripts/python.exe -m jeb bank show --bank-root C:/putanja/do/baze <record-uuid>
```

Nije potrebna biblijska config mapa. bank-root je obvezan i mora biti zaseban
direktorij u [podržanom formatu](BANK_FORMAT.md). Bank naredbe ne učitavaju Project,
ne mijenjaju sources/lock.json, ne primaju knjige i ne pišu nikakva odobrenja.
Uspjeh vraća JSON i exit 0; nevaljani ulaz poruku na stderr i exit 2 bez success
payloada. show prvo provjerava cijeli prostor pa tek onda vraća traženi zapis.

validate vraća broj zapisa i vezanih tijela te hash uređene liste metapodataka.
To nije arhiva ni kriptografski potpis: hash veže i deklarirane hashove tijela,
koji se zasebno provjeravaju na disku. Naredba nikad ne popravlja ili prepisuje.

## Originalni read-only probni primjer za format 1.0

Sljedeći mali primjer stvara novu privremenu bazu izvan repozitorija, s jednim
izmišljenim pojmom i člankom. Nije povijesni izvor niti ljudsko odobrenje.
Pokrenuti Python blok u instaliranom hash-locked okruženju:

```python
import tempfile
from pathlib import Path
from uuid import uuid4
from jeb.core import canonical, sha256
from jeb.bank.validation import validate_bank

root = Path(tempfile.mkdtemp(prefix="jeb-bank-example-"))
workspace = str(uuid4())
when = "2026-11-15T10:00:00Z"
(root / "records").mkdir()
(root / "workspace.json").write_bytes(canonical({
    "schema_version": "1.0", "workspace_id": workspace,
    "title": "Originalni primjer", "created_at": when,
}))

def add(kind, title, data, body=None):
    identity = str(uuid4())
    directory = root / "records" / identity
    directory.mkdir()
    record = {
        "schema_version": "1.0", "workspace_id": workspace, "id": identity,
        "kind": kind, "title": title, "created_at": when,
        "recorded_by": {"id": "example-tool", "kind": "tool"},
        "revision_id": str(uuid4()), "parent_revision": None,
        "body_sha256": None if body is None else sha256(body.encode("utf-8")),
        "visibility": "private", "processing_state": "inbox", "data": data,
    }
    (directory / "record.json").write_bytes(canonical(record))
    if body is not None:
        (directory / "body.md").write_bytes(body.encode("utf-8"))
    return identity

subject = add("entity", "Probni pojam", {"entity_type": "concept"})
article = add("article", "Probni članak", {"subjects": [subject], "sources": []},
              "# Probni članak\n\nOriginalan tehnički primjer bez historijskih tvrdnji.\n")
print(root)
print(article)
print(validate_bank(root))
```

Mapa namjerno ostaje za ručni pregled. Nije uključena u sigurnosnu kopiju ovog
repozitorija. Za stvaran rad sljedeći korak je siguran writer s poviješću;
ne koristiti ručno mijenjanje ID-jeva i hashova kao zamjenu za taj postupak.

## Provjere

```powershell
.venv/Scripts/python.exe -m unittest tests.test_bank -v
.venv/Scripts/python.exe -m ruff check src tests
.venv/Scripts/python.exe -m ruff format --check src tests
.venv/Scripts/python.exe -m jeb validate --stage schemas
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

Testni primjeri nastaju u privremenim mapama i ne koriste postojeće privatne knjige.
Puni plan, uključujući pisanje, povijest, dokaze, pretragu, sučelje, agente i
izvoz, ostaje u [planu implementacije](KNOWLEDGE_BANK_IMPLEMENTATION_PLAN.md).
