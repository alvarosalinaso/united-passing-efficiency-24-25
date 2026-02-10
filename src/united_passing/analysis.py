"""Módulo de análisis de datos."""
import pandas as pd

def top_by_prog_ratio(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Obtiene el top N de jugadores ordenados por Prog_Ratio.
    Calcula Prog_Ratio si no existe (Prog / Cmp).
    """
    df = df.copy()
    
    # Calcular Prog_Ratio si no está presente y tenemos las columnas necesarias
    if 'Prog_Ratio' not in df.columns:
        if 'Prog' in df.columns and 'Cmp' in df.columns:
            # Evitar división por cero
            df['Prog_Ratio'] = df.apply(
                lambda x: x['Prog'] / x['Cmp'] if x['Cmp'] > 0 else 0, axis=1
            )
        else:
             # Si no podemos calcularlo y no está, devolvemos vacío o error
             # Por compatibilidad con el script anterior, asumiremos que el input puede ser el 'reporte' que ya lo tenga
             pass

    if 'Prog_Ratio' in df.columns:
        df_sorted = df.sort_values('Prog_Ratio', ascending=False)
        return df_sorted.head(top_n)
    else:
        # Fallback si no hay métrica
        return df.head(top_n)

def filter_midfielders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra jugadores que son mediocampistas (MF).
    Asume columna 'Pos' con valores como 'MF', 'MFDF', etc.
    """
    if 'Pos' in df.columns:
        return df[df['Pos'].str.contains('MF', na=False)]
    return df
