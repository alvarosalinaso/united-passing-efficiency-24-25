[![Integración Continua](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml)

# Manchester United 24/25: Inteligencia de Pases

🚀 **[Ver Panel Interactivo en Vivo](https://united-passing-efficiency-24-25-csjdeu5gajataagkqbydyu.streamlit.app)**

Dashboard estadístico para deconstruir la influencia de la sala de máquinas de Old Trafford. Este proyecto evalúa directamente la creación de Peligro Esperado en el mediocampo, identificando quién asume riesgos tácticos rompiendo líneas y quién preserva una falsa alta efectividad recurriendo a pases perimetrales.

---

## Funciones Principales y Diseño

- **Filtros Tácticos Activos:** Posibilidad de testear el rendimiento bajo stress. Te permite alterar el resultado visual dependiendo de si el equipo está confrontando líneas altas de presión o si está en un entorno táctico pasivo.
- **Precisión bajo CI:** Diseño purgado con metodologías de CI completas y Unit Testing modularizado.
- **Rutas a Prueba de Fallos:** Implementaciones OSO que aíslan el proyecto de quiebres dependientes de jerarquías de directorios externas.

---

## Módulos y Datasets

- `passing.csv` / `reporte_mediocampo.csv`: Datos depurados por el backend con los cálculos de verticalidad.
- `app.py`: Punto de entrada interactivo para Streamlit. Traduce las tablas en mapas de posicionamiento y correlaciones.

---

## Ejecución Base

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

> **Álvaro Salinas Ortiz** | Análisis de Datos y Estrategia Numérica | [LinkedIn](https://www.linkedin.com/in/alvaro-salinas-ortiz)
