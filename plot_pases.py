"""Genera gráficos simples de pases y guarda imágenes.
Requiere: matplotlib, seaborn (opcional)
"""
import pandas as pd
import matplotlib.pyplot as plt


def plot_top_passers(passes_path='Passing_clean.csv', out_path='grafico_pases_united.png', top_n=10):
    df = pd.read_csv(passes_path)
    if 'Cmp' in df.columns:
        top = df.sort_values('Cmp', ascending=False).head(top_n)
        plt.figure(figsize=(8,6))
        plt.barh(top['Player'][::-1], top['Cmp'][::-1])
        plt.xlabel('Pases completados')
        plt.title('Top {} jugadores por pases completados'.format(top_n))
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path
    else:
        raise KeyError('La columna Cmp no existe en {}'.format(passes_path))

if __name__ == '__main__':
    print('Generando gráfico...')
    print(plot_top_passers())
