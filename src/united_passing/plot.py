"""Módulo para visualización de datos."""
import matplotlib.pyplot as plt
import pandas as pd
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

def plot_top_passers(df: pd.DataFrame, metric: str = 'Cmp', top_n: int = 10, out_path: str = 'grafico_pases_united.png'):
    """Genera un gráfico de barras de los top N jugadores según una métrica."""
    if metric not in df.columns:
        raise KeyError(f'La columna {metric} no existe en los datos.')
    
    # Ordenar y seleccionar top
    df_top = df.sort_values(metric, ascending=False).head(top_n)
    
    plt.figure(figsize=(10, 6))
    
    if HAS_SEABORN:
        sns.set_theme(style="whitegrid")
        sns.barplot(x=metric, y='Player', data=df_top, palette='viridis')
    else:
        # Fallback a matplotlib puro
        plt.barh(df_top['Player'][::-1], df_top[metric][::-1])
    
    plt.xlabel(metric)
    plt.title(f'Top {top_n} jugadores por {metric}')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path
