"""Tests para el módulo de visualización (matplotlib, backend Agg)."""

import matplotlib

matplotlib.use("Agg")

import pandas as pd
import pytest

from united_passing.plot import plot_prog_ratio_scatter, plot_top_passers


@pytest.fixture
def df_pases() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Player": ["Bruno Fernandes", "Casemiro", "Kobbie Mainoo"],
            "Pos": ["MF", "MF", "MF"],
            "Cmp": [82, 60, 45],
            "Prog": [21, 11, 15],
            "Prog_Ratio": [0.2561, 0.1833, 0.3333],
        }
    )


def test_plot_top_passers_guarda_archivo(df_pases, tmp_path):
    out = str(tmp_path / "top.png")
    ruta = plot_top_passers(df_pases, metric="Cmp", top_n=2, out_path=out)
    assert ruta == out
    assert (tmp_path / "top.png").exists()
    assert (tmp_path / "top.png").stat().st_size > 0


def test_plot_top_passers_metrica_inexistente(df_pases, tmp_path):
    with pytest.raises(KeyError):
        plot_top_passers(df_pases, metric="no_existe", out_path=str(tmp_path / "x.png"))


def test_plot_top_passers_sin_columna_player(tmp_path):
    with pytest.raises(KeyError):
        plot_top_passers(pd.DataFrame({"Cmp": [1]}), out_path=str(tmp_path / "x.png"))


def test_plot_prog_ratio_scatter(df_pases, tmp_path):
    out = str(tmp_path / "scatter.png")
    ruta = plot_prog_ratio_scatter(df_pases, out_path=out)
    assert ruta == out
    assert (tmp_path / "scatter.png").exists()


def test_plot_prog_ratio_scatter_falta_columnas(df_pases, tmp_path):
    df_malo = df_pases.drop(columns=["Cmp"])
    with pytest.raises(KeyError):
        plot_prog_ratio_scatter(df_malo, out_path=str(tmp_path / "x.png"))
