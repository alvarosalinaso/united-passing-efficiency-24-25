import pandas as pd
from clean_data import clean_passes


def test_clean_passes_numeric_conversion():
    df = pd.read_csv('passing.csv')
    df_clean = clean_passes(df)
    assert '90s' in df_clean.columns
    assert pd.api.types.is_numeric_dtype(df_clean['90s']), 'La columna 90s debería ser numérica después de la limpieza'
