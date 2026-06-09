"""app.py — minimální VoltPlán demo (Streamlit). Mapa zón obarvená predikcí + top zóny.

    streamlit run src/app.py

Předpoklad: hotová submission (src/train_demand.py) + zones_test.csv s lat/lon.
Skelet — na místě dolaď názvy sloupců. HNED po rozjetí udělej screenshot/záznam jako zálohu.
"""
from __future__ import annotations
import pathlib
import polars as pl
import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "participants"
SUB = ROOT / "submissions" / "predictions_validation.csv"

st.set_page_config(page_title="VoltPlán — Praha mobilita & energetika", layout="wide")
st.title("⚡ VoltPlán — chytré nabíjení, síť a V2G v Praze")
st.caption("Predikce poptávky/zátěže 2030 po zónách · řízené nabíjení + V2G · AIO_PHA-02-PHA")


@st.cache_data
def load():
    zones = pl.read_csv(next(DATA.rglob("zones_validation.csv")), ignore_errors=True)
    pred = pl.read_csv(SUB) if SUB.exists() else None
    return zones, pred


zones, pred = load()
zid = next((c for c in zones.columns if "grid_zone_id" in c.lower()), zones.columns[0])
lat = next((c for c in zones.columns if "lat" in c.lower()), None)
lon = next((c for c in zones.columns if "lon" in c.lower()), None)

if pred is not None:
    target = next((c for c in pred.columns if c.startswith("pred_")), [c for c in pred.columns if c != zid][0])
    df = zones.join(pred, on=zid, how="left")
    st.sidebar.metric("Zón", df.height)
    st.sidebar.metric("Predikovaný cíl", target)

    if lat and lon:
        import pydeck as pdk
        d = df.select([lat, lon, target]).drop_nulls().to_pandas()
        d["w"] = (d[target] - d[target].min()) / (d[target].max() - d[target].min() + 1e-9)
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(latitude=d[lat].mean(), longitude=d[lon].mean(),
                                             zoom=10, pitch=0),
            layers=[pdk.Layer("ScatterplotLayer", d, get_position=f"[{lon}, {lat}]",
                              get_radius="120 + w*400", get_fill_color="[255, 140*(1-w), 0, 160]",
                              pickable=True)],
            tooltip={"text": f"{target}: {{{target}}}"},
        ))
    else:
        st.info("Bez lat/lon sloupců — ukazuju jen tabulku.")

    st.subheader("Top 20 zón podle predikované poptávky")
    st.dataframe(df.sort(target, descending=True).head(20).to_pandas(), use_container_width=True)
else:
    st.warning("Chybí submissions/predictions_validation.csv — spusť nejdřív `python src/train_demand.py`.")
