# Passing Efficiency — Manchester United 2024-25

[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Dashboard táctico que analiza la eficiencia de pases del mediocampo del Manchester United (temporada 2024-2025). Incluye ranking de jugadores, mapas de calor por zona del campo, redes de pases basadas en grafos y evolución temporal de métricas clave.

## Dashboard en Vivo

👉 **[united-passing-efficiency-24-25.streamlit.app](https://united-passing-efficiency-24-25.streamlit.app)**

## Stack

| Capa | Tecnología |
|------|-----------|
| **Lenguaje** | Python 3.8+ |
| **Data** | Pandas, NumPy |
| **Visualización** | Streamlit, Plotly, Matplotlib |
| **Análisis** | SciPy (métricas de centralidad en grafos de pases) |
| **Testing** | Pytest |
| **CI/CD** | GitHub Actions |
| **Licencia** | MIT |

## Estructura

```
united-passing-efficiency-24-25/
├── src/united_passing/     # Paquete principal
│   ├── data.py             # Carga y validación
│   ├── analysis.py         # Métricas tácticas
│   └── plot.py             # Visualizaciones
├── tests/                  # Tests unitarios
├── .github/workflows/      # CI pipeline
├── app.py                  # Dashboard Streamlit
├── passing.csv             # Datos de pases
├── reporte_mediocampo.csv  # Reporte filtrado mediocampo
├── pyproject.toml          # Configuración
└── requirements.txt        # Dependencias
```

## Inicio Rápido

```bash
pip install -r requirements.txt
streamlit run app.py
```

```bash
pytest                      # Tests
```

## Contacto

**Álvaro Salinas Ortiz** — [LinkedIn](https://linkedin.com/in/alvaro-salinas-ortiz) · 
