# United Passing Network — Manchester United 2024-25

[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Plotly.js](https://img.shields.io/badge/Plotly.js-3.x-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/javascript/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.x-8A2BE2)](https://networkx.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Dashboard táctico que analiza la eficiencia de pases del mediocampo del Manchester United (temporada 2024-2025) usando **Complex Network Analysis**. Incluye: redes de pases interactivas (betweenness centrality), comparativas individuales multi-métrica, benchmark vs Premier League, y análisis de rendimiento contra Top 6 vs Resto PL.

## Tabla de contenidos

- [Dashboard Integrado](#dashboard-integrado)
- [Stack](#stack)
- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Inicio Rápido](#inicio-rápido)
- [Testing](#testing)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Dashboard Integrado

👉 **Integrado en [Portfolio Web](https://alvarosalinaso.github.io/portfolio-web/)** → Tab **"🕸️ Red de Pases United"**  
4 vistas interactivas:
- **🗺️ Red de Pases** — Grafo interactivo con betweenness centrality, filtro por rival (Top 6 / Resto PL)
- **📐 Comparativa Individual** — Scatter plot multi-eje (xT, pases progresivos, precisión, verticalidad)
- **⚖️ Benchmark vs Premier League** — Ranking United vs 9 equipos PL en posesión, precisión, pases prog., xT
- **🔄 Resto PL vs Top 6** — Comparativa de métricas según nivel de rival

Desplegado en GitHub Pages (estático, sin backend Python).

## Stack

| Capa | Tecnología |
|------|-----------|
| **Lenguaje** | Python 3.9+ (ETL/Análisis) · JavaScript/Plotly.js (Frontend) |
| **Data** | Pandas, NumPy |
| **Análisis de Redes** | NetworkX (betweenness, degree centrality) |
| **Visualización** | **Plotly.js** (integrado en Portfolio Web), Matplotlib |
| **Testing** | Pytest, Pytest-cov |
| **Lint & Format** | Ruff |
| **CI/CD** | GitHub Actions (matrix 3.9–3.13) |
| **Licencia** | MIT |

## Arquitectura

```
┌─────────────┐   ┌──────────────────┐   ┌─────────────────┐
│  data.py    │──▶│ network_analysis │──▶│  json_export    │
│ (pases/     │   │ (NetworkX:       │   │ (squad, passes, │
│  métricas)  │   │  betweenness,    │   │  stats, PL)     │
└─────────────┘   │   centrality)    │   └─────────────────┘
      │           └──────────────────┘            │
      │                                           ▼
      └────────────────▶ portfolio-web/public/data/ ──▶ Plotly.js charts
                                                        (Vanilla JS modules)
```

## Estructura

```
united-passing-efficiency-24-25/
├── src/united_passing/     # Paquete principal
│   ├── data.py             # Carga y validación
│   ├── network_analysis.py # Métricas de grafos (NetworkX)
│   └── export_json.py      # Exporta datos a portfolio-web
├── tests/                  # Tests unitarios e integración
├── .github/workflows/      # CI pipeline (lint + matrix de tests + coverage)
├── passing.csv             # Datos de pases
├── reporte_mediocampo.csv  # Reporte filtrado mediocampo
├── pyproject.toml          # Configuración (build, ruff, pytest, coverage)
└── requirements.txt        # Dependencias en runtime
```

## Instalación

```bash
git clone https://github.com/alvarosalinaso/united-passing-efficiency-24-25.git
cd united-passing-efficiency-24-25
python -m venv .venv
# Windows: .venv\Scripts\activate   |  Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Para desarrollo (incluye linters y tests):

```bash
pip install -e ".[dev]"
```

## Generar datos para Portfolio Web

```bash
python src/united_passing/export_json.py
```

## Ver Dashboard Interactivo

**[https://alvarosalinaso.github.io/portfolio-web/](https://alvarosalinaso.github.io/portfolio-web/)** → Tab **"🕸️ Red de Pases United"**

## Testing

```bash
pytest                      # Tests + cobertura
ruff check .                # Lint
ruff format --check .       # Verificación de formato
```

## Contribución

Revisa [CONTRIBUTING.md](CONTRIBUTING.md) para convenciones de commits, estilo de código y flujo de PRs.

## Licencia

Distribuido bajo la licencia [MIT](LICENSE). Copyright © 2026 Álvaro Salinas.