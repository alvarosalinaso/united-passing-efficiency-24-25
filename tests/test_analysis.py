"""Smoke tests for united-passing-efficiency-24-25."""


def test_imports():
    from src.ab_testing import run_ab_testing
    from src.clustering_analysis import run_clustering
    from src.forecasting import run_forecasting
    from src.generate_tables import generate
    from src.graph_analysis import run_graph_analysis
    from src.similarity_analysis import run_similarity
    from src.statistical_tests import run_statistical_tests

    assert callable(run_clustering)
    assert callable(run_graph_analysis)
    assert callable(run_forecasting)
    assert callable(run_similarity)
    assert callable(run_ab_testing)
    assert callable(run_statistical_tests)
    assert callable(generate)
