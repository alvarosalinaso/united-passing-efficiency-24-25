"""Tests para el módulo de datos de pases."""
import pytest
import pandas as pd
from unittest.mock import patch
from united_passing.data import clean_passes, build_midfield_report
from united_passing.analysis import top_by_prog_ratio, filter_midfielders, resumen_estadisticas


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def raw_df() -> pd.DataFrame:
    return pd.DataFrame({
        "Player":  ["Bruno Fernandes", "Casemiro", "Kobbie Mainoo", ""],
        "Pos":     ["MF", "MF", "MF", "DF"],
        "Cmp":     ["80", "60", "45", ""],
        "Att":     ["95", "72", "55", "30"],
        "Prog":    ["20", "10", "15", ""],
        "xA":      ["3.1", "0.8", "1.2", ""],
        "EmptyCol": [None, None, None, None],
    })


@pytest.fixture
def clean_df(raw_df) -> pd.DataFrame:
    return clean_passes(raw_df)


# ── Tests: clean_passes ───────────────────────────────────────────────────────

def test_clean_removes_empty_columns(clean_df):
    assert "EmptyCol" not in clean_df.columns


def test_clean_converts_numerics(clean_df):
    assert clean_df["Cmp"].dtype in [float, "float64"]
    assert clean_df.loc[0, "Cmp"] == 80.0
    assert clean_df.loc[1, "Cmp"] == 60.0


def test_clean_empty_string_to_nan(clean_df):
    assert pd.isna(clean_df.loc[3, "Cmp"])


# ── Tests: build_midfield_report ──────────────────────────────────────────────

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


# ── Tests: analysis ───────────────────────────────────────────────────────────

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


# ── Tests: load_data (smoke) ──────────────────────────────────────────────────

def test_load_data_file_not_found():
    from united_passing.data import load_data
    with pytest.raises(FileNotFoundError):
        load_data(passes_path="no_existe.csv")
