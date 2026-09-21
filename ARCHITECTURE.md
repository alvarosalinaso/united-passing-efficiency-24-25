# Arquitectura — united-passing-efficiency-24-25

## Visión general
Análisis de eficiencia de pases del Manchester United (temporada 2024-25). Procesamiento de datos de pases, métricas de progresión, clustering, similarity analysis, graph analysis, A/B testing, forecasting.

## Componentes principales

### Datos
- `passing.csv` — Datos crudos de pases (Player, Pos, Cmp, Att, Prog, xA, etc.)
- `reporte_mediocampo.csv` — Reporte generado
- `analisis_mediocampo_united.png` — Visualización

### Código (src/united_passing/)
- `data.py`:
  - `load_data()`: passing.csv → df + reporte opcional
  - `clean_passes()`: limpieza (tipos, NaN, columnas vacías)
  - `_resolver_ruta()`, `_prog_ratio()`
- `analysis.py`:
  - `build_midfield_report()`: filtra MF, añade Prog_Ratio, ordena
  - `filter_midfielders()`, `top_by_prog_ratio()`, `resumen_estadisticas()`
- `clustering_analysis.py` — run_clustering
- `forecasting.py` — run_forecasting
- `similarity_analysis.py` — run_similarity
- `graph_analysis.py` — run_graph_analysis
- `ab_testing.py` — run_ab_testing
- `statistical_tests.py` — run_statistical_tests
- `generate_tables.py` — generate
- `generate_report.py` — generate_report

## Flujo de datos
```
passing.csv → data.load_data → df
df → data.clean_passes → clean_df
clean_df → analysis.build_midfield_report → midfield_report
midfield_report → clustering/forecasting/similarity/graph/ab_testing/statistical_tests → outputs
```

## Despliegue
- Docker: `Dockerfile` (Python 3.11)
- No es dashboard web — genera PNGs, CSVs, reportes

## Tests
- `tests/test_data.py` — load_data, clean_passes, _resolver_ruta, _prog_ratio, build_midfield_report, analysis functions
- `tests/test_plot.py` — Tests de visualización
- `tests/test_analysis.py` — Smoke tests
- CI: pytest + coverage + ruff (Python 3.9, 3.11, 3.12, 3.13)
- pyproject.toml con optional-dependencies dev

## Estructura de paquete
- `src/united_passing/` — Paquete instalable (`pip install -e .`)
- `pyproject.toml` — Configuración completa (build, ruff, pytest)