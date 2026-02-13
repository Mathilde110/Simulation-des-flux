import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Config page
st.set_page_config(page_title="Comptage Mobilité", layout="wide", page_icon="🚀")

# Style CSS personnalisé - SIMPLIFIÉ
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        color: #262730 !important;
    }
    [data-testid="stMetricValue"] {
        color: #262730 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #262730 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Simulation de comptage des flux de mobilité")
st.markdown("---")

# Rafraîchissement automatique toutes les 1 minute
st_autorefresh(interval=60_000, key="refresh")

# URL RAW du CSV sur GitHub
CSV_URL = "https://raw.githubusercontent.com/Mathilde110/Simulation-des-flux/main/compteurs.csv"

try:
    # Lecture du CSV
    df = pd.read_csv(CSV_URL)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Garder les 50 dernières lignes
    df_recent = df.tail(50)
    
    # Afficher les dernières valeurs avec delta
    last = df_recent.iloc[-1]
    previous = df_recent.iloc[-2] if len(df_recent) > 1 else last
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "👤 Humains", 
            int(last["humains"]),
            delta=int(last["humains"] - previous["humains"])
        )
    
    with col2:
        st.metric(
            "🚲 Vélos", 
            int(last["velos"]),
            delta=int(last["velos"] - previous["velos"])
        )
    
    with col3:
        st.metric(
            "📊 Total", 
            int(last["humains"] + last["velos"]),
            delta=int((last["humains"] + last["velos"]) - (previous["humains"] + previous["velos"]))
        )
    
    st.markdown("---")
    
    # Graphique Plotly interactif
    st.subheader("📈 Évolution des flux en temps réel")
    
    fig = px.line(
        df_recent, 
        x="timestamp", 
        y=["humains", "velos"],
        labels={"value": "Nombre", "timestamp": "Heure", "variable": "Type"},
        color_discrete_map={"humains": "#FF6B6B", "velos": "#4ECDC4"},
        template="plotly_white"
    )
    
    fig.update_layout(
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            title=""
        ),
        height=500,
        margin=dict(l=20, r=20, t=40, b=80),
        yaxis=dict(rangemode='tozero')
    )
    
    fig.update_traces(line=dict(width=3))
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.warning("⏳ En attente des données…")
    st.error(str(e)) des données…")
    st.error(str(e))

