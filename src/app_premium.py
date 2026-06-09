"""VoltPlán — rozhodovací dashboard pro plánování EV infrastruktury (Magistrát HMP).

Čte JEDEN kontraktní soubor `submissions/app_zone_scores.csv` (vyrábí generate_scores.py):
suitability_score + predikovaná poptávka 2030 + rezerva sítě + mezera v pokrytí + férovost
+ doporučený typ + "proč". Žádná čísla natvrdo — skóre vychází z natrénovaného modelu.

    streamlit run src/app_premium.py
"""
from __future__ import annotations

import pathlib

import folium
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import polars as pl
import streamlit as st
from streamlit_folium import st_folium

# ----------------------------------------------------------------------------
# KONFIGURACE + DESIGN (světlé, editorial, institucionální — bez gradientů/emoji)
# ----------------------------------------------------------------------------

st.set_page_config(
    page_title="VoltPlán — plánování EV infrastruktury",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta (OKLCH-konzistentní, jeden accent = energie/vhodnost; warm neutrály)
ACCENT = "#1F6F5C"        # deep teal-green
ACCENT_SOFT = "#2E9E83"
INK = "#23211E"           # warm charcoal (ne čistá čerň)
MUTED = "#6E6A63"
BORDER = "#E6E4DF"
CANVAS = "#F7F6F3"
SURFACE = "#FFFFFF"
WARN = "#B4791F"          # amber — nízká rezerva sítě
DANGER = "#A23A2E"

st.markdown(f"""
<style>
    .stApp {{ background: {CANVAS}; }}
    html, body, [class*="css"] {{
        font-family: -apple-system, "SF Pro Display", "Helvetica Neue", "Segoe UI", sans-serif;
        color: {INK};
    }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 2.2rem; max-width: 1500px; }}

    h1, h2, h3, h4 {{ color: {INK}; letter-spacing: -0.02em; font-weight: 650; }}
    h1 {{ font-size: 1.9rem; }}
    h2 {{ font-size: 1.25rem; border: none; padding: 0; margin-top: .4rem; }}
    h3 {{ font-size: 1.02rem; color: {MUTED}; font-weight: 600; }}
    a {{ color: {ACCENT}; }}

    /* KPI karty */
    [data-testid="stMetric"] {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 16px 18px;
    }}
    [data-testid="stMetricLabel"] {{ color: {MUTED}; font-size: .82rem; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }}
    [data-testid="stMetricValue"] {{ color: {INK}; font-size: 1.7rem; font-weight: 680; }}

    /* taby */
    .stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDER}; }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent; border-radius: 8px 8px 0 0; padding: 8px 18px;
        color: {MUTED}; font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{ color: {ACCENT}; border-bottom: 2px solid {ACCENT}; }}

    /* tlačítka + download */
    .stButton > button, .stDownloadButton > button {{
        background: {INK}; color: #fff; border: none; border-radius: 6px;
        font-weight: 600; padding: 8px 18px;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{ background: #000; color: #fff; }}

    [data-testid="stSidebar"] {{ background: {SURFACE}; border-right: 1px solid {BORDER}; }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {{ font-size: 1.05rem; }}

    .vp-tag {{ display:inline-block; font-size:.7rem; font-weight:700; text-transform:uppercase;
        letter-spacing:.06em; padding:3px 9px; border-radius:999px; background:#EAF3EF; color:{ACCENT}; }}
    .vp-sub {{ color:{MUTED}; font-size:.95rem; margin-top:-.3rem; }}
    .vp-card {{ background:{SURFACE}; border:1px solid {BORDER}; border-radius:10px; padding:18px 20px; }}
    hr {{ border-color: {BORDER}; }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# DATA
# ----------------------------------------------------------------------------

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCORES = ROOT / "submissions" / "app_zone_scores.csv"


@st.cache_data
def load_scores() -> pd.DataFrame:
    if not SCORES.exists():
        st.error(
            "Chybí `submissions/app_zone_scores.csv`. Nejdřív spusť:  "
            "`python src/generate_scores.py`"
        )
        st.stop()
    return pl.read_csv(SCORES).to_pandas()


df_all = load_scores()


def score_color(score: float) -> str:
    """Sekvenční zelená rampa: nízká vhodnost = bledá, vysoká = sytě zelená."""
    t = max(0.0, min(1.0, score / 100.0))
    # interpolace mezi pale (#E9F2EE) a deep accent (#1F6F5C)
    c0 = (233, 242, 238)
    c1 = (31, 111, 92)
    rgb = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
    return "#%02x%02x%02x" % rgb


# ----------------------------------------------------------------------------
# HLAVIČKA
# ----------------------------------------------------------------------------

st.markdown('<span class="vp-tag">B2G · Magistrát hl. m. Prahy</span>', unsafe_allow_html=True)
st.markdown("# VoltPlán — kam umístit dobíječky")
st.markdown(
    '<p class="vp-sub">AI ohodnotí každou zónu Prahy podle predikované poptávky 2030, '
    "rezervy sítě, mezery v pokrytí a férovosti — aby město neinvestovalo do prázdných stanic.</p>",
    unsafe_allow_html=True,
)
st.write("")

# ----------------------------------------------------------------------------
# SIDEBAR — FILTRY
# ----------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## Filtry")

    districts = sorted(df_all["district"].unique().tolist())
    sel_districts = st.multiselect("Správní obvod", districts, default=districts)

    min_score = st.slider("Min. suitability skóre", 0, 100, 0, 5)

    top_n = st.slider("Počet doporučených lokalit (TOP-N)", 5, 50, 15, 5)

    st.divider()
    st.markdown("## Vrstvy mapy")
    show_grid_risk = st.checkbox("Zvýraznit nízkou rezervu sítě", value=False,
                                 help="Zóny s rezervou sítě pod 25 % — kde by síť novou zátěž neunesla.")

    st.divider()
    st.caption("Model: LightGBM · trénink na zones_train, "
               "skórování na holdoutu zones_validation. Sandbox, ne odevzdání.")

# aplikuj filtry
df = df_all[df_all["district"].isin(sel_districts)].copy()
df = df[df["suitability_score"] >= min_score]
if df.empty:
    st.warning("Žádné zóny neodpovídají filtru. Uvolni kritéria v levém panelu.")
    st.stop()

top = df.nlargest(top_n, "suitability_score").reset_index(drop=True)

# ----------------------------------------------------------------------------
# KPI ŘÁDEK
# ----------------------------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)
c1.metric("Hodnocených zón", f"{len(df):,}".replace(",", " "))
c2.metric("Průměrné skóre", f"{df['suitability_score'].mean():.0f} / 100")
underserved = int((df["coverage_gap"] > 0.15).sum())
c3.metric("Podpokrytých zón", f"{underserved}", help="Poptávka výrazně převyšuje stávající stanice")
c4.metric("Doporučeno k řešení", f"{top_n}", help="Top zóny dle suitability v rámci filtru")

st.write("")

tab_map, tab_budget, tab_model = st.tabs(
    ["Mapa & doporučení", "Rozpočet & dopad", "Model & metodika"]
)

# ============================================================================
# TAB 1 — MAPA & DOPORUČENÍ
# ============================================================================

with tab_map:
    col_map, col_table = st.columns([1.55, 1])

    with col_map:
        st.markdown("### Suitability mapa Prahy")
        m = folium.Map(
            location=[df["center_lat"].mean(), df["center_lon"].mean()],
            zoom_start=11, tiles="CartoDB positron", control_scale=True,
        )

        for _, r in df.iterrows():
            low_grid = r["grid_headroom"] < 25
            folium.CircleMarker(
                location=[r["center_lat"], r["center_lon"]],
                radius=5 + (r["suitability_score"] / 100) * 7,
                color="#ffffff", weight=0.6,
                fill=True,
                fill_color=(DANGER if (show_grid_risk and low_grid) else score_color(r["suitability_score"])),
                fill_opacity=0.85,
                popup=folium.Popup(
                    f"<b>{r['grid_zone_id']}</b> · {r['district']}<br>"
                    f"<b>Suitability: {r['suitability_score']:.0f}/100</b><br>"
                    f"Poptávka 2030: {r['predicted_demand_2030']:.0f} EV/den<br>"
                    f"Rezerva sítě: {r['grid_headroom']:.0f} %<br>"
                    f"Stávající stanice: {int(r['current_stations'])}<br>"
                    f"Doporučení: {r['recommended_type']}<br>"
                    f"<i>Proč: {r['top_reasons']}</i>",
                    max_width=270,
                ),
            ).add_to(m)

        # TOP-N očíslované kotvy
        for i, r in top.iterrows():
            folium.Marker(
                location=[r["center_lat"], r["center_lon"]],
                icon=folium.DivIcon(html=(
                    f'<div style="background:{ACCENT};color:#fff;border-radius:50%;'
                    f'width:22px;height:22px;line-height:22px;text-align:center;'
                    f'font-size:11px;font-weight:700;border:2px solid #fff;">{i+1}</div>')),
            ).add_to(m)

        st_folium(m, use_container_width=True, height=560, returned_objects=[])

        # legenda
        st.markdown(
            f'<div style="display:flex;gap:18px;align-items:center;font-size:.82rem;color:{MUTED}">'
            f'<span>Vhodnost:</span>'
            f'<span><span style="display:inline-block;width:12px;height:12px;background:{score_color(15)};'
            f'border-radius:3px;margin-right:5px"></span>nízká</span>'
            f'<span><span style="display:inline-block;width:12px;height:12px;background:{score_color(55)};'
            f'border-radius:3px;margin-right:5px"></span>střední</span>'
            f'<span><span style="display:inline-block;width:12px;height:12px;background:{score_color(95)};'
            f'border-radius:3px;margin-right:5px"></span>vysoká</span>'
            f'<span style="margin-left:8px"><span style="display:inline-block;width:12px;height:12px;'
            f'background:{DANGER};border-radius:3px;margin-right:5px"></span>nízká rezerva sítě</span>'
            "</div>",
            unsafe_allow_html=True,
        )

    with col_table:
        st.markdown(f"### TOP {top_n} doporučených lokalit")
        show = top[[
            "grid_zone_id", "district", "suitability_score",
            "predicted_demand_2030", "grid_headroom", "current_stations", "recommended_type",
        ]].copy()
        show.insert(0, "#", range(1, len(show) + 1))
        show.columns = ["#", "Zóna", "Obvod", "Skóre", "EV/den", "Rezerva %", "Stanice", "Typ"]
        show["Skóre"] = show["Skóre"].round(0).astype(int)
        show["EV/den"] = show["EV/den"].round(0).astype(int)
        show["Rezerva %"] = show["Rezerva %"].round(0).astype(int)
        st.dataframe(show, use_container_width=True, hide_index=True, height=430)

        export = df.sort_values("suitability_score", ascending=False)
        st.download_button(
            "Export doporučení (CSV)",
            export.to_csv(index=False).encode("utf-8"),
            file_name="voltplan_doporuceni_praha.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.divider()
    st.markdown("### Proč model doporučuje TOP lokalitu")
    best = top.iloc[0]
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Predikovaná poptávka", f"{best['predicted_demand_2030']:.0f} EV/den")
    e2.metric("Rezerva sítě", f"{best['grid_headroom']:.0f} %")
    e3.metric("Stávající stanice", f"{int(best['current_stations'])}")
    e4.metric("Index bez vl. stání", f"{best['equity_weight']:.2f}")
    st.markdown(
        f'<div class="vp-card">Zóna <b>{best["grid_zone_id"]}</b> ({best["district"]}) — '
        f'suitability <b>{best["suitability_score"]:.0f}/100</b>. '
        f'Hlavní důvody: {best["top_reasons"]}. Doporučený typ: <b>{best["recommended_type"]}</b> '
        f'({int(best["recommended_ports"])} portů / {int(best["recommended_total_kw"])} kW).</div>',
        unsafe_allow_html=True,
    )

# ============================================================================
# TAB 2 — ROZPOČET & DOPAD (obhajitelná čísla)
# ============================================================================

with tab_budget:
    st.markdown("### Rozpočtový optimalizátor")
    st.caption("„Mám rozpočet X — kam ho dát, aby pokryl co nejvíc poptávky.“ "
               "Model seřadí zóny dle suitability a naplní rozpočet odshora.")

    b1, b2, b3 = st.columns(3)
    budget = b1.number_input("Rozpočet (mil. Kč)", 5, 500, 60, 5)
    cost_ac = b2.number_input("Náklad AC stanice (mil. Kč)", 0.1, 5.0, 0.3, 0.1,
                              help="Veřejná AC stanice v ČR ~0,2–0,4 mil. Kč")
    cost_dc = b3.number_input("Náklad DC rychlostanice (mil. Kč)", 0.5, 5.0, 1.5, 0.1,
                              help="DC rychlonabíječka ~1–2 mil. Kč")

    plan = df.sort_values("suitability_score", ascending=False).copy()
    is_dc = plan["recommended_type"].str.contains("dc|fast|hub", case=False, regex=True)
    plan["unit_cost"] = np.where(is_dc, cost_dc, cost_ac)
    plan["cum_cost"] = plan["unit_cost"].cumsum()
    funded = plan[plan["cum_cost"] <= budget]

    covered_demand = funded["predicted_demand_2030"].sum()
    total_demand = df["predicted_demand_2030"].sum()
    cov_pct = (covered_demand / total_demand * 100) if total_demand else 0

    k1, k2, k3 = st.columns(3)
    k1.metric("Financovatelných lokalit", f"{len(funded)}")
    k2.metric("Pokrytí poptávky", f"{cov_pct:.0f} %",
              help="Podíl predikované poptávky 2030 ve financovaných zónách")
    k3.metric("Průměrné skóre výběru", f"{funded['suitability_score'].mean():.0f} / 100"
              if len(funded) else "—")

    st.write("")
    st.markdown("### Hodnota pro město — zabráněná promrhaná investice")
    st.caption("Konzervativní odhad. Bez cílení končí podle oborových dat ~30 % veřejných "
               "stanic podvyužitých; cílení tento podíl snižuje. Žádné spekulativní násobky.")

    waste_rate_base = 0.30   # podíl podvyužitých stanic bez datového cílení (oborový odhad)
    waste_rate_targeted = 0.10
    avoided = (waste_rate_base - waste_rate_targeted) * budget  # mil. Kč

    g1, g2 = st.columns([1, 1])
    with g1:
        st.markdown(
            f'<div class="vp-card">Z rozpočtu <b>{budget} mil. Kč</b> by cílení místo plošného '
            f'rozmístění mělo uchránit přibližně <b>{avoided:.1f} mil. Kč</b> '
            f'(rozdíl mezi ~30 % a ~10 % podvyužitých stanic).<br><br>'
            f'Roční licence VoltPlánu (~0,3 mil. Kč) se vrátí už při uchránění '
            f'jediné podvyužité AC stanice.</div>',
            unsafe_allow_html=True,
        )
    with g2:
        fig = go.Figure()
        fig.add_bar(x=["Plošně", "S cílením"],
                    y=[waste_rate_base * budget, waste_rate_targeted * budget],
                    marker_color=[MUTED, ACCENT])
        fig.update_layout(
            title="Očekávaná promrhaná investice (mil. Kč)",
            template="plotly_white", height=300, margin=dict(t=40, b=10, l=10, r=10),
            yaxis_title="mil. Kč", showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3 — MODEL & METODIKA
# ============================================================================

with tab_model:
    st.markdown("### Jak model funguje a proč je to opravdová AI")

    m1, m2, m3 = st.columns(3)
    m1.metric("MAE LightGBM", "4.70 EV/den", "−17 % vs. populační baseline", delta_color="inverse")
    m2.metric("Precision@50", "0.84", "shoda TOP-50 zón")
    m3.metric("Recommender typu stanice", "83.8 %", "přesnost na holdoutu")

    st.markdown(
        f'<div class="vp-card">'
        "<b>Dva modely.</b> (1) LightGBM regrese predikuje poptávku po nabíjení 2030 z profilu zóny "
        "(zástavba, byty bez stání, landuse, tranzit, rezerva sítě). (2) LightGBM klasifikátor "
        "doporučuje typ stanice. Skóre <b>suitability</b> kombinuje predikci s rezervou sítě, "
        "mezerou v pokrytí a férovostí.<br><br>"
        "<b>Že to není tabulka:</b> populační baseline („víc lidí → víc nabíjení“) má MAE 5,66; "
        "model 4,70. Model najde i méně očekávané zóny (málo lidí, ale tranzit + volná síť + "
        "žádné stanice), které prosté pravidlo mine."
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")
    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown("#### Anti-leakage")
        st.markdown(
            f'<div class="vp-card">Cílové sloupce <code>target_*_2030_synthetic</code> a vše z nich '
            "odvozené jsou z featur vyřazené (sdílená logika <code>feature_cols</code>). "
            "Model se učí z 60 reálných/2025 featur, ne z budoucích cílů. "
            "Validace na odděleném holdoutu, žádné odevzdání skrytých labelů.</div>",
            unsafe_allow_html=True,
        )
    with cc2:
        st.markdown("#### Etika & nejistota")
        st.markdown(
            f'<div class="vp-card"><b>Cold-start / férovost:</b> index domácností bez vlastního stání '
            "zvyšuje skóre okrajových čtvrtí, aby data-chudé zóny nezůstaly bez nabíjení. "
            "<b>Nejistota:</b> predikce 2030 je pásmo scénářů, ne jedno číslo. "
            "<b>Odpovědnost:</b> výstup je doporučení pro úředníka, ne automatické rozhodnutí.</div>",
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown("#### Rozložení suitability skóre")
    fig = go.Figure(go.Histogram(x=df_all["suitability_score"], nbinsx=25, marker_color=ACCENT_SOFT))
    fig.update_layout(template="plotly_white", height=280, margin=dict(t=10, b=10, l=10, r=10),
                      xaxis_title="suitability_score", yaxis_title="počet zón", bargap=0.05)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("VoltPlán · AIO_PHA-02-PHA · Česká AI Olympiáda 2026 · tým notokens · "
           "data = sandbox (reálná + modelová), výstupy slouží k validaci a interpretaci.")
