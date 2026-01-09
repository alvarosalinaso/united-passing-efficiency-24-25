"""Analiza el reporte de mediocampo y exporta un CSV con los mejores.

Genera un CSV resumen con los top N jugadores ordenados por `Prog_Ratio`.
"""
import pandas as pd


def top_by_prog_ratio(report_path='reporte_mediocampo.csv', out_path='top_mediocampo.csv', top_n=10):
    df = pd.read_csv(report_path)
    if 'Prog_Ratio' in df.columns:
        df_sorted = df.sort_values('Prog_Ratio', ascending=False)
        df_top = df_sorted.head(top_n)
        df_top.to_csv(out_path, index=False)
        return df_top
    else:
        raise KeyError('La columna Prog_Ratio no existe en {}'.format(report_path))


if __name__ == '__main__':
    top = top_by_prog_ratio()
    print('Top de mediocampo por Prog_Ratio:')
    print(top)
