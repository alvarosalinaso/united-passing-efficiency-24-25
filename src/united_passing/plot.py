"""Módulo de visualización de pases del Manchester United."""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

try:
    import seaborn as sns
    sns.set_theme(style="whitegrid", palette="muted")
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

_RED = "#c0392b"
_DARK = "#2c3e50"


def _guardar(fig: plt.Figure, out_path: str) -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✅ Guardado: {out_path}")
    return out_path


def plot_top_passers(
    df: pd.DataFrame,
    metric: str = "Cmp",
    top_n: int = 10,
    out_path: str = "grafico_pases_united.png",
) -> str:
    """
    Gráfico de barras horizontales con los top N jugadores según una métrica.

    Args:
        df: DataFrame limpio de pases.
        metric: Columna a usar como métrica (ej. 'Cmp', 'Prog', 'xA').
        top_n: Número de jugadores a mostrar.
        out_path: Ruta de salida del gráfico.

    Returns:
        Ruta donde se guardó el gráfico.
    """
    if metric not in df.columns:
        raise KeyError(f"La columna '{metric}' no existe en los datos.")
    if "Player" not in df.columns:
        raise KeyError("El DataFrame no tiene columna 'Player'.")

    df_top = df.dropna(subset=[metric]).sort_values(metric, ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))

    colores = [_RED if i == 0 else _DARK for i in range(len(df_top))]

    if HAS_SEABORN:
        sns.barplot(x=metric, y="Player", data=df_top, palette=colores, ax=ax)
    else:
        ax.barh(df_top["Player"][::-1], df_top[metric][::-1], color=colores[::-1])

    ax.set_xlabel(metric, fontsize=11)
    ax.set_ylabel("")
    ax.set_title(f"Top {top_n} jugadores — {metric} | Man Utd 2024/25", fontweight="bold")
    ax.axvline(df_top[metric].mean(), color="gray", linestyle="--", linewidth=0.8,
               label=f"Media: {df_top[metric].mean():.1f}")
    ax.legend(fontsize=8)

    return _guardar(fig, out_path)


def plot_prog_ratio_scatter(
    df: pd.DataFrame,
    out_path: str = "analisis_mediocampo_united.png",
) -> str:
    """
    Scatter: Pases completados (volumen) vs Prog_Ratio (eficiencia progresiva).

    Args:
        df: DataFrame con columnas Cmp y Prog_Ratio.
        out_path: Ruta de salida.

    Returns:
        Ruta donde se guardó el gráfico.
    """
    if "Prog_Ratio" not in df.columns or "Cmp" not in df.columns:
        raise KeyError("Se necesitan columnas 'Prog_Ratio' y 'Cmp'.")

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.scatter(df["Cmp"], df["Prog_Ratio"], color=_RED, s=100, edgecolors=_DARK,
               linewidth=0.6, zorder=3)

    if "Player" in df.columns:
        for _, row in df.iterrows():
            ax.annotate(row["Player"], xy=(row["Cmp"], row["Prog_Ratio"]),
                        xytext=(4, 3), textcoords="offset points", fontsize=8)

    ax.axhline(df["Prog_Ratio"].mean(), color="gray", linestyle="--", linewidth=0.8,
               label=f"Media Prog_Ratio: {df['Prog_Ratio'].mean():.3f}")
    ax.axvline(df["Cmp"].mean(), color="gray", linestyle=":", linewidth=0.8,
               label=f"Media Cmp: {df['Cmp'].mean():.0f}")

    ax.set_xlabel("Pases Completados (Cmp)", fontsize=11)
    ax.set_ylabel("Ratio de Pases Progresivos (Prog/Cmp)", fontsize=11)
    ax.set_title("Volumen vs Eficiencia Progresiva — Mediocampistas Man Utd", fontweight="bold")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    return _guardar(fig, out_path)
