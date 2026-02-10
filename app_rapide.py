import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Comptage Mobilité", layout="centered")
st.title("Simulation de comptage des flux de mobilité 🚀")

# Rafraîchissement automatique toutes les 0,5s
st_autorefresh(interval=500, key="refresh")

try:
    df = pd.read_csv("compteurs.csv")
    df = df.tail(50)  # ne garder que les 50 dernières lignes

    last = df.iloc[-1]

    col1, col2 = st.columns(2)
    col1.metric("👤 Humains", int(last["humains"]))
    col2.metric("🚲 Vélos", int(last["velos"]))

    st.line_chart(df.set_index("timestamp")[["humains", "velos"]])

except Exception:
    st.warning("En attente des données…")