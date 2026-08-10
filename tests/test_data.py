"""Tests del módulo de datos y carga de pases (unificado)."""

import pandas as pd
import pytest

from united_passing.analysis import filter_midfielders, resumen_estadisticas, top_by_prog_ratio
from united_passing.data import (
    _prog_ratio,
    _resolver_ruta,
    build_midfield_report,
    clean_passes,
    load_data,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def raw_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Player": ["Bruno Fernandes", "Casemiro", "Kobbie Mainoo", ""],
            "Pos": ["MF", "MF", "MF", "DF"],
            "Cmp": ["80", "60", "45", ""],
            "Att": ["95", "72", "55", "30"],
            "Prog": ["20", "10", "15", ""],
            "xA": ["3.1", "0.8", "1.2", ""],
            "EmptyCol": [None, None, None, None],
        }
    )


@pytest.fixture
def clean_df(raw_df) -> pd.DataFrame:
    return clean_passes(raw_df)


@pytest.fixture
def passing_csv(tmp_path) -> str:
    """Crea un `passing.csv` real en un directorio temporal."""
    path = tmp_path / "passing.csv"
    pd.DataFrame(
        {
            "Player": ["Bruno Fernandes", "Casemiro"],
            "Pos": ["MF", "MF"],
            "Cmp": ["82", "60"],
            "Att": ["96", "74"],
            "Prog": ["21", "11"],
        }
    ).to_csv(path, index=False)
    return str(path)


# ── Tests: _resolver_ruta ────────────────────────────────────────────────────


def test_resolver_ruta_devuelve_absoluta(tmp_path):
    archivo = tmp_path / "datos.csv"
    archivo.write_text("a,b\n1,2\n", encoding="utf-8")
    ruta = _resolver_ruta(str(archivo))
    assert ruta == archivo.resolve()
    assert ruta.is_absolute()


def test_resolver_ruta_inexistente_raise(tmp_path):
    with pytest.raises(FileNotFoundError):
        _resolver_ruta(str(tmp_path / "no_existe.csv"))


# ── Tests: load_data ─────────────────────────────────────────────────────────


def test_load_data_reads_passes(passing_csv):
    df, _ = load_data(passes_path=passing_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert {"Player", "Cmp", "Att"}.issubset(df.columns)


def test_load_data_returns_empty_report_when_missing(passing_csv, tmp_path):
    _, report = load_data(
        passes_path=passing_csv,
        report_path=str(tmp_path / "no_existe.csv"),
    )
    assert isinstance(report, pd.DataFrame)
    assert report.empty


def test_load_data_missing_passes_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(passes_path=str(tmp_path / "no_existe.csv"))


def test_load_data_reads_optional_report(passing_csv, tmp_path):
    report_path = tmp_path / "reporte.csv"
    pd.DataFrame({"Player": ["X"], "Prog_Ratio": [0.25]}).to_csv(report_path, index=False)
    _, report = load_data(passes_path=passing_csv, report_path=str(report_path))
    assert "Prog_Ratio" in report.columns


# ── Tests: _prog_ratio (edge cases) ──────────────────────────────────────────


def test_prog_ratio_values():
    df = pd.DataFrame({"Prog": [20.0, 10.0, 15.0], "Cmp": [80.0, 60.0, 45.0]})
    result = _prog_ratio(df).tolist()
    assert result == [0.25, round(10 / 60, 4), round(15 / 45, 4)]


def test_prog_ratio_zero_when_cmp_zero_or_nan():
    df = pd.DataFrame({"Prog": [10.0, 5.0], "Cmp": [0.0, pd.NA]})
    assert (_prog_ratio(df) == 0.0).all()


def test_prog_ratio_zero_when_cmp_non_numeric():
    df = pd.DataFrame({"Prog": [10.0], "Cmp": ["n/a"]})
    assert _prog_ratio(df).iloc[0] == 0.0


def test_prog_ratio_sin_columnas():
    df = pd.DataFrame({"Otra": [1, 2]})
    assert (_prog_ratio(df) == 0.0).all()


# ── Tests: clean_passes ──────────────────────────────────────────────────────


def test_clean_removes_empty_columns(clean_df):
    assert "EmptyCol" not in clean_df.columns


def test_clean_converts_numerics(clean_df):
    assert clean_df["Cmp"].dtype in [float, "float64"]
    assert clean_df.loc[0, "Cmp"] == 80.0
    assert clean_df.loc[1, "Cmp"] == 60.0


def test_clean_empty_string_to_nan(clean_df):
    assert pd.isna(clean_df.loc[3, "Cmp"])


def test_clean_passes_idempotente():
    raw_frame = pd.DataFrame(
        {
            "Player": ["A", "B"],
            "Cmp": ["10", ""],
            "Prog": [None, None],
            "Vacia": [None, None],
        }
    )
    limpio_1 = clean_passes(raw_frame)
    limpio_2 = clean_passes(limpio_1)
    assert limpio_1.equals(limpio_2)


# ── Tests: build_midfield_report ─────────────────────────────────────────────


def test_build_midfield_report_filters_mf(clean_df):
    report = build_midfield_report(clean_df)
    assert all(report["Pos"].str.contains("MF"))


def test_build_midfield_report_adds_prog_ratio(clean_df):
    report = build_midfield_report(clean_df)
    assert "Prog_Ratio" in report.columns


def test_build_midfield_report_sorted_desc(clean_df):
    report = build_midfield_report(clean_df)
    ratios = report["Prog_Ratio"].tolist()
    assert ratios == sorted(ratios, reverse=True)


# ── Tests: análisis ─────────────────────────────────────────────────────────


def test_top_by_prog_ratio_calculates_if_missing(clean_df):
    result = top_by_prog_ratio(clean_df, top_n=2)
    assert len(result) <= 2
    assert "Prog_Ratio" in result.columns


def test_top_by_prog_ratio_respects_top_n(clean_df):
    result = top_by_prog_ratio(clean_df, top_n=1)
    assert len(result) == 1


def test_filter_midfielders(clean_df):
    mf = filter_midfielders(clean_df)
    assert all(mf["Pos"].str.contains("MF"))


def test_filter_midfielders_no_pos_column():
    df = pd.DataFrame({"Player": ["A", "B"], "Cmp": [10, 20]})
    result = filter_midfielders(df)
    assert len(result) == 2


def test_resumen_estadisticas_cols(clean_df):
    res = resumen_estadisticas(clean_df)
    assert "Player" in res.columns
    assert "Cmp" in res.columns


# ── Tests: roundtrip end-to-end ──────────────────────────────────────────────


def test_load_clean_build_roundtrip(passing_csv):
    df, _ = load_data(passes_path=passing_csv)
    limpio = clean_passes(df)
    assert "Prog_Ratio" not in limpio.columns
    assert limpio["Cmp"].tolist() == [82.0, 60.0]
