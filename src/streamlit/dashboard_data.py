import pandas as pd
import streamlit as st

@st.cache_data
def load_streamlit_data():
    """Carga los datos csv para visualizar en streamlit y calcula KPIs agregados."""
    df = pd.read_csv("data/raw/passing_players.csv")
    df_time = pd.read_csv("data/raw/passing_timeline.csv")
    
    kpis = {
        "avg_acc": df["pass_acc"].mean(),
        "avg_prog": df["prog_passes"].mean(),
        "avg_xt": df["xT_gen"].mean(),
        "avg_vert": df["vert_idx"].mean(),
        "total_losses": df["losses"].mean(),
    }
    
    return df, df_time, kpis
