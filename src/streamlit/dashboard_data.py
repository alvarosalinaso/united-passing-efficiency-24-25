import pandas as pd
import streamlit as st

@st.cache_data
def load_streamlit_data():
    df = pd.read_csv("data/raw/passing_players.csv")
    t_df = pd.read_csv("data/raw/passing_timeline.csv")
    kpis = {
        "avg_acc": df["pass_acc"].mean(),
        "avg_prog": df["prog_passes"].mean(),
        "avg_xt": df["xT_gen"].mean(),
        "avg_vert": df["vert_idx"].mean(),
        "total_losses": df["losses"].mean(),
    }
    return df, t_df, kpis
