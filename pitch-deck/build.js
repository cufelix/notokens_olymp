/* VoltPlán — pitch deck (Česká AI Olympiáda 2026, AI Startup, krajské Praha)
 * Zadání AIO_PHA-02-PHA · B2G SaaS: KDE mají dobíječky smysl.
 * Plně editovatelný .pptx. Generuj: node build.js
 * Čísla = reálné výstupy modelu (src/train_demand.py + src/generate_scores.py).
 * Branding / screenshoty demo se doplní, až bude appka hotová (placeholdery označené).
 */
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const Fa = require("react-icons/fa");

// ---------- paleta (energetika / tech / B2G — důvěryhodná, „elektrická“) ----------
const C = {
  ink:   "0E1726", // hluboká námořní (dominantní tmavá)
  ink2:  "18283F", // tmavý panel
  volt:  "19C37D", // elektrická zelená (hlavní akcent)
  voltD: "0E9E63", // tmavší zelená
  teal:  "1FA8C9", // sekundární modrozelená
  amber: "F2A93B", // jantarová (síť / pozor)
  rust:  "E0654B", // varovná (přetížení / problém)
  paper: "F3F6F9", // světlé pozadí
  card:  "FFFFFF",
  gray:  "55626F", // tlumený text
  grayL: "9DB2C6", // světlý text na tmavé
  line:  "E1E8EF", // linky
  mint:  "E7F7EF", // velmi světlá zelená (highlight pozadí)
};
const FONT_H = "Georgia";
const FONT_B = "Calibri";
const W = 13.333, H = 7.5;
const DECK = "VoltPlán";
const TOTAL = 12;

async function icon(IconComponent, color = "#FFFFFF", size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}
const shadow = () => ({ type: "outer", color: "000000", blur: 9, offset: 3, angle: 90, opacity: 0.22 });
const softShadow = () => ({ type: "outer", color: "0E1726", blur: 6, offset: 2, angle: 90, opacity: 0.10 });

