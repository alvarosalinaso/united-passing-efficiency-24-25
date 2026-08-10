# Passing Efficiency — Manchester United 2024-25

[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Dashboard táctico que analiza la eficiencia de pases del mediocampo del Manchester United (temporada 2024-2025). Incluye ranking de jugadores, mapas de calor por zona del campo, redes de pases basadas en grafos y evolución temporal de métricas clave.

## Tabla de contenidos

- [Dashboard en Vivo](#dashboard-en-vivo)
- [Stack](#stack)
- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Inicio Rápido](#inicio-rápido)
- [Testing](#testing)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Dashboard en Vivo

👉 **[united-passing-efficiency-24-25.streamlit.app](https://united-passing-efficiency-24-25.streamlit.app)**

## Stack

| Capa | Tecnología |
|------|-----------|
| **Lenguaje** | Python 3.9+ |
| **Data** | Pandas, NumPy |
| **Visualización** | Streamlit, Plotly, Matplotlib |
| **Análisis** | SciPy (métricas de centralidad en grafos de pases) |
| **Testing** | Pytest, Pytest-cov |
| **Lint & Format** | Ruff |
| **CI/CD** | GitHub Actions (matrix 3.9–3.13) |
| **Licencia** | MIT |

## Arquitectura

```
┌─────────────┐   ┌──────────────┐   ┌──────────────┐
│  data.py    │──▶│ analysis.py  │──▶│   plot.py    │
│ (carga/     │   │ (métricas)   │   │ (visualiza)  │
│  limpieza)  │   └──────────────┘   └──────────────┘
└─────────────┘                                  │
      │                                         ▼
      └───────────▶ app.py (Streamlit) ──▶ Dashboard
```

- **data.py** — carga, resolución de rutas y limpieza vectorizada (sin `apply` en bucles).
- **analysis.py** — métricas tácticas y top-N por ratio progresivo.
- **plot.py** — visualizaciones Matplotlib/Seaborn reutilizables.
- **app.py** — capa de presentación (Streamlit) que orquesta los módulos.

## Estructura

```
united-passing-efficiency-24-25/
├── src/united_passing/     # Paquete principal
│   ├── data.py             # Carga y validación
│   ├── analysis.py         # Métricas tácticas
│   └── plot.py             # Visualizaciones
├── tests/                  # Tests unitarios e integración
├── .github/workflows/      # CI pipeline (lint + matrix de tests + coverage)
├── app.py                  # Dashboard Streamlit
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

## Inicio Rápido

```bash
streamlit run app.py
```

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
