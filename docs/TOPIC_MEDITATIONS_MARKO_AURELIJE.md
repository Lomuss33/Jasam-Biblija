# Meditacije — Marko Aurelije

Status: **topic draft / unreviewed**. Ovo nije odobren korpusni izvor, ne
sadrži prepisani tekst i ne daje pravno odobrenje za korištenje prijevoda.

## Osnovna kartica

- Entitet: Marcus Aurelius Antoninus (121–180), rimski car i filozof.
- Djelo: *Ta eis heauton* / *Meditationes*, osobne bilješke u 12 knjiga.
- Jezik djela: koine grčki.
- Tradicionalni naslov „Meditacije” opisuje kasniju recepciju; naslov *ta eis
  heauton* znači približno „samome sebi”.
- IEP navodi da su bilješke vjerojatno nastajale tijekom vojnih kampanja u
  središnjoj Europi oko 171–175. godine, ali redoslijed i datiranje nisu
  potpuno sigurni.

## Izvori i rights stanje

| ID | Uloga | Status |
|---|---|---|
| `src-gutenberg-long-15877` | George Long, engleski prijevod iz 1862.; Project Gutenberg | kandidat; javno-domena tvrdnja mora se provjeriti po jurisdikciji |
| `src-gutenberg-casaubon-2680` | Meric Casaubon, stariji engleski prijevod; Project Gutenberg | kandidat; provjeriti točno izdanje i datoteke |
| `src-perseus-cts` | grčki tekst/CTS identifikacija | kandidat; provjeriti licencu i uvjete korištenja podatka |
| `src-iep-marcus-aurelius` | sekundarna filozofska enciklopedija, John Sellars | bibliografski/interpretativni izvor; ne kopirati članak |
| `src-loc-27007869` | bibliografski zapis Library of Congress | katalogizacijski trag; ne pretpostavljati prava na digitalni artefakt |

Svi zapisi iznad ostaju `unreviewed`. Provider oznaka ili javna dostupnost ne
znači automatsko worldwide clearance. Za projekt se moraju evidentirati točno
izdanje, digitalni artefakt, hash, jurisdikcija, licenca i eventualna prava
prijevoda.

Pravilo pohrane za ovu temu: poveznica se uvijek čuva. Točan artefakt treba se
preuzeti i čuvati čim rights provjera pokaže da je to dopušteno za konfigurirane
jurisdikcije; ako postoji zabrana ili neriješena pravna prepreka, ostaje link
uz dokumentirani razlog i ne preuzimaju se bajtovi.

## Knowledge graph

```text
Marcus Aurelius
├── authored/associated_with → Meditations
├── influenced_by → Epictetus / Stoic tradition
├── historical_context → Roman Empire, reign 161–180
└── source_claims → each claim linked to a precise source and locator

Meditations
├── has_structure → 12 books
├── language → Koine Greek
├── themes → judgement, action, desire, mortality, nature, community
└── editions/translations → separate source entities, never merged
```

## Edukacijski proizvodi

1. **Osnovni vodič** — što je djelo, kome je pripisano, kako je strukturirano
   i kako čitati bez motivacijskih pojednostavljenja.
2. **Tematski moduli** — prosudba i dojam; djelovanje i dužnost; želja i
   kontrola; prolaznost; odnos prema zajednici; kosmička perspektiva.
3. **Kritički modul** — razlika između povijesnog Marka Aurelija, stoicizma i
   modernog self-help prikaza.
4. **Prezentacija** — 10–12 slajdova: problem, kontekst, struktura, tri
   praktične osi, primjeri iz odabranih lokatora, ograničenja, izvori.
5. **Video** — 6–8 minuta: uvod, povijesni okvir, jedna ideja po poglavlju,
   jasno označena interpretacija i završni poziv na provjeru izvora.

## Pravilo za buduće claimove

Svaki claim mora imati: `claim_id`, kategoriju (`historical_claim`,
`source_statement` ili `interpretation`), točan izvor, izdanje/prijevod,
lokator knjiga/poglavlje, status pregleda i suprotne dokaze ako postoje.
Interpretacija se ne smije prikazati kao Markova izravna tvrdnja.

## Početne poveznice

- [Internet Encyclopedia of Philosophy — Marcus Aurelius](https://iep.utm.edu/marcus-aurelius/)
- [Project Gutenberg — Meditations, eBook 15877](https://www.gutenberg.org/ebooks/15877)
- [Project Gutenberg — Meditations, eBook 2680](https://www.gutenberg.org/ebooks/2680)
- [Perseus Digital Library CTS](https://data.perseus.org/)
- [Library of Congress — bibliographic record 27007869](https://www.loc.gov/item/27007869/)

Sljedeći tehnički korak je unijeti ove URL-ove kroz `jeb sources candidates`
 kao neutralni metadata batch, zatim ručno provjeriti točno izdanje i prava.
