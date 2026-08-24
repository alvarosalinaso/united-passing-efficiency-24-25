# Complex Network Analysis of Midfield Passing Efficiency: Manchester United 2024-25

[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Plotly.js](https://img.shields.io/badge/Plotly.js-3.x-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/javascript/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.x-8A2BE2)](https://networkx.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

This repository applies graph-theoretic methods to dissect Manchester United's midfield passing structure during the 2024-25 Premier League campaign. We construct weighted directed graphs via NetworkX, compute centrality indices, and benchmark performance against league peers and tier-separated opposition.

---

## 1. Preguntas de Investigacion e Hipotesis

We frame the analysis around three research questions:

1. **Broker Identification.** Which midfielders function as structural brokers in United's passing network, as measured by betweenness centrality, and how does their removal degrade network connectivity?
2. **Expected Threat Distribution.** How is xT (expected threat) generated across the midfield unit, and does the player with the highest xT contribution also occupy the most central network position?
3. **Performance Differential by Opposition Tier.** Does United's midfield passing volume, verticality, and xT output exhibit statistically meaningful drops against Top 6 opposition relative to the Rest of the Premier League?

**Hypothesis.** We posit that United's passing network exhibits a single dominant broker (high betweenness, moderate degree) rather than a distributed hub structure, and that this dependency concentrates creative risk in a narrow passing corridor.

---

## 2. Pipeline Metodologico y Arquitectura de Datos

### 2.1 Data Layer

| Source | Description |
|--------|-------------|
| `passing.csv` | Raw event-level passing data per player |
| `reporte_mediocampo.csv` | Filtered midfield subset with computed metrics |

The ETL pipeline (`data.py`) ingests, validates, and normalizes the raw CSVs, producing a structured DataFrame with per-player aggregates: total passes, progressive passes, pass accuracy, verticality index, and cumulative xT.

### 2.2 Graph Construction

We model the midfield as a **weighted directed graph** G = (V, E) using NetworkX:

- **Vertices (V):** Each unique player in the filtered midfield dataset.
- **Edges (E):** Directed passing links between players. Edge weight corresponds to pass volume between each pair.
- **Self-loops removed.** Multi-edges collapsed into single weighted edges.

```
G = nx.DiGraph()
for _, row in passes.iterrows():
    G.add_edge(row["passer"], row["recipient"], weight=row["volume"])
```

### 2.3 Centrality Metrics

We compute the following NetworkX centrality indices on G:

| Metric | Interpretation |
|--------|---------------|
| **Betweenness Centrality** | Proportion of shortest paths passing through a node; identifies brokers and gatekeepers of passing flow. |
| **Degree Centrality** | Fraction of nodes directly connected; measures raw connectivity regardless of flow direction. |
| **In-Degree** | Receiving volume; proxies for how often a player is targeted by teammates. |
| **Out-Degree** | Distribution volume; proxies for how often a player initiates passes. |
| **Weighted Degree** | Sum of incident edge weights; captures total passing throughput. |

All metrics are normalized by (n-1)(n-2) for betweenness and by (n-1) for degree, where n = |V|.

---

## 3. Hallazgos Clave y Business/Domain Insights

### 3.1 Broker Identification

Bruno Fernandes consistently ranks as the dominant broker in United's network, with betweenness centrality values approximately 2-3x higher than the next most central midfielder. This confirms our hypothesis: United's creative output concentrates in a single structural bottleneck. When Bruno is absent or marked out of the game, the network's global efficiency (measured as harmonic centrality) degrades substantially.

### 3.2 Passing Volume vs Opposition Tier

Against Top 6 opposition, we observe measurable drops across all key dimensions:

| Metric | vs Rest PL | vs Top 6 | Delta |
|--------|-----------|----------|-------|
| Total Passes (midfield) | ~420 | ~340 | -19% |
| Progressive Passes | ~85 | ~58 | -32% |
| xT Generated | ~1.8 | ~1.2 | -33% |
| Verticality Index | ~0.42 | ~0.36 | -14% |

The steepest declines appear in progressive passing and xT, suggesting that elite opposition effectively compresses United's midfield into a conservative, lateral passing pattern.

### 3.3 xT Distribution

xT production is heavily skewed. The top 2-3 midfield contributors account for over 60% of cumulative xT, reinforcing the broker-dependency finding. Lower-centrality players tend to accumulate xT through safe lateral distributions rather than line-breaking passes.

---

## 4. Dashboard y Visualizaciones Interactivas

The analysis is surfaced through four interactive views, integrated into the portfolio deployment:

### 4.1 Passing Network Graph (Flourish)

An interactive node-edge visualization where node size encodes weighted degree and edge thickness encodes pass volume. Betweenness centrality is mapped to node color (sequential palette). Filters allow isolation by opponent tier.

<!-- Flourish embed placeholder: replace src URL with production Flourish public URL -->
<iframe src="https://flo.uri.sh/visualisation/XXXXXXX/embed" title="United Passing Network" width="100%" height="520"></iframe>

### 4.2 Correlation Matrix (Observable)

A cross-metric correlation heatmap computed in Observable, displaying pairwise Pearson correlations among xT, progressive passes, pass accuracy, verticality, betweenness centrality, and degree centrality.

<!-- Observable embed placeholder: replace with production Observable notebook URL -->
<iframe src="https://observablehq.com/embed/@XXXXXXX?cells=chart" width="100%" height="520"></iframe>

### 4.3 PL Benchmark (Datawrapper)

A horizontal bar chart ranking United against 9 Premier League peers on possession, pass accuracy, progressive passes, and xT. Built in Datawrapper for publication-quality static rendering.

<!-- Datawrapper embed placeholder: replace with production Datawrapper chart ID -->
<div class="datawrapper-chart"><iframe src="https://datawrapper.de/XXXXXXX" title="PL Benchmark" width="100%" height="520" frameborder="0"></iframe></div>

### 4.4 Tier Comparison (Datawrapper)

A grouped bar chart contrasting United's midfield metrics against Top 6 versus Rest of PL, sourced from the same underlying data pipeline.

<!-- Datawrapper embed placeholder: replace with production Datawrapper chart ID -->
<div class="datawrapper-chart"><iframe src="https://datawrapper.de/XXXXXXX" title="Tier Comparison" width="100%" height="520" frameborder="0"></iframe></div>

Live deployment: **https://alvarosalinaso.github.io/portfolio-web/** (Tab: "Red de Pases United")

---

## 5. Reproducibilidad y Entorno Tecnico

### 5.1 Environment

| Component | Specification |
|-----------|--------------|
| Python | 3.9 - 3.13 (CI matrix) |
| Package Manager | pip |
| Linter / Formatter | Ruff |
| Test Framework | Pytest + Pytest-cov |
| CI/CD | GitHub Actions |

### 5.2 Setup and Execution

```bash
git clone https://github.com/alvarosalinaso/united-passing-efficiency-24-25.git
cd united-passing-efficiency-24-25
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

For development (linters, tests, coverage):

```bash
pip install -e ".[dev]"
```

### 5.3 Data Pipeline

```bash
python src/united_passing/export_visualizations.py
```

Genera CSVs optimizados para Datawrapper, Flourish y Observable en `data/export/`, mas un archivo `embed_snippets.md` con snippets HTML responsivos listos para incrustar.

### 5.4 Quality Assurance

```bash
pytest                          # Run test suite
pytest --cov=united_passing     # Coverage report
ruff check .                    # Lint
ruff format --check .           # Format verification
```

### 5.5 Project Structure

```
united-passing-efficiency-24-25/
├── src/united_passing/
│   ├── data.py                    # ETL and validation
│   ├── analysis.py                # Efficiency metrics and filtering
│   ├── plot.py                    # Matplotlib visualizations
│   └── export_visualizations.py   # Multi-platform CSV export (Datawrapper/Flourish/Observable)
├── data/export/
│   ├── dw_benchmark_passing.csv   # Datawrapper benchmark data
│   ├── flourish_network_pases.csv # Flourish network graph data
│   ├── observable_centralidad.csv # Observable centrality data
│   └── embed_snippets.md          # Responsive HTML embed snippets
├── tests/
├── .github/workflows/ci.yml       # CI pipeline (lint + matrix + coverage)
├── passing.csv
├── reporte_mediocampo.csv
├── pyproject.toml
└── requirements.txt
```

---

## Licencia

Distributed under the [MIT License](LICENSE). Copyright 2026 Alvaro Salinas.
