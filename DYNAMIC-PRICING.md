# Dynamic Pricing — Jak se řidič motivuje (ne direktivně)

## ⚠️ KRITICKÁ VĚCI (kterou jsme opravili)

**PŮVODNÍ CHYBA:**
```
"VoltPlán řídí nabíjení"
└─ Problém: Řidič přijde v 18h a chce nabít TEĎKA
   My říkáme "nabíjej v 23h" → řidič: "No, ne."
   Výsledek: Model je zbytečný
```

**SPRÁVNÉ ŘEŠENÍ:**
```
"VoltPlán MOTIVUJE nabíjení přes ceny + V2G kompenzaci"
└─ Řidič se sám rozhoduje EKONOMICKY
└─ Levnější = nabíjí | Dražší = čeká
└─ To funguje!
```

---

## 💰 EKONOMICKÝ MODEL (24 hodin)

### CENY ELEKTŘINY PODLE KAPACITY SÍTĚ

```
ČTYŘIADVACET HODIN:

00-06h:  2 Kč/kWh  ← LEVNÉ (noc, přebytek OZE)    NABÍJEJ!
06-11h:  5 Kč/kWh
11-14h:  4 Kč/kWh  ← LEVNÉ (oběd, slunce)        NABÍJEJ!
14-18h:  6 Kč/kWh
18-22h: 15 Kč/kWh  ← DRAHÉ (špička, poptávka)    NE!
22-24h:  3 Kč/kWh  ← VELMI LEVNÉ (noc)           NABÍJEJ!

ZDROJ CEN: VoltPlán počítá z hourly_reserve v datech
├─ Vysoká reserve = levná (3-5 Kč/kWh)
└─ Nízká reserve = drahá (15-20 Kč/kWh)
```

### ŘIDIČŮV ROZHODOVACÍ PROCES

```
ŘIDIČ PŘIJDE V 18h:

1. Připojí auto do SMART NABÍJEČKY (Wallbox + VoltPlán API)

2. Řekne: "Chci 100% baterie do 8h zítra"
   (cíl, ne timing)

3. Nabíječka se podívá do VoltPlánu:
   ├─ 18-22h: 15 Kč/kWh (DRAHÁ) → čeká
   ├─ 22-23h: 3 Kč/kWh (LEVNÁ) → začíná nabíjet
   ├─ 23-06h: 2-3 Kč/kWh (LEVNÁ) → pokračuje
   └─ 06-08h: 5 Kč/kWh (OK) → finalizuje

4. V 8h má auto 100% za nejlevnější cenu
   └─ Řidič je SPOKOJENÝ (ušetřil ~100 Kč na elektřině)

5. Průměrná cena: ~4 Kč/kWh (místo 15 Kč) = 70% úspora!
```

---

## ⚡ V2G KOMPENZACE (auto = zdroj peněz)

### PŘÍPAD: Špička v 20h

```
SITUACE:
├─ Vaš model vidí: "V 20h je špička, nízká reserve"
├─ Síť nemá dost kapacity
└─ Potřebuje flexibility

VOLTPLÁN ŘÍKÁ AUTU:
"Jeee, máte baterii. Vraťte energii v 20-21h?"

AUTO ROZHODNE:
├─ Vrátí 240 kWh
└─ Dostane 400 Kč (= 1.67 Kč/kWh, to je premium)

ŘIDIČ:
├─ "Vrátím energii a dostanu 400 Kč?" → ANO!
├─ Není to povinnost, je to PROFIT
└─ Všichni vyhrávají
```

### CENÍK V2G KOMPENZACE

```
Čas              Cena flexibility  Příklad (240 kWh)
────────────────────────────────────────────────────
18-19h (špička): 1.5 Kč/kWh    = 360 Kč
19-20h (špička): 1.8 Kč/kWh    = 432 Kč
20-21h (PEAK):   2.0 Kč/kWh    = 480 Kč ← nejvýnosněji
21-22h (špička): 1.5 Kč/kWh    = 360 Kč
22-24h (mild):   0.5 Kč/kWh    = 120 Kč

Řidič si vybere: "Vrátím v 20h, jsou tam peníze."
```

