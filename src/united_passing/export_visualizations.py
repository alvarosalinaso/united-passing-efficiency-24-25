"""Exportación de datos para visualizaciones multi-plataforma.

Genera CSVs y snippets HTML para:
- Datawrapper (barras de métricas de pase)
- Flourish (diagrama de red de conexiones entre jugadores)
- Observable Plot (dispersión centralidad vs precisión)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_EXPORT_DIR = _PROJECT_ROOT / "data" / "export"


def _resolver_ruta(nombre: str) -> Path:
    """Resuelve la ruta de un archivo de datos.

    Prioriza: (1) rutas absolutas, (2) relativas al directorio actual,
    (3) relativas a la raíz del proyecto.

    Args:
        nombre: Nombre o ruta del archivo.

    Returns:
        Ruta absoluta resuelta.

    Raises:
        FileNotFoundError: si el archivo no existe en ningún candidato.
    """
    ruta = Path(nombre)
    if ruta.is_absolute():
        if not ruta.exists():
            raise FileNotFoundError(f"No se encontró '{nombre}'.")
        return ruta.resolve()

    candidatos = [ruta, Path.cwd() / ruta, _PROJECT_ROOT / ruta]
    for c in candidatos:
        if c.exists():
            return c.resolve()

    raise FileNotFoundError(f"No se encontró '{nombre}'. Colócalo en la raíz del proyecto.")

# Promedios de la Premier League 2024-25 (valores de referencia)
_PL_AVERAGES: dict[str, float] = {
    "Cmp%": 82.5,
    "PrgDist": 8500,
    "Ast": 3.5,
    "xA": 3.2,
    "KP": 35,
    "PPA": 25,
    "PrgP": 80,
}


def _ensure_export_dir() -> None:
    """Crea el directorio de exportación si no existe."""
    _EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def _load_passes() -> pd.DataFrame:
    """Carga y limpia los datos de pases."""
    df = pd.read_csv(_resolver_ruta("passing.csv"))
    df = df[df["Player"].notna() & (df["Player"] != "Total")].copy()

    numeric_cols = [
        "90s", "Cmp", "Att", "Cmp%", "TotDist", "PrgDist",
        "Ast", "xA", "KP", "1/3", "PPA", "CrsPA", "PrgP",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna(subset=["Player"]).reset_index(drop=True)


def _short_name(full_name: str) -> str:
    """Extrae el apellido para usar en conexiones de red."""
    parts = full_name.strip().split()
    return parts[-1] if parts else full_name


def export_benchmark_csv(df: pd.DataFrame) -> Path:
    """Exporta CSV para Datawrapper: métricas United vs promedio PL.

    Returns:
        Ruta del CSV generado.
    """
    metrics = ["Cmp%", "PrgDist", "Ast", "xA", "KP", "PPA", "PrgP"]
    present = [m for m in metrics if m in df.columns]

    united_avg = {}
    for m in present:
        values = pd.to_numeric(df[m], errors="coerce").dropna()
        united_avg[m] = round(values.mean(), 2) if len(values) > 0 else 0.0

    rows = []
    for metric in present:
        rows.append({
            "Metric": metric,
            "Manchester United": united_avg.get(metric, 0),
            "PL Average": _PL_AVERAGES.get(metric, 0),
            "Difference": round(
                united_avg.get(metric, 0) - _PL_AVERAGES.get(metric, 0), 2
            ),
        })

    out_df = pd.DataFrame(rows)
    path = _EXPORT_DIR / "dw_benchmark_passing.csv"
    out_df.to_csv(path, index=False)
    return path


def export_network_csv(df: pd.DataFrame) -> Path:
    """Exporta CSV para Flourish: conexiones de pase entre jugadores.

    Crea aristas basadas en: misma posición + similitud de métricas de pase.
    El peso refuerza la conexión (mayor peso = más similitud).

    Returns:
        Ruta del CSV generado.
    """
    df_clean = df[["Player", "Pos", "Cmp", "PrgP", "PPA"]].dropna().copy()
    df_clean["short"] = df_clean["Player"].apply(_short_name)
    df_clean["Pos_base"] = df_clean["Pos"].str.split(",").str[0].str.strip()

    edges: list[dict[str, str | float]] = []

    for i, row_i in df_clean.iterrows():
        for j, row_j in df_clean.iterrows():
            if i >= j:
                continue
            if row_i["Pos_base"] != row_j["Pos_base"]:
                continue

            cmp_diff = abs(row_i["Cmp"] - row_j["Cmp"])
            prgp_diff = abs(row_i["PrgP"] - row_j["PrgP"])
            max_cmp = max(row_i["Cmp"], row_j["Cmp"], 1)
            max_prgp = max(row_i["PrgP"], row_j["PrgP"], 1)

            similarity = 1.0 - (
                0.5 * (cmp_diff / max_cmp) + 0.5 * (prgp_diff / max_prgp)
            )

            if similarity > 0.4:
                edges.append({
                    "source": row_i["short"],
                    "target": row_j["short"],
                    "weight": round(similarity, 4),
                    "source_position": row_i["Pos_base"],
                    "target_position": row_j["Pos_base"],
                })

    out_df = pd.DataFrame(edges)
    path = _EXPORT_DIR / "flourish_network_pases.csv"
    out_df.to_csv(path, index=False)
    return path


def _betweenness_proxy(df: pd.DataFrame) -> pd.Series:
    """Calcula una proxy de betweenness centrality.

    Usa: (KP + 1/3 + PPA) / (Att + 1) como medida de intermediación
    en la red de pase.

    Returns:
        Serie con centralidad normalizada (0-1).
    """
    kp = pd.to_numeric(df.get("KP", 0), errors="coerce").fillna(0)
    tercios = pd.to_numeric(df.get("1/3", 0), errors="coerce").fillna(0)
    ppa = pd.to_numeric(df.get("PPA", 0), errors="coerce").fillna(0)
    att = pd.to_numeric(df.get("Att", 1), errors="coerce").fillna(1).clip(lower=1)

    raw = (kp + tercios + ppa) / att
    max_val = raw.max()
    if max_val > 0:
        return (raw / max_val).round(4)
    return raw


def export_centrality_csv(df: pd.DataFrame) -> Path:
    """Exporta CSV para Observable Plot: centralidad vs precisión de pase.

    Returns:
        Ruta del CSV generado.
    """
    cols_needed = ["Player", "Pos", "Cmp%", "Att", "KP", "1/3", "PPA"]
    present = [c for c in cols_needed if c in df.columns]
    df_sub = df[present].dropna(subset=["Cmp%", "Att"]).copy()

    df_sub["betweenness"] = _betweenness_proxy(df_sub).values
    df_sub["pass_accuracy"] = pd.to_numeric(df_sub["Cmp%"], errors="coerce")
    df_sub["position"] = df_sub.get("Pos", pd.Series("Unknown")).str.split(",").str[0]

    out_df = df_sub[["Player", "position", "betweenness", "pass_accuracy"]].copy()
    out_df = out_df.sort_values("betweenness", ascending=False).reset_index(drop=True)

    path = _EXPORT_DIR / "observable_centralidad.csv"
    out_df.to_csv(path, index=False)
    return path


def _generate_embed_html() -> str:
    """Genera snippets HTML responsive para incrustar visualizaciones.

    Returns:
        String con el contenido Markdown formateado.
    """
    snippet = """# Embed Snippets - Visualizaciones United Passing 24-25

