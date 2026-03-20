"""Módulo para carga y limpieza de datos de pases del Manchester United."""
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

# Columnas numéricas conocidas del dataset FBref
_NUMERIC_COLS = [
    "90s", "Cmp", "Att", "Cmp%", "TotDist", "PrgDist",
    "Ast", "xA", "KP", "1/3", "PPA", "CrsPA", "Prog",
]

_PROJECT_ROOT = Path(__file__).parent.parent.parent


def _resolver_ruta(nombre: str) -> Path:
    """Busca el archivo en CWD y en la raíz del proyecto."""
    candidatos = [Path(nombre), Path.cwd() / nombre, _PROJECT_ROOT / nombre]
    for c in candidatos:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError(
        f"No se encontró '{nombre}'. Colócalo en la raíz del proyecto."
    )


def load_data(
    passes_path: str = "passing.csv",
    report_path: str = "reporte_mediocampo.csv",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga los datos de pases y el reporte de mediocampo.

    Args:
        passes_path: Nombre/ruta del CSV de pases (FBref).
        report_path: Nombre/ruta del CSV de reporte de mediocampo.

    Returns:
        Tupla (df_pases, df_reporte). df_reporte puede ser vacío
        si el archivo no existe todavía.
    """
    df = pd.read_csv(_resolver_ruta(passes_path))

    try:
        report = pd.read_csv(_resolver_ruta(report_path))
    except FileNotFoundError:
        report = pd.DataFrame()

    return df, report


def clean_passes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el DataFrame de pases:
      - Elimina columnas completamente vacías.
      - Convierte strings vacíos a NaN.
      - Coerce columnas numéricas conocidas.

    Args:
        df: DataFrame crudo de pases.

    Returns:
        DataFrame limpio.
    """
    df = df.copy()

    # Eliminar columnas 100% vacías
    df.dropna(axis=1, how="all", inplace=True)

    # Strings vacíos → NaN
    df.replace(r"^\s*$", pd.NA, regex=True, inplace=True)

    # Convertir numéricas conocidas
    for col in _NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def build_midfield_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera el reporte de mediocampo calculando Prog_Ratio y filtrando MF.

    Args:
        df: DataFrame limpio de pases.

    Returns:
        DataFrame con columna Prog_Ratio, ordenado descendente.
    """
    df = df.copy()

    if "Prog" in df.columns and "Cmp" in df.columns:
        df["Prog_Ratio"] = df.apply(
            lambda r: round(r["Prog"] / r["Cmp"], 4) if r["Cmp"] and r["Cmp"] > 0 else 0.0,
            axis=1,
        )

    if "Pos" in df.columns:
        df = df[df["Pos"].str.contains("MF", na=False)].copy()

    if "Prog_Ratio" in df.columns:
        df.sort_values("Prog_Ratio", ascending=False, inplace=True)

    return df.reset_index(drop=True)
