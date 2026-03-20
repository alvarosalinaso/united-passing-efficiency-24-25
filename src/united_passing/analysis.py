"""Módulo de análisis de eficiencia de pases del Manchester United."""
import pandas as pd


def top_by_prog_ratio(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Top N jugadores por Prog_Ratio (pases progresivos / completados).

    Si Prog_Ratio no existe en el DataFrame, se calcula desde Prog y Cmp.
    Si tampoco existen esas columnas, devuelve las primeras top_n filas.

    Args:
        df: DataFrame limpio con estadísticas de pases.
        top_n: Número de jugadores a retornar.

    Returns:
        DataFrame ordenado por Prog_Ratio descendente.
    """
    df = df.copy()

    if "Prog_Ratio" not in df.columns:
        if {"Prog", "Cmp"}.issubset(df.columns):
            df["Prog_Ratio"] = df.apply(
                lambda r: round(r["Prog"] / r["Cmp"], 4) if r["Cmp"] > 0 else 0.0,
                axis=1,
            )
        else:
            return df.head(top_n)

    return df.sort_values("Prog_Ratio", ascending=False).head(top_n).reset_index(drop=True)


def filter_midfielders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra filas cuya columna 'Pos' contenga 'MF'.

    Args:
        df: DataFrame con columna 'Pos'.

    Returns:
        DataFrame filtrado. Si no existe 'Pos', retorna el DataFrame original.
    """
    if "Pos" not in df.columns:
        return df
    return df[df["Pos"].str.contains("MF", na=False)].reset_index(drop=True)


def resumen_estadisticas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tabla resumen con métricas clave por jugador.

    Args:
        df: DataFrame limpio de pases.

    Returns:
        DataFrame con Player, Cmp, Att, Cmp%, Prog, Prog_Ratio (si disponibles).
    """
    cols_deseadas = ["Player", "Pos", "90s", "Cmp", "Att", "Cmp%", "Prog", "Prog_Ratio", "KP", "xA"]
    cols_presentes = [c for c in cols_deseadas if c in df.columns]
    return df[cols_presentes].copy()
