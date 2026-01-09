"""Carga los CSV del proyecto y muestra un resumen inicial.
Uso: python data_load.py
"""
import pandas as pd

def load_data(passes_path='passing.csv', report_path='reporte_mediocampo.csv'):
    df = pd.read_csv(passes_path)
    report = pd.read_csv(report_path)
    return df, report

if __name__ == '__main__':
    df, report = load_data()
    print('Pases: rows={}, cols={}'.format(*df.shape))
    print(df.head())
    print('\nReporte mediocampo: rows={}, cols={}'.format(*report.shape))
    print(report.head())
