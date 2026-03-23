import pandas as pd
from pathlib import Path

NUMS = ["90s", "Cmp", "Att", "Cmp%", "TotDist", "PrgDist", "Ast", "xA", "KP", "1/3", "PPA", "CrsPA", "Prog"]
ROOT = Path(__file__).parent.parent.parent

def _locate(f_name: str) -> Path:
    for c in [Path(f_name), Path.cwd() / f_name, ROOT / f_name]:
        if c.exists(): return c.resolve()
    raise FileNotFoundError(f"Missing '{f_name}'")

def pull_files(base="passing.csv", rep="reporte_mediocampo.csv"):
    d_f = pd.read_csv(_locate(base))
    try:
        r_f = pd.read_csv(_locate(rep))
    except FileNotFoundError:
        r_f = pd.DataFrame()
    return d_f, r_f

def sanitize(d_f: pd.DataFrame) -> pd.DataFrame:
    t = d_f.copy()
    t.dropna(axis=1, how="all", inplace=True)
    t.replace(r"^\s*$", pd.NA, regex=True, inplace=True)
    for c in NUMS:
        if c in t.columns: t[c] = pd.to_numeric(t[c], errors="coerce")
    return t

def gen_mf_report(d_f: pd.DataFrame) -> pd.DataFrame:
    t = d_f.copy()
    if {"Prog", "Cmp"}.issubset(t.columns):
        t["Prog_Ratio"] = t.apply(lambda row: round(row["Prog"] / row["Cmp"], 4) if row["Cmp"] else 0.0, axis=1)
    if "Pos" in t.columns:
        t = t[t["Pos"].str.contains("MF", na=False)]
    if "Prog_Ratio" in t.columns:
        t.sort_values("Prog_Ratio", ascending=False, inplace=True)
    return t.reset_index(drop=True)
