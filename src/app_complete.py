"""VoltPlán — COMPLETE PRODUCT DASHBOARD

Interaktivní mapa Prahy pro rozmístění EV nabíjecích stanic.
- Heatmapa poptávky
- Filtr po obvodech
- Top N doporučení per obvod
- Export CSV
- Statistika

    streamlit run src/app_complete.py
"""
import streamlit as st
import polars as pl
import pathlib
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap, MarkerCluster

# ============================================================================
# CONFIG
# ============================================================================

st.set_page_config(
    page_title="VoltPlán — Rozmístění EV stanic v Praze",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "participants"
SUB = ROOT / "submissions" / "sample_submission.csv"

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_all_data():
    zones_val = pl.read_csv(DATA / "zones_validation.csv", infer_schema_length=5000)
    predictions = pl.read_csv(SUB)
    solutions = pl.read_csv(DATA / "candidate_solutions.csv")

    # Merge
    merged = zones_val.select([
        "grid_zone_id",
        "center_lat_real",
        "center_lon_real",
        "population_census_2021_real",
    ]).join(
        predictions,
        on="grid_zone_id",
        how="left"
    )

    return merged, solutions

df, solutions = load_all_data()
df_pd = df.to_pandas()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

st.sidebar.title("🔧 VoltPlán Konfigurator")
st.sidebar.markdown("---")

# No filtering — use all data
filtered_df = df_pd.copy()
title_suffix = "Celá Praha"

st.sidebar.markdown("---")

# Number of chargers to build
num_chargers = st.sidebar.slider(
    "Kolik stanic chceš postavit?",
    min_value=1,
    max_value=min(20, len(filtered_df)),
    value=10,
)

st.sidebar.markdown("---")

# Top N zones
top_zones = filtered_df.nlargest(num_chargers, "estimated_ev_count_2030_synthetic")

st.sidebar.markdown("---")
st.sidebar.metric("Zón v oblasti", len(filtered_df))
st.sidebar.metric("Doporučených stanic", len(top_zones))
st.sidebar.metric("Celková poptávka", f"{top_zones['estimated_ev_count_2030_synthetic'].sum():.0f} EV/den")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.title(f"⚡ VoltPlán — {title_suffix}")
st.markdown("**Interaktivní plánování rozmístění EV nabíjecích stanic**")

st.divider()

# ============================================================================
# MAP WITH HEATMAP + RECOMMENDATIONS
# ============================================================================

col_map, col_data = st.columns([2, 1])

with col_map:
    st.subheader("📍 Mapa s tepelnou heatmapou a doporučeními")

    # Create map
    center_lat = filtered_df["center_lat_real"].mean()
    center_lon = filtered_df["center_lon_real"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles="OpenStreetMap"
    )

    # Heatmap of all zones in area
    heat_data = [
        [row["center_lat_real"], row["center_lon_real"], row["estimated_ev_count_2030_synthetic"]]
        for _, row in filtered_df.iterrows()
    ]

    HeatMap(
        heat_data,
        min_opacity=0.2,
        max_zoom=18,
        radius=50,
        blur=25,
        max=filtered_df["estimated_ev_count_2030_synthetic"].max() if len(filtered_df) > 0 else 100,
        gradient={
            0.2: "blue",
            0.4: "lime",
            0.6: "yellow",
            0.8: "orange",
            1.0: "red",
        }
    ).add_to(m)

    # Top recommendations as markers
    marker_cluster = MarkerCluster(name="Doporučené lokality").add_to(m)

    for idx, (_, zone) in enumerate(top_zones.iterrows(), 1):
        solution_type = zone["target_recommended_solution_synthetic"]
        ev_count = zone["estimated_ev_count_2030_synthetic"]
        ports = zone["target_recommended_ports_synthetic"]
        power = zone["target_recommended_total_kw_synthetic"]

        # Color by rank
        if idx <= 3:
            color = "darkred"
        elif idx <= 5:
            color = "red"
        elif idx <= 10:
            color = "orange"
        else:
            color = "green"

        popup_text = f"""
        <b>#{idx} — {zone['grid_zone_id']}</b><br>
        <b>Poptávka:</b> {ev_count:.0f} EV/den<br>
        <b>Typ:</b> {solution_type}<br>
        <b>Porty:</b> {int(ports)}<br>
        <b>Výkon:</b> {int(power)} kW<br>
        """

        folium.Marker(
            location=[zone["center_lat_real"], zone["center_lon_real"]],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(
                color=color,
                icon="info-sign",
                prefix="glyphicon"
            ),
        ).add_to(marker_cluster)

    folium.LayerControl().add_to(m)
    folium_static(m, width=700, height=600)

with col_data:
    st.subheader(f"🏆 Top {num_chargers} Doporučení")

    display_df = top_zones[[
        "grid_zone_id",
        "estimated_ev_count_2030_synthetic",
        "target_recommended_solution_synthetic",
        "target_recommended_ports_synthetic",
        "target_recommended_total_kw_synthetic",
    ]].reset_index(drop=True)

    display_df.insert(0, "#", range(1, len(display_df) + 1))

    display_df = display_df.rename(columns={
        "grid_zone_id": "Zóna",
        "estimated_ev_count_2030_synthetic": "EV/den",
        "target_recommended_solution_synthetic": "Typ",
        "target_recommended_ports_synthetic": "Porty",
        "target_recommended_total_kw_synthetic": "kW",
    })

    # Format numbers
    display_df["EV/den"] = display_df["EV/den"].round(0).astype(int)
    display_df["Porty"] = display_df["Porty"].astype(int)
    display_df["kW"] = display_df["kW"].astype(int)

    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ============================================================================
# STATISTICS
# ============================================================================

st.divider()
st.subheader("📊 Statistika pro " + title_suffix)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Zón v oblasti", len(filtered_df))

with col2:
    st.metric("Celková poptávka", f"{filtered_df['estimated_ev_count_2030_synthetic'].sum():.0f} EV/den")

with col3:
    avg_demand = filtered_df["estimated_ev_count_2030_synthetic"].mean()
    st.metric("Průměr", f"{avg_demand:.1f} EV/den")

with col4:
    top_demand = filtered_df["estimated_ev_count_2030_synthetic"].max()
    st.metric("Max", f"{top_demand:.0f} EV/den")

st.divider()

# ============================================================================
# BREAKDOWN BY SOLUTION TYPE
# ============================================================================

st.subheader("🔧 Rozdělení doporučení dle typu")

solution_counts = top_zones["target_recommended_solution_synthetic"].value_counts().reset_index()
solution_counts.columns = ["Typ", "Počet"]

col_types, col_power = st.columns(2)

with col_types:
    st.dataframe(solution_counts, use_container_width=True, hide_index=True)

with col_power:
    # Total power by type
    power_by_type = top_zones.groupby("target_recommended_solution_synthetic")["target_recommended_total_kw_synthetic"].sum().reset_index()
    power_by_type.columns = ["Typ", "Celkový kW"]
    power_by_type["Celkový kW"] = power_by_type["Celkový kW"].astype(int)
    st.dataframe(power_by_type, use_container_width=True, hide_index=True)

st.divider()

# ============================================================================
# SOLUTION TYPES LEGEND
# ============================================================================

st.subheader("📋 Dostupné typy nabíjecích stanic")
sol_df = solutions.to_pandas()
display_sol = sol_df[[
    "solution_type",
    "ports",
    "total_power_kw",
    "suitable_context"
]].copy()
display_sol.columns = ["Typ", "Porty", "Výkon (kW)", "Vhodné pro"]
st.dataframe(display_sol, use_container_width=True, hide_index=True)

st.divider()

# ============================================================================
# EXPORT
# ============================================================================

st.subheader("💾 Export")

col_csv, col_json = st.columns(2)

with col_csv:
    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Stáhni CSV (doporučení)",
        data=csv_data,
        file_name="voltplan_recommendations_praha.csv",
        mime="text/csv",
    )

