Proyecto: Análisis de pases — Manchester United 2024-2025

Contenido:
- `Passing 2024-2025 Manchester United - Passing (1).csv`: datos de pases y estadísticas por jugador.
- `reporte_mediocampo.csv`: reporte filtrado y métricas específicas para mediocampistas.
- `analisis_mediocampo_united (1).png`, `grafico_pases_united (1).png`: visualizaciones generadas.

Objetivo:
Analizar la distribución y eficacia de pases del plantel del Manchester United (temporada 2024-2025), con un enfoque en mediocampistas.

Requisitos:
- Python 3.8+
- pandas
- matplotlib/seaborn (opcional para gráficos)

Instalación rápida:
1. Crear entorno virtual:

```
python -m venv .venv
.
```

2. Instalar dependencias:

```
pip install pandas matplotlib seaborn
```

Uso básico:
1. Cargar los CSV en pandas:

```python
import pandas as pd
df = pd.read_csv('Passing 2024-2025 Manchester United - Passing (1).csv')
report = pd.read_csv('reporte_mediocampo.csv')
```

2. Revisar columnas y limpiar valores faltantes según sea necesario.

Subir a GitHub:
1. Inicialice git y haga commit (pasos automatizables desde este repo).
2. Añada un remote y haga `git push` al repositorio remoto (necesito la URL o permisos para crear/pushear al repo).

Notas:
- He limpiado el formato de los CSV (eliminadas las marcas de bloque ```csv) para poder leerlos directamente con `pandas.read_csv`.
- Si quieres que cree el repositorio en tu cuenta y haga el push, proporciona la URL del repo o un token con permisos (recomiendo realizar el push desde tu máquina para mayor seguridad).
