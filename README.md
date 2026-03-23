[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)

# Manchester United 24/25: Inteligencia de Pases

Métricas crudas del mediocampo de Old Trafford para esta temporada. Aquí medimos quién rompe líneas de verdad (xT, pases progresivos) y quién juega a la segura inflando su precisión.

## Archivos clave
- `passing.csv`: Stats puras de FBRef / StatsBomb para toda la plantilla.
- `reporte_mediocampo.csv`: Foco quirúrgico en jugadores de la medular.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Para usar el core analítico rápido:
```python
from data_load import load_data
df, df_m = load_data('passing.csv', 'reporte_mediocampo.csv')
```

## Disclaimer
Scripts purgados y unificados. La pipeline limpia tira directamente los datasets para que el dash en Streamlit los escupa.

> Bajo licencia MIT. 
> Álvaro Salinas Ortiz | alvarosalinasortiz@gmail.com
