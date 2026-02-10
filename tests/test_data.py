"""Tests para el módulo de datos."""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from united_passing.data import load_data, clean_passes

def test_clean_passes():
    """Prueba la limpieza básica de datos."""
    data = {
        'Player': ['Bruno', 'Casemiro', ''],
        'Cmp': ['50', '40', ''],
        'EmptyCol': [None, None, None]
    }
    df = pd.DataFrame(data)
    cleaned = clean_passes(df)
    
    assert 'EmptyCol' not in cleaned.columns
    assert pd.isna(cleaned.iloc[2]['Player'])
    assert cleaned.iloc[0]['Cmp'] == 50
    assert cleaned.iloc[1]['Cmp'] == 40

@patch('united_passing.data.pd.read_csv')
@patch('united_passing.data.Path.exists')
def test_load_data(mock_exists, mock_read_csv):
    """Prueba la carga de datos con mocking."""
    mock_exists.return_value = True
    mock_df = pd.DataFrame({'Player': ['Bruno']})
    mock_read_csv.return_value = mock_df
    
    df, report = load_data()
    
    assert not df.empty
    assert 'Player' in df.columns
