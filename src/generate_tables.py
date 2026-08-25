"""Genera tabla ejecutiva de pases con great_tables"""
import pandas as pd
from pathlib import Path
from great_tables import GT

def generate():
    df = pd.read_csv("data/export/benchmark_pases.csv", encoding="utf-8")
    if "player" in df.columns and "betweenness" in df.columns:
        top = df.nlargest(5, "betweenness")[["player", "betweenness", "degree", "precision"]]
        top.columns = ["Jugador", "Betweenness", "Degree", "Precisión Pase"]
    else:
        top = df.head(5)
    
    tbl = (
        GT(top)
        .tab_header(title="Top 5 Métricas de Red — Man United Pases 2024-25")
        .tab_source_note("Fuente: StatsBomb Open Data | Análisis: Álvaro Salinas")
    )
    Path("assets").mkdir(exist_ok=True)
    tbl.save("assets/executive_table.html")
    print("[TABLE] assets/executive_table.html generado")

if __name__ == "__main__":
    generate()
