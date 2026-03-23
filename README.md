[![Integración Continua](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)

# Manchester United 24/25: Inteligencia de Pases

Métricas estadísticas del mediocampo de Old Trafford para esta temporada. Aquí medimos quién rompe líneas de presión (Peligro Esperado, pases progresivos) y quién juega a lo seguro inflando su precisión porcentual mediante pases laterales o defensivos.

## Funcionalidades Principales
- **Integración Continua Saneada**: Refactorización profunda de todas las funciones para trabajar con enfoques rápidos y concisos. Las pruebas unitarias actúan como red de seguridad y validación automática del repositorio en la nube.
- **Resolución Binaria**: La aplicación central y sus gráficos acceden a la información sin errores en el manejo transversal de rutas de archivos de lectura absoluta.
- **Filtros Dinámicos**: Posibilidad de ver la desviación táctica y el sesgo de la información dependiendo de si se enfrenta un equipo de alta presión o un rival de corte inferior.

## Archivos Clave
- `passing.csv` / `reporte_mediocampo.csv`: Datos tácticos procesados y filtrados.
- `app.py`: La interfaz de usuario reactiva que consume las métricas y dibuja los tableros de posiciones, mapas de calor e índices de verticalidad en tiempo real.

## Configuración Inicial

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

> Álvaro Salinas Ortiz | alvarosalinasortiz@gmail.com | [LinkedIn](https://www.linkedin.com/in/alvaro-salinas-ortiz)