(async () => {
  const I = {
    plug:     await icon(Fa.FaChargingStation),
    bolt:     await icon(Fa.FaBolt),
    map:      await icon(Fa.FaMapMarkedAlt),
    chart:    await icon(Fa.FaChartLine),
    db:       await icon(Fa.FaDatabase),
    brain:    await icon(Fa.FaBrain),
    city:     await icon(Fa.FaCity),
    coins:    await icon(Fa.FaCoins),
    euro:     await icon(Fa.FaEuroSign),
    globe:    await icon(Fa.FaGlobeEurope),
    scale:    await icon(Fa.FaBalanceScale),
    users:    await icon(Fa.FaUsers),
    leaf:     await icon(Fa.FaLeaf),
    server:   await icon(Fa.FaServer),
    search:   await icon(Fa.FaSearchLocation),
    layers:   await icon(Fa.FaLayerGroup),
    battery:  await icon(Fa.FaCarBattery),
    shield:   await icon(Fa.FaShieldAlt),
    sync:     await icon(Fa.FaSyncAlt),
    warn:     await icon(Fa.FaExclamationTriangle),
    check:    await icon(Fa.FaCheckCircle),
    bulb:     await icon(Fa.FaLightbulb),
    pin:      await icon(Fa.FaMapPin),
    home:     await icon(Fa.FaHome),
    trophy:   await icon(Fa.FaTrophy),
    net:      await icon(Fa.FaNetworkWired),
    route:    await icon(Fa.FaRoute),
    grid:     await icon(Fa.FaThLarge),
    clock:    await icon(Fa.FaClock),
    question: await icon(Fa.FaQuestion),
    eye:      await icon(Fa.FaEye),
    flag:     await icon(Fa.FaFlagCheckered),
    voltBolt: await icon(Fa.FaBolt, "#19C37D"),
  };

  const pres = new pptxgen();
  pres.defineLayout({ name: "W", width: W, height: H });
  pres.layout = "W";
  pres.author = "Tým VoltPlán";
  pres.company = "Česká AI Olympiáda 2026";
  pres.title = "VoltPlán — AI pro chytré rozmístění EV dobíjení v Praze";

  // ---------- sdílené helpery ----------
  function footer(slide, n, dark = false) {
    slide.addText([
      { text: "VoltPlán", options: { bold: true, color: dark ? "FFFFFF" : C.ink } },
      { text: "  ·  AIO_PHA-02-PHA", options: { color: dark ? C.grayL : C.gray } },
    ], { x: 0.5, y: H - 0.42, w: 6, h: 0.3, fontFace: FONT_B, fontSize: 10.5, align: "left", margin: 0 });
    slide.addText(String(n).padStart(2, "0") + " / " + TOTAL, { x: W - 1.7, y: H - 0.42, w: 1.2, h: 0.3,
      fontFace: FONT_B, fontSize: 10.5, color: dark ? C.grayL : C.gray, align: "right", margin: 0 });
  }
  function eyebrow(slide, text, x, y, color = C.volt) {
    slide.addText(text.toUpperCase(), { x, y, w: 11, h: 0.3, fontFace: FONT_B, bold: true,
      fontSize: 12, color, charSpacing: 3, align: "left", margin: 0 });
  }
  function titleBlock(slide, eyebrowTxt, title, x, y, titleColor = C.ink, tw = null, ec = C.volt) {
    eyebrow(slide, eyebrowTxt, x, y, ec);
    slide.addText(title, { x, y: y + 0.32, w: tw || (W - x - 0.6), h: 1.1, fontFace: FONT_H, bold: true,
      fontSize: 31, color: titleColor, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.02 });
  }
  function iconBadge(slide, data, x, y, d, color) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: d, h: d, rectRadius: d * 0.22,
      fill: { color }, line: { type: "none" } });
    slide.addImage({ data, x: x + d * 0.26, y: y + d * 0.26, w: d * 0.48, h: d * 0.48 });
  }

  // ============================================================
  // 1 — TITUL
  // ============================================================
  let s = pres.addSlide();
  s.background = { color: C.ink };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.22, h: H, fill: { color: C.volt }, line: { type: "none" } });
  s.addShape(pres.shapes.OVAL, { x: 9.2, y: -2.4, w: 6.2, h: 6.2, fill: { color: C.ink2 }, line: { type: "none" } });
  s.addShape(pres.shapes.OVAL, { x: 10.0, y: 2.5, w: 2.8, h: 2.8, fill: { color: C.voltD, transparency: 45 }, line: { type: "none" } });
  s.addImage({ data: I.plug, x: 10.75, y: 3.25, w: 1.3, h: 1.3 });
  s.addText("ČESKÁ AI OLYMPIÁDA 2026  ·  AI STARTUP  ·  KRAJSKÉ PRAHA", { x: 0.85, y: 1.55, w: 10, h: 0.4,
    fontFace: FONT_B, bold: true, fontSize: 13, color: C.volt, charSpacing: 3, margin: 0 });
  s.addText("VoltPlán", { x: 0.8, y: 2.05, w: 11, h: 1.5, fontFace: FONT_H, bold: true,
    fontSize: 70, color: "FFFFFF", align: "left", valign: "top", margin: 0 });
  s.addText([
    { text: "AI, která městu řekne, ", options: { color: C.grayL } },
    { text: "KDE mají dobíječky smysl", options: { color: C.volt, bold: true } },
    { text: " — a kde jen utopí peníze.", options: { color: C.grayL } },
  ], { x: 0.85, y: 3.7, w: 9.3, h: 1.0, fontFace: FONT_B, fontSize: 19, align: "left", valign: "top",
    margin: 0, lineSpacingMultiple: 1.2 });
  s.addShape(pres.shapes.LINE, { x: 0.85, y: 5.4, w: 4.2, h: 0, line: { color: C.volt, width: 2 } });
  s.addText([
    { text: "Predikce poptávky 2030  ·  kapacita sítě  ·  férovost", options: { color: "FFFFFF", bold: true } },
  ], { x: 0.85, y: 5.6, w: 9, h: 0.4, fontFace: FONT_B, fontSize: 15, align: "left", margin: 0 });
  s.addText("B2G SaaS pro Hl. m. Prahu · zadání AIO_PHA-02-PHA · udržitelná mobilita a energetika",
    { x: 0.85, y: H - 0.6, w: 11, h: 0.3, fontFace: FONT_B, italic: true, fontSize: 11, color: C.grayL, margin: 0 });

  // ============================================================
  // 2 — PROBLÉM + ZÁKAZNÍK
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.paper };
  titleBlock(s, "Problém & zákazník", "Města staví dobíječky naslepo —\na platí za to.", 0.7, 0.55);
  s.addText("Do roku 2030 musí Praha řádově znásobit veřejné dobíjení. Rozhodnutí „kam“ se dnes dělají podle dostupných pozemků a dohadů, ne podle skutečné budoucí poptávky a kapacity sítě. Výsledek: prázdné stojany na jednom místě a fronty na druhém.",
    { x: 0.72, y: 2.35, w: 7.3, h: 1.7, fontFace: FONT_B, fontSize: 15, color: C.gray, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.2 });

  const probs = [
    [I.warn, "Mrtvé investice", "Část veřejných dobíječek končí podvyužitá — zmařené miliony z veřejných peněz."],
    [I.net, "Riziko pro síť", "Stanice na špatném místě přetíží trafostanici; jinde zůstává volná kapacita."],
    [I.scale, "Nerovnost", "Bohaté čtvrti dostanou nabíjení první, okraj čeká — spirála podinvestování."],
  ];
  probs.forEach((p, i) => {
    const y = 2.35 + i * 1.42;
    s.addShape(pres.shapes.RECTANGLE, { x: 8.25, y, w: 4.4, h: 1.28, fill: { color: C.card }, line: { color: C.line, width: 1 }, shadow: softShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x: 8.25, y, w: 0.1, h: 1.28, fill: { color: C.rust }, line: { type: "none" } });
    iconBadge(s, p[0], 8.5, y + 0.27, 0.74, C.ink);
    s.addText(p[1], { x: 9.4, y: y + 0.2, w: 3.1, h: 0.4, fontFace: FONT_H, bold: true, fontSize: 15, color: C.ink, margin: 0 });
    s.addText(p[2], { x: 9.4, y: y + 0.6, w: 3.1, h: 0.62, fontFace: FONT_B, fontSize: 11.5, color: C.gray, margin: 0, valign: "top", lineSpacingMultiple: 1.04 });
  });

  // zákazník pruh
  s.addShape(pres.shapes.RECTANGLE, { x: 0.72, y: 4.55, w: 7.3, h: 1.95, fill: { color: C.ink }, line: { type: "none" }, shadow: softShadow() });
  s.addText("ZÁKAZNÍK (B2G)", { x: 1.0, y: 4.78, w: 6, h: 0.3, fontFace: FONT_B, bold: true, fontSize: 12, color: C.volt, charSpacing: 2, margin: 0 });
  const cust = [
    [I.city, "Hl. m. Praha / MČ", "rozhoduje o umístění"],
    [I.server, "Operátor ICT / Golemio", "datová platforma města"],
    [I.bolt, "PRE / distributor", "kapacita sítě"],
  ];
  cust.forEach((p, i) => {
    const x = 1.0 + i * 2.33;
    iconBadge(s, p[0], x, 5.25, 0.7, C.ink2);
    s.addText(p[1], { x: x - 0.05, y: 6.0, w: 2.25, h: 0.32, fontFace: FONT_B, bold: true, fontSize: 11.5, color: "FFFFFF", margin: 0, lineSpacingMultiple: 0.95 });
    s.addText(p[2], { x: x - 0.05, y: 6.28, w: 2.25, h: 0.3, fontFace: FONT_B, fontSize: 10, color: C.grayL, margin: 0 });
  });
  footer(s, 2);

  // ============================================================
  // 3 — ŘEŠENÍ
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.paper };
  titleBlock(s, "Řešení", "VoltPlán oskóruje každou zónu Prahy\n— a seřadí, kam investovat first.", 0.7, 0.55);
  s.addText([
    { text: "Suitability skóre 0–100", options: { bold: true, color: C.voltD } },
    { text: " pro každou zónu: spojuje ", options: { color: C.gray } },
    { text: "mobilitu", options: { bold: true, color: C.ink } },
    { text: " (kde bude poptávka po EV) s ", options: { color: C.gray } },
    { text: "energetikou", options: { bold: true, color: C.ink } },
    { text: " (kde síť unese zátěž) — přesně to propojení, které zadání odměňuje.", options: { color: C.gray } },
  ], { x: 0.72, y: 2.4, w: 11.9, h: 0.8, fontFace: FONT_B, fontSize: 15, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  const sol = [
    [I.chart, "Predikce poptávky", "LightGBM odhadne počet EV / zátěž v zóně 2030 z profilu území.", "40 %"],
    [I.search, "Mezera v pokrytí", "Poptávka mínus dnešní stanice → kde reálně chybí kapacita.", "30 %"],
    [I.bolt, "Rezerva sítě", "Kde trafostanice unese nové dobíjení bez přetížení.", "15 %"],
    [I.scale, "Férovost", "Domácnosti bez vlastního stání → priorita, ne spirála.", "15 %"],
  ];
  const sw = 2.93, sg = 0.17, sx0 = 0.7, sy0 = 3.45;
  sol.forEach((p, i) => {
    const x = sx0 + i * (sw + sg);
    s.addShape(pres.shapes.RECTANGLE, { x, y: sy0, w: sw, h: 3.05, fill: { color: C.card }, line: { color: C.line, width: 1 }, shadow: softShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: sy0, w: sw, h: 0.09, fill: { color: C.volt }, line: { type: "none" } });
    iconBadge(s, p[0], x + 0.3, sy0 + 0.32, 0.74, C.ink);
    s.addText(p[3], { x: x + sw - 1.15, y: sy0 + 0.34, w: 0.95, h: 0.5, fontFace: FONT_H, bold: true, fontSize: 22, color: C.volt, align: "right", margin: 0 });
    s.addText("VÁHA", { x: x + sw - 1.15, y: sy0 + 0.82, w: 0.95, h: 0.22, fontFace: FONT_B, bold: true, fontSize: 8, color: C.gray, align: "right", charSpacing: 2, margin: 0 });
    s.addText(p[1], { x: x + 0.3, y: sy0 + 1.2, w: sw - 0.55, h: 0.6, fontFace: FONT_H, bold: true, fontSize: 15.5, color: C.ink, margin: 0, valign: "top" });
    s.addText(p[2], { x: x + 0.3, y: sy0 + 1.82, w: sw - 0.5, h: 1.1, fontFace: FONT_B, fontSize: 12, color: C.gray, margin: 0, valign: "top", lineSpacingMultiple: 1.08 });
  });
  s.addText([
    { text: "Výstup:  ", options: { bold: true, color: C.voltD } },
    { text: "heatmapa Prahy + žebříček TOP lokací + „proč tady“ u každé zóny → město dostane rovnou akční seznam.", options: { color: C.gray } },
  ], { x: 0.7, y: 6.62, w: 11.9, h: 0.4, fontFace: FONT_B, italic: true, fontSize: 12.5, align: "left", margin: 0 });
  footer(s, 3);

  // ============================================================
  // 4 — DATA
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.paper };
  titleBlock(s, "Data", "Reálná data o Praze — pečlivě\noddělená od modelových cílů.", 0.7, 0.55, C.ink, 9);

  // levý sloupec: reálné vstupy
  s.addShape(pres.shapes.RECTANGLE, { x: 0.7, y: 2.5, w: 5.85, h: 4.0, fill: { color: C.card }, line: { color: C.line, width: 1 }, shadow: softShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.7, y: 2.5, w: 0.14, h: 4.0, fill: { color: C.teal }, line: { type: "none" } });
  s.addText("REÁLNÉ / ODVOZENÉ VSTUPY", { x: 1.05, y: 2.72, w: 5, h: 0.3, fontFace: FONT_B, bold: true, fontSize: 12, color: C.teal, charSpacing: 1.5, margin: 0 });
  const real = [
    ["2 378 + 517", "zón Praha — trénink + vlastní holdout"],
    ["855", "reálných MPO dobíjecích stanic"],
    ["3 408", "trafostanic — výkon, špička, rezerva"],
    ["2,29 mil.", "hodinových záznamů zátěže sítě (4 týdny)"],
  ];
  real.forEach((p, i) => {
    const y = 3.2 + i * 0.83;
    s.addText(p[0], { x: 1.05, y, w: 1.95, h: 0.5, fontFace: FONT_H, bold: true, fontSize: 21, color: C.ink, align: "left", margin: 0 });
    s.addText(p[1], { x: 3.05, y: y + 0.04, w: 3.4, h: 0.7, fontFace: FONT_B, fontSize: 11.5, color: C.gray, valign: "middle", margin: 0, lineSpacingMultiple: 1.0 });
  });

  // pravý sloupec: čištění + anti-leakage
  const dq = [
    [I.sync, "Čištění", "Chybějící hodnoty, různý zápis, duplicity z reálných zdrojů → sjednoceno."],
    [I.shield, "Anti-leakage", "Cíle target_*_2030_synthetic a vše z nich odvozené NIKDY nejsou featura."],
    [I.eye, "Reálné vs. modelové", "_real / _derived / _synthetic rozlišeno — modelová data nejsou měření."],
  ];
  dq.forEach((p, i) => {
    const y = 2.5 + i * 1.37;
    s.addShape(pres.shapes.RECTANGLE, { x: 6.78, y, w: 5.85, h: 1.22, fill: { color: C.card }, line: { color: C.line, width: 1 }, shadow: softShadow() });
    iconBadge(s, p[0], 7.05, y + 0.27, 0.72, C.ink);
    s.addText(p[1], { x: 7.95, y: y + 0.18, w: 4.5, h: 0.4, fontFace: FONT_H, bold: true, fontSize: 16, color: C.ink, margin: 0 });
    s.addText(p[2], { x: 7.95, y: y + 0.58, w: 4.55, h: 0.56, fontFace: FONT_B, fontSize: 11.5, color: C.gray, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
  });
  footer(s, 4);

  // ============================================================
  // 5 — DATOVÁ PIPELINE / SCRAPING & SBĚR DAT V ČASE
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.paper };
  titleBlock(s, "Datová pipeline", "Sami si data sbíráme — automaticky\na pořád dokola.", 0.7, 0.55, C.ink, 9);
  s.addText("VoltPlán neběží na jednorázovém exportu. Noční konektory stahují data z 8 zdrojů — přes API i headless scraping tam, kde API není — a samy je čistí, validují a verzují. Tím služba „žije zítra“: model se přeučuje na čerstvých datech bez ruční práce.",
    { x: 0.72, y: 2.3, w: 11.9, h: 0.95, fontFace: FONT_B, fontSize: 14.5, color: C.gray, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  // zdroje (scrapované konektory)
  s.addText("SCRAPOVANÉ ZDROJE  ·  8 KONEKTORŮ", { x: 0.72, y: 3.35, w: 8, h: 0.3, fontFace: FONT_B, bold: true, fontSize: 12, color: C.teal, charSpacing: 1.5, margin: 0 });
  const srcs = [
    [I.route, "Golemio API", "parkování, polohy PID, Waze dojezdy", "real-time"],
    [I.city, "opendata.praha.eu", "RÚIAN, územní plán, landuse", "měsíčně"],
    [I.users, "ČSÚ census", "populace, byty bez stání", "ročně"],
    [I.bolt, "PRE / distributor", "kapacita TS, odběrová rezerva", "měsíčně"],
    [I.clock, "ČHMÚ weather API", "počasí → vliv na nabíjení", "hodinově"],
    [I.plug, "MPO + provozovatelé", "stávající stanice + využití", "týdně"],
    [I.map, "OpenStreetMap", "silnice, POI, stožáry VO", "měsíčně"],
    [I.sync, "Zpětná vazba z appky", "reálné využití → do modelu", "průběžně"],
  ];
  const cw = 2.93, cgx = 0.17, cgy = 0.16, cx0 = 0.7, cy0 = 3.75, ch = 1.15;
  srcs.forEach((p, i) => {
    const col = i % 4, row = Math.floor(i / 4);
    const x = cx0 + col * (cw + cgx), y = cy0 + row * (ch + cgy);
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: cw, h: ch, fill: { color: C.card }, line: { color: C.line, width: 1 }, shadow: softShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.08, h: ch, fill: { color: C.teal }, line: { type: "none" } });
    iconBadge(s, p[0], x + 0.22, y + 0.22, 0.6, C.ink);
    s.addText(p[1], { x: x + 0.95, y: y + 0.16, w: cw - 1.05, h: 0.3, fontFace: FONT_B, bold: true, fontSize: 12, color: C.ink, margin: 0 });
    s.addText(p[3], { x: x + 0.95, y: y + 0.44, w: cw - 1.05, h: 0.22, fontFace: FONT_B, bold: true, fontSize: 8.5, color: C.voltD, charSpacing: 1, margin: 0 });
    s.addText(p[2], { x: x + 0.22, y: y + 0.72, w: cw - 0.35, h: 0.38, fontFace: FONT_B, fontSize: 10, color: C.gray, margin: 0, valign: "top", lineSpacingMultiple: 0.98 });
  });

  // pipeline tok
  s.addShape(pres.shapes.RECTANGLE, { x: 0.7, y: 6.45, w: 11.95, h: 0.62, fill: { color: C.ink }, line: { type: "none" }, shadow: softShadow() });
  const flow = ["Scraping / ingest", "Čištění + validace", "Anti-leakage guard", "Feature store (verzováno)", "Re-train modelu", "Nové skóre v appce"];
  flow.forEach((t, i) => {
    const x = 0.95 + i * 1.97;
    s.addText(t, { x, y: 6.45, w: 1.75, h: 0.62, fontFace: FONT_B, bold: true, fontSize: 10.5, color: "FFFFFF", align: "center", valign: "middle", margin: 0, lineSpacingMultiple: 0.95 });
    if (i < flow.length - 1) s.addText("›", { x: x + 1.62, y: 6.45, w: 0.4, h: 0.62, fontFace: FONT_H, bold: true, fontSize: 18, color: C.volt, align: "center", valign: "middle", margin: 0 });
  });
  footer(s, 5);

  // ============================================================
  // 6 — AI MODEL (tmavá, jádro techniky)
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.ink };
  titleBlock(s, "AI model — jádro techniky", "Opravdová AI, ne tabulka.\nA umíme to dokázat.", 0.7, 0.55, "FFFFFF");
  s.addText([
    { text: "LightGBM", options: { bold: true, color: C.volt } },
    { text: " na 60 anti-leakage featurách (zástavba, byty bez stání, parking, MHD, rezerva sítě…). Trénink na 2 378 zónách, ověření na odděleném holdoutu 517 zón.", options: { color: C.grayL } },
  ], { x: 0.72, y: 1.95, w: 7.1, h: 1.1, fontFace: FONT_B, fontSize: 14.5, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.18 });

  const proof = [
    [I.chart, "−17 %", "nižší chyba (MAE) než triviální „úměrně populaci“ pravidlo"],
    [I.check, "P@50 = 0,84", "ze 50 nejžhavějších zón model trefí 42 správně"],
    [I.brain, "83,8 %", "přesnost doporučení typu stanice (AC / DC / hub)"],
  ];
  proof.forEach((p, i) => {
    const y = 3.25 + i * 1.08;
    iconBadge(s, p[0], 0.72, y, 0.74, C.voltD);
    s.addText(p[1], { x: 1.62, y: y - 0.06, w: 2.3, h: 0.5, fontFace: FONT_H, bold: true, fontSize: 26, color: C.volt, margin: 0 });
    s.addText(p[2], { x: 3.7, y: y - 0.02, w: 4.1, h: 0.85, fontFace: FONT_B, fontSize: 12, color: C.grayL, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });
  });

  // pravý panel: proč AI
  s.addShape(pres.shapes.RECTANGLE, { x: 8.5, y: 1.95, w: 4.13, h: 4.55, fill: { color: C.ink2 }, line: { type: "none" }, shadow: shadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 8.5, y: 1.95, w: 4.13, h: 0.1, fill: { color: C.volt }, line: { type: "none" } });
  s.addText("PROČ JE TO AI, NE PRAVIDLO", { x: 8.8, y: 2.25, w: 3.6, h: 0.6, fontFace: FONT_B, bold: true, fontSize: 12, color: C.volt, charSpacing: 1.5, margin: 0, lineSpacingMultiple: 1.0 });
  const why = [
    "Učí se z 60 signálů naráz — ne z jednoho „hodně lidí → velký hub“.",
    "Najde i méně očekávané sedící lokace (serendipity), ne jen centrum.",
    "Měříme proti baseline → víme, KDY model platí a kdy ne.",
  ];
  why.forEach((t, i) => {
    const y = 3.05 + i * 1.08;
    s.addImage({ data: I.voltBolt, x: 8.85, y: y + 0.02, w: 0.28, h: 0.28 });
    s.addText(t, { x: 9.25, y: y - 0.05, w: 3.15, h: 1.0, fontFace: FONT_B, fontSize: 12, color: "FFFFFF", margin: 0, valign: "top", lineSpacingMultiple: 1.1 });
  });
  footer(s, 6, true);

  // ============================================================
  // 7 — VÝSLEDKY + DEMO
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.paper };
  titleBlock(s, "Výsledky & živé demo", "Z modelu rovnou akční seznam\npro radnici.", 0.7, 0.55);

  // levá: placeholder pro screenshot dema
  s.addShape(pres.shapes.RECTANGLE, { x: 0.7, y: 2.5, w: 6.5, h: 4.0, fill: { color: C.ink }, line: { type: "none" }, shadow: softShadow() });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2.9, y: 3.55, w: 2.1, h: 2.1, rectRadius: 0.2, fill: { color: C.ink2 }, line: { type: "none" } });
  s.addImage({ data: I.map, x: 3.5, y: 4.15, w: 0.9, h: 0.9 });
  s.addText("[ SCREENSHOT ŽIVÉHO DEMA ]", { x: 0.7, y: 5.75, w: 6.5, h: 0.35, fontFace: FONT_B, bold: true, fontSize: 13, color: C.volt, align: "center", charSpacing: 2, margin: 0 });
  s.addText("Interaktivní mapa Prahy — heatmapa skóre, filtr po obvodech, popup „proč tady“, export pro úřad.",
    { x: 1.1, y: 6.1, w: 5.7, h: 0.5, fontFace: FONT_B, italic: true, fontSize: 10.5, color: C.grayL, align: "center", margin: 0, lineSpacingMultiple: 1.0 });

  // pravá: top lokace + statistika
  s.addText("TOP DOPORUČENÁ LOKACE", { x: 7.5, y: 2.5, w: 5, h: 0.3, fontFace: FONT_B, bold: true, fontSize: 12, color: C.voltD, charSpacing: 1.5, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 7.5, y: 2.85, w: 5.15, h: 1.5, fill: { color: C.card }, line: { color: C.line, width: 1 }, shadow: softShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: 7.5, y: 2.85, w: 0.12, h: 1.5, fill: { color: C.volt }, line: { type: "none" } });
  s.addText("91,1", { x: 7.75, y: 3.0, w: 1.5, h: 0.9, fontFace: FONT_H, bold: true, fontSize: 40, color: C.volt, margin: 0, valign: "middle" });
  s.addText("/100", { x: 7.78, y: 3.85, w: 1.5, h: 0.3, fontFace: FONT_B, fontSize: 12, color: C.gray, margin: 0 });
  s.addText([
    { text: "TS_3820 · Praha 13\n", options: { bold: true, color: C.ink, fontSize: 15 } },
    { text: "predikce ~201 EV 2030 · jen 1 stanice dnes · volná rezerva sítě", options: { color: C.gray, fontSize: 11 } },
  ], { x: 9.4, y: 3.0, w: 3.1, h: 1.25, fontFace: FONT_B, valign: "middle", margin: 0, lineSpacingMultiple: 1.1 });

  const stats = [["517", "zón oskórováno"], ["TOP-N", "žebříček pro úřad"], ["CSV / mapa", "export výstupů"]];
  stats.forEach((p, i) => {
    const x = 7.5 + i * 1.74;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 4.55, w: 1.6, h: 1.95, fill: { color: C.ink }, line: { type: "none" }, shadow: softShadow() });
    s.addText(p[0], { x: x + 0.05, y: 4.85, w: 1.5, h: 0.7, fontFace: FONT_H, bold: true, fontSize: 23, color: C.volt, align: "center", margin: 0, valign: "middle" });
    s.addText(p[1], { x: x + 0.05, y: 5.65, w: 1.5, h: 0.7, fontFace: FONT_B, fontSize: 11, color: C.grayL, align: "center", margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
  });
  footer(s, 7);

  // ============================================================
  // 8 — BYZNYS
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.paper };
  titleBlock(s, "Byznys model", "Roční licence — protože plánování\nměsta nikdy nekončí.", 0.7, 0.55);
  s.addText([
    { text: "Opakovaná hodnota, opakovaný příjem:", options: { bold: true, color: C.ink } },
    { text: " město neplatí jednorázovou studii, ale ", options: { color: C.gray } },
    { text: "živou službu", options: { bold: true, color: C.voltD } },
    { text: ", která se aktualizuje s novými daty a scénáři růstu EV.", options: { color: C.gray } },
  ], { x: 0.72, y: 2.4, w: 11.9, h: 0.7, fontFace: FONT_B, fontSize: 15, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.15 });

  const biz = [
    [I.euro, "Roční SaaS licence", "Předplatné pro HMP / MČ / Operátora ICT za přístup + pravidelnou aktualizaci skóre."],
    [I.coins, "Návratnost", "Jedna chybně umístěná DC stanice = stovky tisíc až miliony Kč. VoltPlán ji zaplatí mnohonásobně."],
    [I.sync, "Datová smyčka", "Reálné využití stanic teče zpět do modelu → predikce se v čase zpřesňuje. Služba žije."],
    [I.globe, "Škálování", "Stejný engine na 22 MČ Prahy → další krajská města → distributoři. Marginální náklad ~0."],
  ];
  const bw = 2.93, bg = 0.17, bx0 = 0.7, by0 = 3.3;
  biz.forEach((p, i) => {
    const x = bx0 + i * (bw + bg);
    s.addShape(pres.shapes.RECTANGLE, { x, y: by0, w: bw, h: 3.2, fill: { color: C.card }, line: { color: C.line, width: 1 }, shadow: softShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: by0, w: 0.09, h: 3.2, fill: { color: C.volt }, line: { type: "none" } });
    iconBadge(s, p[0], x + 0.3, by0 + 0.32, 0.76, C.ink);
    s.addText(p[1], { x: x + 0.3, y: by0 + 1.2, w: bw - 0.55, h: 0.6, fontFace: FONT_H, bold: true, fontSize: 15, color: C.ink, margin: 0, valign: "top" });
    s.addText(p[2], { x: x + 0.3, y: by0 + 1.78, w: bw - 0.5, h: 1.35, fontFace: FONT_B, fontSize: 12, color: C.gray, margin: 0, valign: "top", lineSpacingMultiple: 1.1 });
  });
  footer(s, 8);

  // ============================================================
  // 9 — NÁŠ ÚHEL + ZAHRANIČNÍ INSPIRACE
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.ink };
  s.addShape(pres.shapes.OVAL, { x: 10.2, y: -2.0, w: 5.0, h: 5.0, fill: { color: C.ink2 }, line: { type: "none" } });
  titleBlock(s, "Náš úhel & světový trend", "Osvědčený přístup ze světa,\nlokalizovaný na Prahu.", 0.7, 0.55, "FFFFFF");
  s.addText("„EV suitability scoring“ je ve světě prověřený obor — my ho jako první stavíme na pražská data o síti a férovosti.",
    { x: 0.72, y: 1.95, w: 11.9, h: 0.6, fontFace: FONT_B, fontSize: 14.5, color: C.grayL, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.1 });

  const refs = [
    ["NCSU EVSE Map (USA)", "suitability mapa + vrstva kapacity sítě"],
    ["StreetLight Data", "equity / Justice40 — férovost v plánování"],
    ["EV-Planner, ILIT", "multi-kritériální umístění dobíječek"],
    ["Driivz", "data-driven ROI a využití stanic"],
  ];
  const rw = 2.93, rg = 0.17, rx0 = 0.7, ry0 = 2.75;
  refs.forEach((p, i) => {
    const x = rx0 + i * (rw + rg);
    s.addShape(pres.shapes.RECTANGLE, { x, y: ry0, w: rw, h: 1.55, fill: { color: C.ink2 }, line: { type: "none" }, shadow: shadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: ry0, w: rw, h: 0.08, fill: { color: C.teal }, line: { type: "none" } });
    s.addText(p[0], { x: x + 0.25, y: ry0 + 0.28, w: rw - 0.45, h: 0.55, fontFace: FONT_H, bold: true, fontSize: 14.5, color: "FFFFFF", margin: 0, valign: "top" });
    s.addText(p[1], { x: x + 0.25, y: ry0 + 0.85, w: rw - 0.45, h: 0.6, fontFace: FONT_B, fontSize: 11, color: C.grayL, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.7, y: 4.65, w: 11.95, h: 1.75, fill: { color: C.voltD, transparency: 12 }, line: { color: C.volt, width: 1 } });
  iconBadge(s, I.bulb, 1.0, 4.95, 0.9, C.volt);
  s.addText("NÁŠ DIFERENCIÁTOR PRO PRAHU", { x: 2.2, y: 4.92, w: 9, h: 0.3, fontFace: FONT_B, bold: true, fontSize: 12, color: C.volt, charSpacing: 1.5, margin: 0 });
  s.addText([
    { text: "Spojujeme ", options: { color: "FFFFFF" } },
    { text: "mobilitu × energetiku", options: { bold: true, color: C.volt } },
    { text: ": rezerva trafostanic z PRE vrstvy + equity (byty bez stání) + scénáře růstu EV + vysvětlení „proč tady“. To samotná zahraniční tabulka neumí.", options: { color: "FFFFFF" } },
  ], { x: 2.2, y: 5.28, w: 10.2, h: 1.0, fontFace: FONT_B, fontSize: 13.5, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12 });
  footer(s, 9, true);

  // ============================================================
  // 10 — ETIKA (čtyři oblasti)
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.paper };
  titleBlock(s, "Etika & odpovědnost", "Čtyři rizika, která bereme vážně\n— ne dodatek, ale součást návrhu.", 0.7, 0.55, C.ink, 9.5);
  const eth = [
    [I.shield, "Chybná predikce & odpovědnost", "Model je podpora rozhodnutí, ne autopilot. Doporučení = vstup pro úředníka, finální slovo má člověk."],
    [I.eye, "Soukromí", "Pracujeme s agregovanými daty na úrovni zón a sítě — žádné sledování pohybu jednotlivců."],
    [I.scale, "Spravedlnost & cold-start", "equity_weight chrání okrajové a chudší čtvrti před spirálou podinvestování. Férovost je přímo ve skóre."],
    [I.question, "Komunikace nejistoty", "Predikce 2030 ukazujeme jako pásmo scénářů (konzervativní / střední / ambiciózní), ne jedno „zaručené“ číslo."],
  ];
  const ew = 5.85, eh = 1.55, egx = 0.2, egy = 0.2, ex0 = 0.7, ey0 = 2.85;
  eth.forEach((p, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = ex0 + col * (ew + egx), y = ey0 + row * (eh + egy);
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: ew, h: eh, fill: { color: C.card }, line: { color: C.line, width: 1 }, shadow: softShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.1, h: eh, fill: { color: C.volt }, line: { type: "none" } });
    iconBadge(s, p[0], x + 0.3, y + 0.32, 0.78, C.ink);
    s.addText(p[1], { x: x + 1.32, y: y + 0.24, w: ew - 1.6, h: 0.42, fontFace: FONT_H, bold: true, fontSize: 15.5, color: C.ink, margin: 0 });
    s.addText(p[2], { x: x + 1.32, y: y + 0.68, w: ew - 1.55, h: 0.8, fontFace: FONT_B, fontSize: 11.5, color: C.gray, margin: 0, valign: "top", lineSpacingMultiple: 1.06 });
  });
  s.addText([
    { text: "Cold-start skóruje 2× — ", options: { bold: true, color: C.voltD } },
    { text: "technicky (málo dat o okraji) i eticky (spravedlnost). U nás je to jeden a tentýž mechanismus.", options: { color: C.gray } },
  ], { x: 0.7, y: 6.5, w: 11.9, h: 0.5, fontFace: FONT_B, italic: true, fontSize: 13, align: "left", margin: 0 });
  footer(s, 10);

  // ============================================================
  // 11 — JAK ETIKA FUNGUJE V SYSTÉMU (mechanismy)
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.ink };
  s.addShape(pres.shapes.OVAL, { x: 10.2, y: -2.2, w: 5.2, h: 5.2, fill: { color: C.ink2 }, line: { type: "none" } });
  titleBlock(s, "Etika zabudovaná v produktu", "Etika není slide navíc —\nje to kód, který běží.", 0.7, 0.55, "FFFFFF");
  s.addText("Každé ze čtyř rizik má v systému konkrétní mechanismus. Nejsou to sliby do pitche — jsou to vlastnosti, které jsou v produktu vidět a dají se zkontrolovat.",
    { x: 0.72, y: 1.95, w: 11.9, h: 0.7, fontFace: FONT_B, fontSize: 14, color: C.grayL, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12 });

  const mech = [
    [I.scale, "Férovost ve skóre", "equity_weight = 15 % suitability. Čtvrti s byty bez stání dostávají prioritu přímo ve vzorci → cold-start spirálu lámeme matematicky, ne dobrou vůlí."],
    [I.warn, "Indikátor jistoty", "Zóny s řídkými daty dostanou nižší confidence a jsou v mapě označené. Model neříká „nevím“ potichu — řekne to nahlas."],
    [I.users, "Člověk rozhoduje", "Doporučení = návrh pro úředníka, ne příkaz. Každé skóre má audit log (vstupy + verze modelu) → rozhodnutí je dohledatelné."],
    [I.chart, "Pásmo, ne jedno číslo", "Predikce 2030 jako 3 scénáře růstu EV (konzervativní / střední / ambiciózní). Nejistotu komunikujeme, neschováváme."],
    [I.shield, "Minimum dat (GDPR)", "Pracujeme jen s agregáty na úroveň zóny a sítě. Žádná osobní data, žádné sledování jednotlivých vozidel ani lidí."],
    [I.bulb, "Vysvětlitelnost", "U každé zóny „proč tady“ (top důvody + feature importance). Žádný black-box — město i občan vidí, na čem skóre stojí."],
  ];
  const mw = 3.92, mgx = 0.18, mgy = 0.18, mx0 = 0.7, my0 = 2.85, mh = 1.78;
  mech.forEach((p, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = mx0 + col * (mw + mgx), y = my0 + row * (mh + mgy);
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: mw, h: mh, fill: { color: C.ink2 }, line: { type: "none" }, shadow: shadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: mw, h: 0.08, fill: { color: C.volt }, line: { type: "none" } });
    iconBadge(s, p[0], x + 0.26, y + 0.28, 0.66, C.voltD);
    s.addText(p[1], { x: x + 1.05, y: y + 0.32, w: mw - 1.25, h: 0.6, fontFace: FONT_H, bold: true, fontSize: 14, color: "FFFFFF", margin: 0, valign: "middle" });
    s.addText(p[2], { x: x + 0.28, y: y + 1.0, w: mw - 0.5, h: 0.72, fontFace: FONT_B, fontSize: 10.5, color: C.grayL, margin: 0, valign: "top", lineSpacingMultiple: 1.06 });
  });
  footer(s, 11, true);

  // ============================================================
  // 12 — TÝM + CLOSING (tmavá)
  // ============================================================
  s = pres.addSlide();
  s.background = { color: C.ink };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.22, h: H, fill: { color: C.volt }, line: { type: "none" } });
  s.addShape(pres.shapes.OVAL, { x: 9.4, y: -2.2, w: 5.6, h: 5.6, fill: { color: C.ink2 }, line: { type: "none" } });
  titleBlock(s, "Tým", "Tři lidé, jedna běžící linie,\nhotové demo.", 0.7, 0.7, "FFFFFF");

  const team = [
    [I.brain, "Model & data", "predikce, suitability, anti-leakage"],
    [I.map, "Aplikace", "běžící mapa + živé demo"],
    [I.coins, "Byznys & pitch", "licence, ROI, etika"],
  ];
  team.forEach((p, i) => {
    const x = 0.72 + i * 4.05;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 3.05, w: 3.8, h: 2.0, fill: { color: C.ink2 }, line: { type: "none" }, shadow: shadow() });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 3.05, w: 3.8, h: 0.09, fill: { color: C.volt }, line: { type: "none" } });
    iconBadge(s, p[0], x + 0.3, 3.35, 0.8, C.voltD);
    s.addText(p[1], { x: x + 1.3, y: 3.45, w: 2.4, h: 0.5, fontFace: FONT_H, bold: true, fontSize: 17, color: "FFFFFF", margin: 0, valign: "middle" });
    s.addText(p[2], { x: x + 0.32, y: 4.35, w: 3.3, h: 0.6, fontFace: FONT_B, fontSize: 12, color: C.grayL, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
  });

  s.addShape(pres.shapes.LINE, { x: 0.85, y: 5.6, w: 4.2, h: 0, line: { color: C.volt, width: 2 } });
  s.addText([
    { text: "VoltPlán", options: { bold: true, color: C.volt } },
    { text: " — město přestane stavět naslepo. Děkujeme.", options: { color: "FFFFFF" } },
  ], { x: 0.85, y: 5.85, w: 11, h: 0.5, fontFace: FONT_H, fontSize: 20, align: "left", margin: 0 });
  s.addText("Česká AI Olympiáda 2026 · AI Startup · AIO_PHA-02-PHA · krajské kolo Praha",
    { x: 0.85, y: H - 0.55, w: 11, h: 0.3, fontFace: FONT_B, italic: true, fontSize: 11, color: C.grayL, margin: 0 });

  await pres.writeFile({ fileName: "VoltPlan-pitch.pptx" });
  console.log("WROTE VoltPlan-pitch.pptx");
})();
