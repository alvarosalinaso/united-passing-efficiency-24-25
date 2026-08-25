"""
Clusterizacion de jugadores por metricas de pases.
K-Means + elbow + silhouette + PCA visualization.
"""

import json
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score
    from sklearn.preprocessing import StandardScaler

    AVAILABLE = True
except ImportError:
    AVAILABLE = False


def run_clustering(
    data_dir: Path = Path("data/export"), output_dir: Path = Path("data/export")
) -> dict:
    if not AVAILABLE:
        print("[CLUSTER] scikit-learn no instalado")
        return {}

    csv_files = list(data_dir.glob("*.csv"))
    if not csv_files:
        print("[CLUSTER] No CSV files found")
        return {}

    results = {}
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, encoding="utf-8")
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) < 2:
            continue

        X = df[num_cols].fillna(0).replace([np.inf, -np.inf], 0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        inertias, silhouettes = [], []
        K_range = range(2, min(7, len(df) // 3 + 1))
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X_scaled)
            inertias.append(km.inertia_)
            silhouettes.append(silhouette_score(X_scaled, labels))

        optimal_k = list(K_range)[np.argmax(silhouettes)] if silhouettes else 2
        km_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        df["cluster"] = km_final.fit_predict(X_scaled)

        # PCA for visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)  # noqa: F841

        profiles = {}
        for c in range(optimal_k):
            cluster_df = df[df["cluster"] == c]
            profiles[f"cluster_{c}"] = {
                "size": len(cluster_df),
                "pct": round(len(cluster_df) / len(df) * 100, 1),
                "mean_values": {col: round(cluster_df[col].mean(), 3) for col in num_cols},
            }
            if "player" in cluster_df.columns:
                profiles[f"cluster_{c}"]["players"] = cluster_df["player"].tolist()[:5]

        results[csv_file.stem] = {
            "optimal_k": optimal_k,
            "silhouette": round(max(silhouettes), 3) if silhouettes else 0,
            "features": num_cols,
            "profiles": profiles,
            "pca_variance_explained": round(sum(pca.explained_variance_ratio_), 3),
        }
        print(
            f"[CLUSTER] {csv_file.stem}: k={optimal_k}, silhouette={max(silhouettes):.3f}"
            if silhouettes
            else f"[CLUSTER] {csv_file.stem}: done"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "clustering_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results


if __name__ == "__main__":
    run_clustering()