---

## 🔗 TECHNICKÁ IMPLEMENTACE

### CO JE POTŘEBA

**1. SMART NABÍJEČKA (hardware)**
```
Příklady: Wallbox, Tesla Supercharger, Nissan CHAdeMO
Musí umět: Přijmout instrukci "nabíjej v těchto hodinách"
API: OpenADR, OCPP 2.0 (standardy)
```

**2. V2G CAPABLE AUTO (hardware)**
```
Příklady: Nissan Leaf, BMW i3, Hyundai Kona EV
Musí: Mít V2G nabíječku (nije standardní AC, ale DC)
```

**3. VOLTPLÁN API (software)**
```
Endpoint 1: GET /prices-24h/{zone_id}
└─ Vrátí: [2, 5, 4, 6, 15, 3, ...] (ceny každou hodinu)

Endpoint 2: POST /v2g-offer/{car_id}
└─ Nabídne: "Vrátíte 240 kWh v 20h za 480 Kč?"

Endpoint 3: GET /smart-charger-schedule/{charger_id}
└─ Vrátí: Kdy nabíjet: [23, 00, 01, 02, 03, ...]
```

**4. N8N SMYČKA (operace)**
```
Každou hodinu:
1. Načti aktuální reserve z PRE dat
2. Přepočítej ceny (reserve → cena)
3. Pushnout ceny do nabíječek + app
4. Monitoruj V2G nabídky (auto vrací?)
5. Zaloguj flexibility zdroj
```

---

## 📊 VÝSLEDKY (co se změní)

### PŘED VOLTPLÁNEM (dnes)

```
Řidičů chování: Náhodné
├─ Přijde v 18h → nabije v 18h (špička!)
├─ Není mu to samy, kdo by plánoval?
├─ Síť se přetěžuje
└─ Distributor kupuje drahé energii (100 MIL Kč/rok)
```

### S VOLTPLÁNEM (správně)

```
Řidičů chování: Optimální (ekonomicky motivované)
├─ Vidí ceny: "Nabije v noci za 2 Kč" vs "za 15 Kč"?
├─ Objedná si "100% do 8h" → nabíječka se postará
├─ Špička v 20h → auto vrátí energii za 480 Kč
├─ Všichni vyhrávají
└─ Distributor ušetří 100 MIL Kč/rok (nemusí koupit drahě)
```

---

## 🎯 PITCH (co ŘÍCI)

> *"VoltPlán NEŘÍDÍ nabíjení direktivně.*
> 
> *Místo toho: Vidíte ceny elektřiny za každou hodinu.*
> 
> *V 11-14h: 4 Kč/kWh (levná) → nabijete.*
> *V 18-22h: 15 Kč/kWh (drahá) → čekáte.*
> 
> *Řidič se sám rozhoduje. Chování je automaticky optimální.*
> 
> *Navíc: V2G. Auto v špičce vrátí energii za 480 Kč.*
> 
> *Nikdo není do toho tlačen. Všichni chtějí, protože to vychází.*
> 
> *Výsledek: Síť bez přetížení. Všichni profitují."*

---

## ✅ SHRNUTÍ: KLÍČ K ÚSPĚCHU

| Co | Bylo (naivní) | Je (správně) |
|---|---|---|
| **Řízení nabíjení** | Direktivní ("nabíjej teď") | Ekonomické (ceny elektřiny) |
| **Motivace řidiče** | Byť dobrý | Chovat se optimálně = profit |
| **V2G** | "Auta vrací" | "Auta vrací a dostávají peníze" |
| **Realismus** | Řidič ignoruje | Řidič CHCE, protože mu to vychází |

---

`AIO_PHA-02-PHA | Česká AI Olympiáda 2026 | notokens | 2026-06-09`
