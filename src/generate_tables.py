"""Genera tabla ejecutiva de pases con fallback a pandas styling"""

from pathlib import Path

import pandas as pd


def generate():
    csv_path = Path("data/export/dw_benchmark_passing.csv")
    if not csv_path.exists():
        print(f"[TABLE] {csv_path} not found, skipping")
        return
    df = pd.read_csv(csv_path, encoding="utf-8")
    if "player" in df.columns and "betweenness" in df.columns:
        top = df.nlargest(5, "betweenness")[["player", "betweenness", "degree", "precision"]]
        top.columns = ["Jugador", "Betweenness", "Degree", "Precisión Pase"]
    else:
        top = df.head(5)

    # Try great_tables first, fallback to pandas styling
    try:
        from great_tables import GT
        tbl = (
            GT(top)
            .tab_header(title="Top 5 Métricas de Red — Man United Pases 2024-25")
            .tab_source_note("Fuente: StatsBomb Open Data | Análisis: Álvaro Salinas")
        )
        Path("assets").mkdir(exist_ok=True)
        tbl.save("assets/executive_table.html")
        print("[TABLE] assets/executive_table.html generado (great_tables)")
    except ImportError:
        # Fallback: pandas styling
        styled = top.style.set_caption("Top 5 Métricas de Red — Man United Pases 2024-25") \
            .set_table_styles([
                {"selector": "caption", "props": [("font-size", "16px"), ("font-weight", "bold")]},
                {"selector": "th", "props": [("background-color", "#da020e"), ("color", "white"), ("font-weight", "bold")]},
                {"selector": "td", "props": [("border", "1px solid #ddd")]},
            ]) \
            .format(precision=3) \
            .hide(axis="index")
        Path("assets").mkdir(exist_ok=True)
        styled.to_html("assets/executive_table.html")
        print("[TABLE] assets/executive_table.html generado (pandas styling fallback)")


if __name__ == "__main__":
    generate()
