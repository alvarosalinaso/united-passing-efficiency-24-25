import pandas as pd
import streamlit as st

from pathlib import Path
@st.cache_data(ttl=60)
def load_streamlit_data():
    base = Path(__file__).parent.parent.parent / "data" / "raw"
    df = pd.read_csv(base / "passing_players.csv")
    t_df = pd.read_csv(base / "passing_timeline.csv")
    df_teams = pd.read_csv(base / "pl_teams.csv")
    kpis = {
        "avg_acc": df["pass_acc"].mean(),
        "avg_prog": df["prog_passes"].mean(),
        "avg_xt": df["xT_gen"].mean(),
        "avg_vert": df["vert_idx"].mean(),
        "total_losses": df["losses"].mean(),
    }
    return df, t_df, df_teams, kpis
