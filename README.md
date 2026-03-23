[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)

# Manchester United 24/25: Inteligencia de Pases y Verticalidad

Métricas crudas del mediocampo de Old Trafford para esta temporada. Aquí medimos quién rompe líneas de verdad (Peligro Esperado, pases progresivos) y quién juega a lo seguro inflando su precisión porcentual (y entregando la pelota al costado bajo presión).

## Novedades del Repositorio
- **Integración Continua Saneada**: Refactoricé agresivamente la capa de código para desechar nombres poéticos y burocracia documental. Pasé los métodos a enfoques ultra rápidos. Las pruebas unitarias se configuraron de nuevo y se ejecutan fluidamente devolviendo la medalla de Github a un verde perfecto.
- **Resolución dinámica:** La aplicación central y sus gráficos ahora montan sus datos locales sin fallos gracias al enrutamiento absoluto a prueba de errores.
- **Filtros Dinámicos (Mejores 6 contra el Resto):** Posibilidad real de ver la desviación táctica y el sesgo de datos dependiendo del nivel de presión asfixiante del rival.

## Archivos clave
- `passing.csv` / `reporte_mediocampo.csv`: Datos tácticos filtrados directamente al mediocampo.
- `app.py`: La interfaz de usuario reactiva que consume las métricas transaccionales y exprime tableros de posiciones, mapas de calor e índices de verticalidad.

## Configuración Inicial

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

> Bajo licencia MIT. 
> Álvaro Salinas Ortiz | alvarosalinasortiz@gmail.com | [LinkedIn](https://www.linkedin.com/in/alvaro-salinas-ortiz)