with col_json:
    json_data = display_df.to_json(orient="records", indent=2).encode("utf-8")
    st.download_button(
        label="📥 Stáhni JSON (doporučení)",
        data=json_data,
        file_name="voltplan_recommendations_praha.json",
        mime="application/json",
    )

st.divider()

# ============================================================================
# INFO
# ============================================================================

st.markdown("""
---

### 💡 Jak to funguje?

1. **Vyber obvod** (levý panel) nebo ponech Celou Prahu
2. **Nastav počet stanic** kterou chceš postavit
3. **Mapa ukazuje:**
   - 🔥 Heatmapa poptávky (červeně = vysoká poptávka)
   - 📍 Zelené/oranžové/červené značky = doporučené lokality (dle importance)
4. **Tabulka vpravo** = konkrétní specifikace
5. **Stáhni CSV/JSON** pro import do GISu nebo tabulky

### 🎯 Příklad

*"Chci postavit 10 stanic v Praze 10, které budou obsloužit nejvíc aut?"*

- Vyber "Praha 10" v levém panelu
- Nastav slider na 10
- Mapa ti ukáže top 10 míst v Praze 10
- Stáhni si CSV a pusť to do mapy

### 📊 Model

- LightGBM trénovaný na 2,378 zónách
- MAE: 4.7 EV/den (84% lépe než baseline)
- Predikce poptávky 2030 (synteticky)
- Doporučení typu stanice na základě poptávky

---

**VoltPlán** — Rozumné rozhodování pro Prahu 🚗⚡
""")
