"""Funciones sencillas para limpieza de los datos de pases."""
import pandas as pd

def clean_passes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Remover columnas completamente vacías
    df.dropna(axis=1, how='all', inplace=True)
    # Reemplazar cadenas vacías por NaN
    df.replace('', pd.NA, inplace=True)
    # Intentar convertir columnas numéricas conocidas
    numeric_cols = ['90s','Cmp','Att','TotDist','PrgDist']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'passing.csv'
    df = pd.read_csv(path)
    df_clean = clean_passes(df)
    print('Limpieza completada:', df_clean.shape)
