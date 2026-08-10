"""Módulo para carga y limpieza de datos de pases del Manchester United."""

from pathlib import Path

import pandas as pd

# Columnas numéricas conocidas del dataset FBref
_NUMERIC_COLS = [
    "90s",
    "Cmp",
    "Att",
    "Cmp%",
    "TotDist",
    "PrgDist",
    "Ast",
    "xA",
    "KP",
    "1/3",
    "PPA",
    "CrsPA",
    "Prog",
]

_PROJECT_ROOT = Path(__file__).parent.parent.parent


def _resolver_ruta(nombre: str) -> Path:
    """Resuelve la ruta de un archivo de datos.

    Prioriza: (1) rutas absolutas, (2) relativas al directorio actual,
    (3) relativas a la raíz del proyecto.

    Args:
        nombre: Nombre o ruta del archivo.

    Returns:
        Ruta absoluta resuelta.

    Raises:
        FileNotFoundError: si el archivo no existe en ningún candidato.
    """
    ruta = Path(nombre)
    if ruta.is_absolute():
        if not ruta.exists():
            raise FileNotFoundError(f"No se encontró '{nombre}'.")
        return ruta.resolve()

    candidatos = [ruta, Path.cwd() / ruta, _PROJECT_ROOT / ruta]
    for c in candidatos:
        if c.exists():
            return c.resolve()

    raise FileNotFoundError(f"No se encontró '{nombre}'. Colócalo en la raíz del proyecto.")


def load_data(
    passes_path: str = "passing.csv",
    report_path: str = "reporte_mediocampo.csv",
) -> tuple[pd.DataFrame, pd.DataFrame]:
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


def _prog_ratio(df: pd.DataFrame) -> pd.Series:
    """Calcula Prog / Cmp de forma vectorizada.

    El ratio es 0.0 cuando Cmp es nulo, no numérico o menor/igual a 0.

    Args:
        df: DataFrame con columnas 'Prog' y 'Cmp'.

    Returns:
        Serie con el ratio de pases progresivos (4 decimales).
    """
    if "Cmp" not in df.columns or "Prog" not in df.columns:
        return pd.Series(0.0, index=df.index, dtype=float)
    cmp = pd.to_numeric(df["Cmp"], errors="coerce")
    prog = pd.to_numeric(df["Prog"], errors="coerce")
    return (prog / cmp).where(cmp.gt(0), 0.0).round(4).fillna(0.0)


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

    df["Prog_Ratio"] = _prog_ratio(df)

    if "Pos" in df.columns:
        df = df[df["Pos"].str.contains("MF", na=False)].copy()

    df.sort_values("Prog_Ratio", ascending=False, inplace=True)

    return df.reset_index(drop=True)