## Datawrapper Benchmark (Métricas de Pase)

```html
<div style="width:100%; max-width:800px; margin:0 auto;">
  <iframe
    title="Manchester United vs PL Average - Passing Metrics"
    aria-label="Bar Chart"
    src="https://datawrapper.dwcdn.net/CHART_ID/"
    loading="lazy"
    style="width:100%; border:none; height:400px;"
  ></iframe>
</div>
<noscript>
  <p>Ver <a href="data/export/dw_benchmark_passing.csv">dw_benchmark_passing.csv</a> para los datos.</p>
</noscript>
```

## Flourish Network Graph (Conexiones entre Jugadores)

```html
<div style="width:100%; max-width:900px; margin:0 auto;">
  <iframe
    title="Red de Pases - Manchester United"
    aria-label="Network Graph"
    src="https://public.flourish.studio/visualisation/CHART_ID/"
    loading="lazy"
    style="width:100%; border:none; height:500px;"
  ></iframe>
</div>
<noscript>
  <p>Ver <a href="data/export/flourish_network_pases.csv">flourish_network_pases.csv</a> para los datos.</p>
</noscript>
```

## Observable Scatter (Centralidad vs Precisión)

```html
<div style="width:100%; max-width:800px; margin:0 auto;">
  <div id="observable-chart"></div>
  <script type="module">
    import {Plot} from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";
    import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

    const data = await d3.csv("data/export/observable_centralidad.csv");
    const chart = Plot.plot({
      marks: [
        Plot.dot(data, {
          x: "betweenness",
          y: "pass_accuracy",
          fill: "position",
          r: 4,
          title: d => `${d.Player}\\nBetweenness: ${d.betweenness}\\nAccuracy: ${d.pass_accuracy}%`
        }),
        Plot.linearRegressionY(data, {x: "betweenness", y: "pass_accuracy", stroke: "red", strokeWidth: 1.5})
      ],
      x: {label: "Betweenness Centrality →", grid: true},
      y: {label: "Pass Accuracy (%) →", grid: true},
      color: {legend: true},
      width: 700,
      height: 450,
      marginBottom: 50,
      marginLeft: 60
    });
    document.getElementById("observable-chart").appendChild(chart);
  </script>
</div>
<noscript>
  <p>Ver <a href="data/export/observable_centralidad.csv">observable_centralidad.csv</a> para los datos.</p>
</noscript>
```
"""
    return snippet


def main() -> None:
    """Punto de entrada principal: genera CSVs y snippets HTML."""
    _ensure_export_dir()

    print("Cargando datos de pases...")
    df = _load_passes()
    print(f"  → {len(df)} jugadores cargados.")

    print("\n[1/3] Exportando benchmark Datawrapper...")
    path1 = export_benchmark_csv(df)
    print(f"  → {path1}")

    print("\n[2/3] Exportando red Flourish...")
    path2 = export_network_csv(df)
    print(f"  → {path2}")

    print("\n[3/3] Exportando centralidad Observable...")
    path3 = export_centrality_csv(df)
    print(f"  → {path3}")

    print("\nGenerando snippets HTML...")
    md_content = _generate_embed_html()
    md_path = _EXPORT_DIR / "embed_snippets.md"
    md_path.write_text(md_content, encoding="utf-8")
    print(f"  → {md_path}")

    print("\n✅ Exportación completada exitosamente.")


if __name__ == "__main__":
    main()
