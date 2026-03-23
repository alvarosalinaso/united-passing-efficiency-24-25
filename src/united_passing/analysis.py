import pandas as pd

def top_prog(d_f: pd.DataFrame, tops: int = 10) -> pd.DataFrame:
    t_df = d_f.copy()
    if "Prog_Ratio" not in t_df.columns:
        if {"Prog", "Cmp"}.issubset(t_df.columns):
            t_df["Prog_Ratio"] = t_df.apply(lambda r: round(r["Prog"] / r["Cmp"], 4) if r["Cmp"] > 0 else 0.0, axis=1)
        else:
            return t_df.head(tops)
    return t_df.sort_values("Prog_Ratio", ascending=False).head(tops).reset_index(drop=True)

def mfs_only(d_f: pd.DataFrame) -> pd.DataFrame:
    return d_f[d_f["Pos"].str.contains("MF", na=False)].reset_index(drop=True) if "Pos" in d_f.columns else d_f

def slim_stats(d_f: pd.DataFrame) -> pd.DataFrame:
    req = ["Player", "Pos", "90s", "Cmp", "Att", "Cmp%", "Prog", "Prog_Ratio", "KP", "xA"]
    return d_f[[c for c in req if c in d_f.columns]].copy()
