"""
Orchestrador principal — United Passing Efficiency 2024-25.
Ejecuta todo el pipeline de analisis.
"""

from ab_testing import run_ab_testing
from clustering_analysis import run_clustering
from forecasting import run_forecasting
from generate_tables import generate as generate_exec_tables
from graph_analysis import run_graph_analysis
from similarity_analysis import run_similarity
from statistical_tests import run_statistical_tests


def main():
    print("=" * 60)
    print("ANALISIS DE EFICIENCIA DE PASES — MAN UNITED 2024-25")
    print("=" * 60)

    print("\n[1/7] Clustering de jugadores...")
    run_clustering()

    print("\n[2/7] Analisis de grafos de pases...")
    run_graph_analysis()

    print("\n[3/7] Forecasting de eficiencia...")
    run_forecasting()

    print("\n[4/7] Analisis de similaridad...")
    run_similarity()

    print("\n[5/7] A/B Testing...")
    run_ab_testing()

    print("\n[6/7] Tests estadisticos...")
    run_statistical_tests()

    print("\n[7/7] Generando tablas ejecutivas...")
    generate_exec_tables()

    print("\n" + "=" * 60)
    print("Pipeline completo.")


if __name__ == "__main__":
    main()
