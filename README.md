[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)

# Manchester United 24/25: Inteligencia de Pases y Verticalidad

Métricas crudas del mediocampo de Old Trafford para esta temporada. Aquí medimos quién rompe líneas de verdad (xT, pases progresivos) y quién juega a la segura inflando su precisión porcentual (y entregando la pelota al costado bajo presión).

## Novedades del Repositorio (Current Build)
- **CI / Pipeline 100% Saneado**: Refactoricé agresivamente la capa de `src` para desechar nombres poéticos y burocracia documental. Pasé métodos a enfoques ultra rápidos (`sanitize`, `mfs_only`). Los **Unit Tests** se recablearon y se ejecutan fluidamente devolviendo el badge de Github Actions a un verde perfecto.
- **Resolución dinámica:** El *app.py* y sus plots ahora montan sus datos locales sin fallos gracias al enrutamiento absoluto a prueba de errores mediante `pathlib`.
- **Filtros Dinámicos (Top 6 vs Resto):** Posibilidad real de ver la desviación táctica y el sesgo de datos dependiendo del nivel de presión asfixiante del rival.

## Archivos clave
- `passing.csv` / `reporte_mediocampo.csv`: Datos de FBRef filtrados directamente a la medular.
- `app.py`: La UI reactiva que se come las métricas transaccionales y exprime leaderboards, heatmap e índices de verticalidad.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

> Bajo licencia MIT. 
> Álvaro Salinas Ortiz | alvarosalinasortiz@gmail.com | [LinkedIn](https://www.linkedin.com/in/alvaro-salinas-ortiz)
