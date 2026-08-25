"""
Analisis de similaridad entre jugadores.
Cosine similarity + perfilamiento por metricas de pase.
"""
import json
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.preprocessing import StandardScaler
    AVAILABLE = True
except ImportError:
    AVAILABLE = False


def run_similarity(data_dir: Path = Path("data/export"), output_dir: Path = Path("data/export")) -> dict:
    if not AVAILABLE:
        print("[SIM] scikit-learn no instalado")
        return {}

    results = {}
    csv_files = list(data_dir.glob("*.csv"))
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, encoding="utf-8")
        name = csv_file.stem
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) < 2 or "player" not in df.columns:
            continue

        X = df[num_cols].fillna(0).replace([np.inf, -np.inf], 0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        sim_matrix = cosine_similarity(X_scaled)
        players = df["player"].tolist()

        # Top 3 most similar pairs
        pairs = []
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                pairs.append({
                    "player_a": players[i],
                    "player_b": players[j],
                    "similarity": round(float(sim_matrix[i, j]), 4),
                })
        pairs.sort(key=lambda x: x["similarity"], reverse=True)

        # Player profiles
        profiles = {}
        for idx, player in enumerate(players):
            profiles[player] = {col: round(float(X.iloc[idx][col]), 4) for col in num_cols}
            profiles[player]["cluster"] = int(np.argmax(sim_matrix[idx])) if idx != np.argmax(sim_matrix[idx]) else -1

        results[name] = {
            "n_players": len(players),
            "top_similar_pairs": pairs[:5],
            "mean_similarity": round(float(np.mean(sim_matrix[np.triu_indices(len(players), k=1)])), 4),
            "profiles": profiles,
        }
        print(f"[SIM] {name}: {len(players)} jugadores, similaridad media = {results[name]['mean_similarity']:.3f}")

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "similarity_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results


if __name__ == "__main__":
    run_similarity()
