# Pilot teme: katolička Biblija

Ovo je početni okvir za osobnu knowledge banku. Ne sadrži prepisani biblijski
tekst, ne proglašava izvore očišćenima i ne dodjeljuje odobrenja.

Produktna dopuna 2026-11-19: pilot treba služiti jasnom čitateljskom toku —
knjiga/odlomak, kontekst i objašnjenje, točan dokaz, povezani lik/priča i povratak.
Svih osam odgovora sada je zapisano u
[reading-desk ugovoru](READING_DESK_PRODUCT_DIRECTION.md), a odabran je
[John 9 scenarij](JOHN_9_READING_DESK_PILOT.md). Uključuje usporedno čitanje i
objašnjenje, dvojezični preklop, odvojene vrste dokaza i privatne bilješke,
isticanja i predložene veze u prvoj uporabljivoj verziji.
Početni CLI unos ispod ostaje tehnički alat; nije cilj svakodnevnog
čitanja. Ova dopuna ne odabire novo izdanje, tumačenje ili dodatnu knjigu.

## Početni dopušteni opseg

Trenutni projektni opseg dopušta ovih pet pilot-knjiga:

| ID | Radni naziv | Status |
|---|---|---|
| GEN | Postanak | planned |
| MAT | Matej | planned |
| MRK | Marko | planned |
| LUK | Luka | planned |
| JHN | Ivan | planned |

Za svaku knjigu baza može imati `entity` zapis knjige, `source` zapise izdanja
i prijevoda, zatim zasebne `entity` zapise glavnih likova. Lik nije automatski
činjenica: claim o liku treba imati evidence koji pokazuje točan izvor i lokator.

## Model jednog lika

```text
entity: osoba
  title: naziv prikaza
  data.entity_type: person

claim: tvrdnja o osobi
  subject: točna revizija entity zapisa
  category: source_statement | historical_claim | interpretation
  review_state: unreviewed

evidence: veza prema izvoru
  claim: točna revizija claim zapisa
  source: točna revizija source zapisa
  relation: supports | contradicts | contextualizes | mentions
  locator: text_span | page | section | time
```

`historical_claim` se ne smije tretirati kao potvrđena činjenica samo zato što
postoji u bazi. Contradicting evidence ostaje vidljiv uz supporting evidence;
baza ne bira istinu automatski.

## Knjige izvan pilota

Ostale knjige katoličkog kanona nisu dodane u ovaj opseg. Njihov status je
`pending_owner_scope_decision`. Dodavanje knjige traži zasebnu vlasničku odluku
s datumom i tekstom odluke, zatim odvojeni pregled schema/code promjene.
Cross-reference, bibliografska napomena ili archive član ne predstavljaju takvu
odluku.

## Prvi praktični tok

```powershell
$bank = 'C:\moja-katolicka-biblija'
.venv/Scripts/python.exe -m jeb bank init --bank-root $bank --title 'Katolička Biblija · osobna baza' --format 3.0
.venv/Scripts/python.exe -m jeb bank search --bank-root $bank --query Matej
.venv/Scripts/python.exe -m jeb bank validate --bank-root $bank
```

Prvi stvarni unos treba početi od točnog izdanja ili drugog provjerljivog source
zapisa. Bez sourcea se može napraviti samo privatni inbox/entity zapis, ne i
claim koji se predstavlja kao potvrđena činjenica.
