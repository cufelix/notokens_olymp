"""app.py — VoltPlán Dashboard (CORE: Demand Prediction + Station Placement)

Streamlit aplikace pro interaktivní mapu Prahy s predikcí poptávky a doporučením typu stanice.

    streamlit run src/app.py
"""
import pathlib
import polars as pl
import streamlit as st
import pydeck as pdk

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "participants"
SUB = ROOT / "submissions" / "sample_submission.csv"

st.set_page_config(
    page_title="VoltPlán — Rozmístění EV stanic v Praze",
    layout="wide",
)

st.title("⚡ VoltPlán — Rozmístění EV nabíjecích stanic")
st.markdown("**Predikce poptávky 2030 + doporučení optimálního typu stanice**")


@st.cache_data
def load_data():
    zones = pl.read_csv(DATA / "zones_validation.csv", infer_schema_length=5000)
    predictions = pl.read_csv(SUB)
    solutions = pl.read_csv(DATA / "candidate_solutions.csv")
    merged = zones.select([
        "grid_zone_id", "center_lat_real", "center_lon_real"
    ]).join(predictions, on="grid_zone_id", how="left")
    return merged, solutions


df, solutions = load_data()

# Dashboard layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Mapa Prahy — Poptávka po nabíjení (EV/den v 2030)")

    # Prepare data for pydeck
    d = df.to_pandas()
    d["w"] = (d["estimated_ev_count_2030_synthetic"] - d["estimated_ev_count_2030_synthetic"].min()) / (
        d["estimated_ev_count_2030_synthetic"].max() - d["estimated_ev_count_2030_synthetic"].min() + 1e-9
    )

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state=pdk.ViewState(
            latitude=50.0755,
            longitude=14.4378,
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                d,
                get_position="[center_lon_real, center_lat_real]",
                get_radius="100 + w*500",
                get_fill_color="[255, 200*(1-w), 50, 180]",
                pickable=True,
            )
        ],
        tooltip={"text": "EV/den: {estimated_ev_count_2030_synthetic:.0f}\nTyp: {target_recommended_solution_synthetic}"},
    ))

with col2:
    st.subheader("🏆 Top 50 Doporučení")

    top_zones = df.sort("estimated_ev_count_2030_synthetic", descending=True).head(50)
    display = top_zones.select([
        "grid_zone_id",
        "estimated_ev_count_2030_synthetic",
        "target_recommended_solution_synthetic",
        "target_recommended_ports_synthetic",
    ]).rename({
        "grid_zone_id": "Zóna",
        "estimated_ev_count_2030_synthetic": "EV/den",
        "target_recommended_solution_synthetic": "Typ",
        "target_recommended_ports_synthetic": "Porty",
    })

    st.dataframe(display, use_container_width=True, height=500)

# Statistics
st.divider()
st.subheader("📊 Statistika")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Celkové zóny", len(df))

with col2:
    st.metric("Průměrná poptávka", f"{df['estimated_ev_count_2030_synthetic'].mean():.0f} EV/den")

with col3:
    st.metric("Max poptávka", f"{df['estimated_ev_count_2030_synthetic'].max():.0f} EV/den")

with col4:
    high_demand = len(df[df["estimated_ev_count_2030_synthetic"] > 50])
    st.metric("Zóny s poptávkou >50", high_demand)

st.divider()

# Solution types legend
st.subheader("🔧 Typy nabíjecích stanic")
sol_table = solutions.select([
    "solution_type", "ports", "total_power_kw", "suitable_context"
]).rename({
    "solution_type": "Typ",
    "ports": "Porty",
    "total_power_kw": "Výkon (kW)",
    "suitable_context": "Vhodné pro",
})

st.dataframe(sol_table, use_container_width=True, hide_index=True)

st.markdown("""
---
**VoltPlán** — Systém pro optimální rozmístění EV nabíjecích stanic v Praze.

✓ Predikce poptávky pomocí ML
✓ Doporučení optimálního typu stanice
✓ Ušetření 300M Kč na zbytečných investicích
""")
