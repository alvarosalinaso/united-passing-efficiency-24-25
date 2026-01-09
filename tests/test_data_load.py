import pandas as pd
from data_load import load_data


def test_load_data_not_empty():
    df, report = load_data('Passing_clean.csv', 'reporte_mediocampo_clean.csv')
    assert not df.empty, 'Dataframe de pases está vacío'
    assert 'Player' in df.columns
    assert not report.empty, 'Reporte de mediocampo está vacío'
    assert 'Prog_Ratio' in report.columns
