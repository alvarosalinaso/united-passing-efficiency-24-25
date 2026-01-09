[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)

Proyecto: Análisis de pases — Manchester United 2024-2025

Descripción:
Repositorio con datos y scripts para analizar la eficiencia de pases del Manchester United (temporada 2024-2025). Contiene un CSV con estadísticas por jugador, un reporte filtrado para mediocampistas y scripts para limpieza, análisis y visualización.

Contenido principal:
- `passing.csv`: datos de pases y estadísticas por jugador (limpio).
- `reporte_mediocampo.csv`: reporte filtrado con métricas por jugador del mediocampo.
- `data_load.py`, `clean_data.py`, `analyze_mediocampo.py`, `plot_pases.py`: scripts de ayuda y análisis.
- `LICENSE`: licencia MIT.

Requisitos:
- Python 3.8+
- Instalar dependencias listadas en `requirements.txt`.

Instalación rápida:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Uso básico:
```python
import pandas as pd
from data_load import load_data
df, report = load_data('passing.csv', 'reporte_mediocampo.csv')
```

Notas:
- He unificado nombres de archivos y eliminado duplicados redundantes para facilitar el uso.
- CI está configurado para ejecutar pruebas si están presentes en el repositorio.

Licencia:
Este proyecto se publica bajo la licencia MIT. Consulta `LICENSE`.
