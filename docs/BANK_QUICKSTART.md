# Brzi početak osobne baze znanja

Ovo je lokalna, privatna i read-only web projekcija baze. Python CLI je mjesto
za promjene; viewer služi za pretragu i čitanje.

## 1. Napravi bazu

```powershell
$bank = 'C:\moja-baza-znanja'
.venv/Scripts/python.exe -m jeb bank init `
  --bank-root $bank `
  --title 'Moja baza znanja' `
  --format 3.0
```

Format3.0 je potreban za trajne claim/evidence zapise. Zadani format ostaje2.0
ako želiš samo entity/source/article zapise.

## 2. Dodaj zapis

`create` prima JSON datoteku s točno ovim poljima:

```json
{
  "kind": "entity",
  "title": "Aleksandar Veliki",
  "data": {"entity_type": "person"},
  "visibility": "private",
  "processing_state": "inbox"
}
```

```powershell
.venv/Scripts/python.exe -m jeb bank create `
  --bank-root $bank `
  --input .\entity.json `
  --actor lovro `
  --actor-kind human `
  --reason 'Početni unos teme'
```

Za source zapis dodaj `--body .\izvor.md`; body ostaje vezan hashom uz revision.
Ne unositi tekst iz izvora ako prava, izdanje ili porijeklo nisu provjereni.

## 3. Pretraži i otvori

```powershell
.venv/Scripts/python.exe -m jeb bank search `
  --bank-root $bank `
  --query Aleksandar

.venv/Scripts/python.exe -m jeb bank validate --bank-root $bank
```

Viewer je samo za čitanje:

```powershell
$env:JEB_BANK_ROOT = $bank
npm run dev
```

Otvori `http://127.0.0.1:5187`, pa odaberi **Baza znanja**. Baza se ne servira
ako `JEB_BANK_ROOT` nije izričito postavljen.

## 4. Sačuvaj i vrati

```powershell
.venv/Scripts/python.exe -m jeb bank backup `
  --bank-root $bank `
  --output 'D:\backups\moja-baza.zip'

.venv/Scripts/python.exe -m jeb bank backup-verify `
  --input 'D:\backups\moja-baza.zip'
```

Backup je privatna nešifrirana kopija. Ne predstavlja javnu objavu ni pravnu
dozvolu za izvore.

## Pravilo rada

`entity` opisuje predmet, `source` čuva porijeklo i body, `claim` navodi tvrdnju,
a `evidence` povezuje tvrdnju s točnom povijesnom revizijom izvora. Stare
revizije se ne brišu. AI može predložiti zapis, ali ne stvara ljudsko odobrenje.
