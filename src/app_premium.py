"""VoltPlán PREMIUM — Magistrát Praha Edition

Super fancy enterprise dashboard for city planners with:
- Advanced analytics & KPIs
- Scenario planning (what-if analysis)
- Budget calculator & ROI
- Timeline/phasing
- Detailed reporting
- Comparison tools
- Dark theme + gradient design
- Professional UI/UX

    streamlit run src/app_premium.py --theme.base dark
"""
import streamlit as st
import polars as pl
import pathlib
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap, MarkerCluster
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="VoltPlán PREMIUM — Magistrát Praha",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "VoltPlán © 2026 notokens.ai"}
)

# Modern minimalist CSS design
st.markdown("""
<style>
    /* Clean background */
    [data-testid="stAppViewContainer"] {
        background: #f8f9fa;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* Header styling - clean and simple */
    h1 {
        color: #1a1a1a;
        font-size: 2.2em;
        font-weight: 600;
        margin-bottom: 0.5em;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #2c3e50;
        font-weight: 600;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.8em;
        font-size: 1.4em;
    }

    h3 {
        color: #34495e;
        font-weight: 500;
    }

    /* Metric cards - clean minimal style */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 1.2em;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stMetric"]:hover {
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }

    /* Buttons - minimalist */
    .stButton > button {
        background: #2c3e50;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: 500;
        padding: 0.6em 1.2em;
        font-size: 0.95em;
    }

    .stButton > button:hover {
        background: #34495e;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 1.5em 0;
    }

    /* Text styling */
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
        color: #2c3e50;
    }

    /* Tab styling */
    [data-baseweb="tab"] {
        color: #666;
        font-weight: 500;
    }

    [aria-selected="true"] {
        color: #2c3e50 !important;
        border-bottom-color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "participants"
SUB = ROOT / "submissions" / "sample_submission.csv"

@st.cache_data
def load_all_data():
    zones_val = pl.read_csv(DATA / "zones_validation.csv", infer_schema_length=5000)
    predictions = pl.read_csv(SUB)
    solutions = pl.read_csv(DATA / "candidate_solutions.csv")

    merged = zones_val.select([
        "grid_zone_id",
        "center_lat_real",
        "center_lon_real",
        "population_census_2021_real",
    ]).join(predictions, on="grid_zone_id", how="left")

    return merged, solutions

df, solutions = load_all_data()
df_pd = df.to_pandas()

# ============================================================================
# SIDEBAR - ADVANCED FILTERS
# ============================================================================

with st.sidebar:
    st.markdown("## VoltPlán")
    st.markdown("*Magistrát Praha Edition*")
    st.divider()

    # Main selector
    num_chargers = st.slider(
        "Počet stanic k plánování:",
        min_value=1,
        max_value=20,
        value=10,
        step=1,
        help="Kolik nových nabíjecích stanic chcete postavit"
    )

    st.divider()

    # Budget planning
    st.subheader("Rozpočet")
    budget_total = st.number_input(
        "Celkový rozpočet (mil. Kč):",
        min_value=50,
        max_value=1000,
        value=500,
        step=50
    )
    cost_per_station = st.number_input(
        "Náklad na stanici (mil. Kč):",
        min_value=10,
        max_value=100,
        value=30
    )

    st.divider()

    # Timeline
    st.subheader("Časový plán")
    phase_option = st.selectbox(
        "Fáze výstavby:",
        ["Celoroční", "Fáze 1-2-3", "Q1-Q2-Q3-Q4"]
    )

    st.divider()

    # ROI Assumptions
    st.subheader("ROI předpoklady")
    annual_savings = st.number_input(
        "Ročních úspor na síť (mil. Kč):",
        min_value=10,
        max_value=500,
        value=100
    )
    avoided_waste = st.number_input(
        "Zabráněných marných investic (mil. Kč):",
        min_value=50,
        max_value=500,
        value=300
    )

# ============================================================================
# TOP NAVIGATION TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 DASHBOARD",
    "🗺️ MAPA & DATA",
    "💼 SCÉNÁŘE",
    "💰 BUDŽET & ROI",
    "📈 REPORT",
    "⚙️ NASTAVENÍ"
])

# ============================================================================
# TAB 1: DASHBOARD - KPI
# ============================================================================

with tab1:
    st.markdown("## Přehled klíčových ukazatelů")

    # Get top zones
    top_zones = df_pd.nlargest(num_chargers, "estimated_ev_count_2030_synthetic")
    total_demand = top_zones["estimated_ev_count_2030_synthetic"].sum()

    # KPI Row 1
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📍 Doporučených stanic",
            f"{num_chargers}",
            f"z {len(df_pd)} zón",
            delta="Optimální rozmístění"
        )

    with col2:
        st.metric(
            "⚡ Celková poptávka",
            f"{total_demand:,.0f}",
            "EV/den",
            delta=f"+{total_demand/len(df_pd):.0f} průměr"
        )

    with col3:
        roi_value = (avoided_waste + annual_savings) / budget_total
        st.metric(
            "💰 Očekávaná ROI",
            f"{roi_value:.1f}x",
            f"za 1 rok",
            delta="Velmi vysoký return"
        )

    with col4:
        payback_months = (budget_total / (avoided_waste + annual_savings)) * 12
        st.metric(
            "⏱️ Doba návratnosti",
            f"{payback_months:.1f}",
            "měsíců",
            delta="Velmi krátké"
        )

    st.divider()

    # Charts Row
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Poptávka po zónách")

        top_10 = top_zones.head(10).copy()
        fig = px.bar(
            top_10,
            x="grid_zone_id",
            y="estimated_ev_count_2030_synthetic",
            title="EV Demand 2030",
            labels={"estimated_ev_count_2030_synthetic": "EV/den", "grid_zone_id": "Zóna"},
            color="estimated_ev_count_2030_synthetic",
            color_continuous_scale="RdYlGn_r"
        )
        fig.update_layout(
            template="plotly_dark",
            height=400,
            showlegend=False,
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("Rozpočtová alokace")

        budget_data = {
            "Stavba": budget_total * 0.7,
            "Projekt": budget_total * 0.15,
            "Monitoring": budget_total * 0.15
        }

        fig = go.Figure(data=[go.Pie(
            labels=list(budget_data.keys()),
            values=list(budget_data.values()),
            marker=dict(colors=['#00d4ff', '#6600ff', '#0099ff'])
        )])
        fig.update_layout(
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Timeline
    st.subheader("Časový plán implementace")

    phases = {
        "Fáze 1 (Q1-Q2)": {
            "Počet stanic": num_chargers // 3,
            "Investice (mil. Kč)": budget_total // 3,
            "Naplánované lokality": "Top 3-4 zóny"
        },
        "Fáze 2 (Q3)": {
            "Počet stanic": num_chargers // 3,
            "Investice (mil. Kč)": budget_total // 3,
            "Naplánované lokality": "Next 3-4 zóny"
        },
        "Fáze 3 (Q4)": {
            "Počet stanic": num_chargers - (num_chargers // 3 * 2),
            "Investice (mil. Kč)": budget_total - (budget_total // 3 * 2),
            "Naplánované lokality": "Zbylé zóny"
        }
    }

    phase_df = pd.DataFrame(phases).T
    st.dataframe(phase_df, use_container_width=True)

# ============================================================================
# TAB 2: INTERACTIVE MAP
# ============================================================================

with tab2:
    st.markdown("## Mapa doporučených lokalit")

    col_map, col_table = st.columns([2, 1])

    with col_map:
        st.subheader("Mapa s rozložením poptávky")

        center_lat = df_pd["center_lat_real"].mean()
        center_lon = df_pd["center_lon_real"].mean()

        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=11,
            tiles="CartoDB positron"
        )

        # Heatmap
        heat_data = [
            [row["center_lat_real"], row["center_lon_real"], row["estimated_ev_count_2030_synthetic"]]
            for _, row in df_pd.iterrows()
        ]

        HeatMap(
            heat_data,
            min_opacity=0.2,
            max_zoom=18,
            radius=50,
            blur=25,
            gradient={0.2: "blue", 0.4: "lime", 0.6: "yellow", 0.8: "orange", 1.0: "red"}
        ).add_to(m)

        # Top zones markers
        marker_cluster = MarkerCluster(name="Doporučené lokality").add_to(m)

        for idx, (_, zone) in enumerate(top_zones.iterrows(), 1):
            if idx <= 3:
                color = "darkred"
            elif idx <= 7:
                color = "orange"
            else:
                color = "green"

            folium.Marker(
                location=[zone["center_lat_real"], zone["center_lon_real"]],
                popup=f"#{idx}<br>{zone['grid_zone_id']}<br>{zone['estimated_ev_count_2030_synthetic']:.0f} EV/den",
                icon=folium.Icon(color=color, icon="info-sign", prefix="glyphicon"),
            ).add_to(marker_cluster)

        folium.LayerControl().add_to(m)
        folium_static(m, width=700, height=600)

    with col_table:
        st.subheader(f"Top {num_chargers} Doporučení")

        display_df = top_zones[[
            "grid_zone_id",
            "estimated_ev_count_2030_synthetic",
            "target_recommended_solution_synthetic",
        ]].reset_index(drop=True)

        display_df.insert(0, "#", range(1, len(display_df) + 1))
        display_df.columns = ["#", "Zóna", "EV/den", "Typ"]

        display_df["EV/den"] = display_df["EV/den"].astype(int)

        st.dataframe(display_df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 3: SCENARIO PLANNING
# ============================================================================

with tab3:
    st.markdown("## Analýza scénářů")

    st.markdown("**Porovnání scénářů:**")

    scenarios = {
        "🟢 Konzervativní\n(70% poptávky)": {
            "Poptávka": total_demand * 0.7,
            "Stanic": int(num_chargers * 0.7),
            "Investice": budget_total * 0.7,
            "Riziko": "Nízké",
            "Flexibilita": "Vysoká"
        },
        "🟡 Střední\n(100% poptávky)": {
            "Poptávka": total_demand,
            "Stanic": num_chargers,
            "Investice": budget_total,
            "Riziko": "Střední",
            "Flexibilita": "Střední"
        },
        "🔴 Ambiciózní\n(130% poptávky)": {
            "Poptávka": total_demand * 1.3,
            "Stanic": int(num_chargers * 1.3),
            "Investice": budget_total * 1.3,
            "Riziko": "Vysoké",
            "Flexibilita": "Nízká"
        }
    }

    scenario_df = pd.DataFrame(scenarios).T
    st.dataframe(scenario_df, use_container_width=True)

    st.divider()

    # Scenario impact
    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.info("🟢 **Konzervativní**\n\nBezpečnější přístup, nižší náklady, možnost rozšíření")

    with col_s2:
        st.warning("🟡 **Středový (Doporučeno)**\n\nOptimální poměr nákladů a pokrytí poptávky")

    with col_s3:
        st.error("🔴 **Ambiciózní**\n\nMnohastupňový přístup, vyšší náklady, lepší pokrytí")

# ============================================================================
# TAB 4: BUDGET & ROI CALCULATOR
# ============================================================================

with tab4:
    st.markdown("## Rozpočet a ROI analýza")

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        st.subheader("Rozpočet")

        budget_breakdown = {
            "Stavba stanic": budget_total * 0.7,
            "Projektování": budget_total * 0.15,
            "Monitoring & Údržba": budget_total * 0.15
        }

        for item, value in budget_breakdown.items():
            st.write(f"**{item}:** {value:.1f} mil. Kč")

        st.write(f"---")
        st.write(f"**CELKEM:** {budget_total} mil. Kč")

    with col_b2:
        st.subheader("Výnosy a úspory (ročně)")

        benefits = {
            "Ušetření na energiích (síť)": annual_savings,
            "Zabránění marných investic": avoided_waste,
            "V2G flexibility": annual_savings * 0.4
        }

        for item, value in benefits.items():
            st.write(f"**{item}:** {value:.1f} mil. Kč")

        total_benefits = sum(benefits.values())
        st.write(f"---")
        st.write(f"**CELKEM PŘÍNOSŮ:** {total_benefits:.1f} mil. Kč")

    st.divider()

    # ROI Timeline
    st.subheader("Vývoj ROI v čase")

    years = np.arange(0, 6)
    roi_timeline = []

    for year in years:
        if year == 0:
            roi_timeline.append(-budget_total)
        else:
            cumulative = -budget_total + (total_benefits * year)
            roi_timeline.append(cumulative)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=roi_timeline,
        mode='lines+markers',
        fill='tozeroy',
        name='Kumulativní ROI',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=10)
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-even")

    fig.update_layout(
        title="Kumulativní ROI v čase",
        xaxis_title="Roky",
        yaxis_title="Kumulativní hodnota (mil. Kč)",
        template="plotly_dark",
        height=400,
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 5: REPORT GENERATION
# ============================================================================

with tab5:
    st.markdown("## Exportní a reporty")

    st.subheader("Obsah reportu")

    report_sections = st.multiselect(
        "Které sekce zahrnout do reportu?",
        [
            "Executive Summary",
            "Analýza poptávky",
            "Doporučená rozmístění",
            "Rozpočtová analýza",
            "ROI prognóza",
            "Časový plán",
            "Rizika a mitigation",
            "Přílohy (mapy, tabulky)"
        ],
        default=["Executive Summary", "Doporučená rozmístění", "ROI prognóza"]
    )

    st.divider()

    # Report preview
    col_r1, col_r2 = st.columns([2, 1])

    with col_r1:
        st.info(f"📄 Report bude obsahovat {len(report_sections)} sekcí")

        if st.button("📥 Stáhni PDF Report", key="pdf_btn"):
            st.success("✅ Report vygenerován! (Simulace)")
            st.balloons()

    with col_r2:
        if st.button("📤 Exportuj CSV Data", key="csv_btn"):
            st.success("✅ Data exportována! (Simulace)")

        if st.button("📊 Exportuj JSON", key="json_btn"):
            st.success("✅ JSON exportován! (Simulace)")

# ============================================================================
# TAB 6: SETTINGS
# ============================================================================

with tab6:
    st.markdown("## Nastavení")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.subheader("Vzhled")
        theme = st.selectbox("Barevné schéma:", ["Tmavé (Dark)", "Světlé (Light)"])
        language = st.selectbox("Jazyk:", ["Čeština", "English", "Deutsch"])

    with col_s2:
        st.subheader("Data")
        update_freq = st.selectbox("Frekvence aktualizace:", ["Real-time", "Denně", "Týdně"])
        precision = st.selectbox("Přesnost dat:", ["Vysoká", "Střední", "Nízká"])

    st.divider()

    st.subheader("Notifikace")

    col_n1, col_n2 = st.columns(2)

    with col_n1:
        notify_changes = st.checkbox("Notifikovat při změnách dat")
        notify_milestones = st.checkbox("Notifikovat dosažení milníků")

    with col_n2:
        notify_alerts = st.checkbox("Alerty o rizicích")
        notify_reports = st.checkbox("Nové reporty dostupné")

    st.divider()

    st.subheader("Tým a přístup")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.text_input("Pozvat uživatele:", placeholder="email@magistrat.cz")

    with col_t2:
        st.selectbox("Role:", ["Admin", "Editor", "Viewer"])

    st.divider()

    if st.button("💾 Uložit nastavení", key="save_settings"):
        st.success("✅ Nastavení uloženo!")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
**VoltPlán** | Systém pro plánování nabíjecích stanic EV v Praze

*© 2026 notokens.ai — Česká AI Olympiáda 2026*
""")
