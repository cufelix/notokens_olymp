# MENTOR SESSION PREP — Karta B1: Zákazník a problém

**Tým:** notokens (Vojtěch, Timofej, Felix)  
**Mentor:** [doplnit během schůzky]  
**Čas:** [doplnit během schůzky]

---

## ✅ CO MÁME PŘIPRAVENO (před konzultací)

### 1. PROBLÉM (Jednou větou)
```
Praha má 59,000 EV a cíl 10,000 nových dobíjecích stanic do 2030.
Bez dat → 30% je mrtvých investic (300 MIL Kč zmařeno).
Večerní špička přetěžuje síť. Chybí spojení mobility + energetiky.
```

### 2. BYTZNYS MODEL (opakovaný příjem)

**Zákazníci:**
- **Energetická komunita** (Pražské společenství pro OZE)
  - Zaplatí: 50k Kč/měsíc (600k/rok)
  - Dostane: 112 MIL Kč/rok z V2G flexibility
  - ROI: 187x

- **Distributor** (PRE — Pražská energetika)
  - Zaplatí: 200k Kč/měsíc (2.4 MIL/rok)
  - Ušetří: 100 MIL Kč/rok (nemusí koupit drahě v špičce)
  - ROI: 42x

- **Magistrát Praha**
  - Zaplatí: 30k Kč/měsíc (360k/rok)
  - Ušetří: 270 MIL Kč/rok (zbytečné investice)
  - ROI: 750x

**Náš příjem:** 3.36 MIL Kč (předplatné) + 37.5 MIL Kč (V2G) = **40+ MIL Kč/rok**

### 3. ŘEŠENÍ (3 vrstvy)

| Vrstva | Co | Jak |
|--------|-----|-----|
| **1. Predikce** | Kde stavět stanice | LightGBM model: "Tady bude 2,000 EV/den" |
| **2. Dynamic pricing** | Kdy nabíjet (ekonomicky) | Ceny se mění dle kapacity: 3–15 Kč/kWh |
| **3. V2G** | Auto jako zdroj | V2G: vrací energii v špičce → kompenzace |

### 4. WHY NOW
- 2026: Data jsou TU (59,000 EV existuje)
- 2030: Rozhodování se DĚLÁ teď (10,000 stanic)
- Bez řešení: 300 MIL Kč zmařeno
- S řešením: 482 MIL Kč ušetření

---

## ❓ OTÁZKY, KTERÉ CHCEME POLOŽIT MENTOROVI

### Otázka 1: Opravdu to zákazníci koupi?
```
"Máme tři konkrétní zákazníky (komunita, PRE, magistrát).
Všichni mají problém a peníze. Ale jak se jich dostaneme na
first call? Jaké jsou best practices na B2B SaaS v ČR?"
```

### Otázka 2: Co je první MVP (co opravdu buildovat vs. jenom popisovat)?
```
"V hackathonu máme 4 hodiny. Musíme si vybrat:
- Jenom predikce (LightGBM)
- + V2G heuristika
- + Dynamic pricing kalkulátor
- + Live demo

Co je kritické na prvním call s magistrátem, aby věřili
že to máme opravdu thought-through?"
```

### Otázka 3: Jak řešit regulatory/political risks?
```
"PRE je státní/monopolní. Magistrát je byrokracie.
Jak přesvědčit takovéto instituce, aby používaly startup řešení?
Chybí nám risk analysis na tenhle aspekt."
```

### Otázka 4: Konkurence & diferenciátor?
```
"V2G a dynamic pricing nejsou nové koncepty.
Čím se liší náš přístup? Je to opravdu hard to copy?
Nebo jsme jen assembleři open-source řešení?"
```

---

## 📌 NAŠE HYPOTÉZY (co si myslíme, ale nejsme si jistí)

### Hypotéza 1: Economic incentives fungují
**Tvrdíme:** Řidič se sám rozhodne nabíjet v noci, když je elektřina 3 Kč místo 15 Kč.  
**Riziko:** Řidič chce nabít TEĎKA (18h), ne čekat do 23h.  
**Řešení:** Smart nabíječka to dělá automaticky. Test: Wallbox API.

### Hypotéza 2: V2G flexibility je opravdu monetizable
**Tvrdíme:** Komunita prodá energii vracenou z aut za 1.5 Kč/kWh.  
**Riziko:** Agregátor jí koupí za 0.5 Kč (příliš málo).  
**Řešení:** Direct contract s PRE: "Vracíte flexibilitu → my vám garantujeme cenu."

### Hypotéza 3: Magistrát koupi bez dodělané implementace
**Tvrdíme:** Pilot PRE existuje, data jsou tam, magistrát má rozpočet.  
**Riziko:** Magistrát čeká hotový produkt, ne MVP.  
**Řešení:** Začít s Operátorem ICT (Golemio) — oni jsou technické gatekeeping.

---

## 🎯 CO CHCEME OD MENTORA (konkrétně)

- **Validace byznys modelu:** Je tahle revenue structure realistická?
- **Traction path:** Kam bychom měli jít v prvních 3 měsících (post-hackathonu)?
- **Red flags:** Co vidí mentor jako riziko, co my nevidíme?
- **Introductions:** Má kontakty na někoho v PRE, Magistrátu, nebo komunitě?
- **Reality check:** Je toto startup-worthy, nebo je to consulting projekt?

---

## 💼 ELEVATOR PITCH (co budeme mentorovi презентovать)

> **VoltPlán je SaaS pro energetické komunity, distributory a města.**
>
> **Problém:** Praha staví 10,000 dobíjecích stanic, ale bez dat → 30% je prázdných (300 MIL Kč zmařeno). Večerní špička přetěžuje síť.
>
> **Řešení:** 
> 1. Predikce (kde stavět)
> 2. Dynamic pricing (kdy nabíjet — řidič se rozhoduje sám)
> 3. V2G (auto vrací energii = peníze)
>
> **Tržiště:** 3 konkrétní zákazníci (komunita + PRE + magistrát) s 482 MIL Kč ročním problémem.
>
> **Náš příjem:** 40+ MIL Kč/rok (SaaS + V2G výnosy).
>
> **Traction:** Magistrát má rozpočet TEĎKA (2026), rozhodování se dělá TEĎKA, pilot PRE existuje.

---

## 📝 POZNÁMKY Z KONZULTACE (vyplnit během schůzky)

### Co mi mentor doporučil:

```
[Zde si zapíší mentorovy tipy, validators, red flags, introductions]
```

### Co konkrétně upravíme v businessu modelu:

```
[Zde si zapíší změny, které mentor navrhne]
```

---

## ✅ CHECKLIST PŘED SCHŮZKOU

- ✅ PITCH-ONE-PAGE.md — memorován (3 zákazníci, 40M/rok)
- ✅ DYNAMIC-PRICING.md — přečteno (ekonomické řízení, ne direktivy)
- ✅ Hypotézy připravené (risk analysis)
- ✅ Otázky pro mentora napsané
- ✅ Elevator pitch prepared (30 sekund)
- ✅ GitHub repo hotový (všechno pushnuto)
- ⏳ Data: čekat na sandbox dataset

---

**Jděte na mentora s vědomím, že máte KONKRÉTNÍ byznys, ne jenom techniku. Mentor chce slyšet o zákaznících a penězích, ne o ML modelech.** 

💡 **KEY MESSAGE:** "Tady jsou tři instituce, které mají dnes problém. Vy jste expert na byznys — jak se jim dostaneme na first call?"
