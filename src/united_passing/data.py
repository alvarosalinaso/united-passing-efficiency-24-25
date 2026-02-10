"""Módulo para carga y limpieza de datos."""
import pandas as pd
from pathlib import Path

def load_data(passes_path: str = 'passing.csv', report_path: str = 'reporte_mediocampo.csv') -> tuple:
    """Carga los datos de pases y el reporte de mediocampo desde CSV."""
    # Usar Path para mayor robustez, asumiendo ejecución desde la raíz o configurando paths relativos
    base_path = Path.cwd()
    p_path = base_path / passes_path
    r_path = base_path / report_path
    
    if not p_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {p_path}")
        
    df = pd.read_csv(p_path)
    
    if r_path.exists():
        report = pd.read_csv(r_path)
    else:
        report = pd.DataFrame() # Return empty if report doesn't exist yet
        
    return df, report

def clean_passes(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia el DataFrame de pases."""
    df = df.copy()
    # Remover columnas completamente vacías
    df.dropna(axis=1, how='all', inplace=True)
    # Reemplazar cadenas vacías por NaN (usando forward fill para compatibilidad o pd.NA)
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    
    # Intentar convertir columnas numéricas conocidas
    numeric_cols = ['90s', 'Cmp', 'Att', 'TotDist', 'PrgDist', 'Ast', 'xA', 'KP', '1/3', 'PPA', 'CrsPA', 'Prog']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df
