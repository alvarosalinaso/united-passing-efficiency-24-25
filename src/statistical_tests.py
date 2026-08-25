"""Tests estadísticos para análisis de pases Manchester United."""
import json
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


def run_statistical_tests(data_dir: Path = Path("data/export"), output_dir: Path = Path("data/export")) -> dict:
    if not SCIPY_AVAILABLE:
        return {}

    results = {}

    csv_files = list(data_dir.glob("*.csv"))
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, encoding="utf-8")
        name = csv_file.stem

        # Correlation between centrality metrics
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) >= 2:
            corr_matrix = df[num_cols].corr()
            # Find strongest pair
            max_corr = 0
            best_pair = ("", "")
            for i in range(len(num_cols)):
                for j in range(i+1, len(num_cols)):
                    c = abs(corr_matrix.iloc[i, j])
                    if c > max_corr:
                        max_corr = c
                        best_pair = (num_cols[i], num_cols[j])

            if max_corr > 0:
                r, p = stats.pearsonr(df[best_pair[0]].dropna(), df[best_pair[1]].dropna())
                results[f"{name}_strongest_correlation"] = {
                    "test": "Pearson correlation",
                    "variables": list(best_pair),
                    "r": round(r, 4),
                    "p_value": round(p, 6),
                    "significant": p < 0.05,
                }
                print(f"[STATS] {name}: {best_pair} r={r:.3f}, p={p:.4f}")

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "statistical_tests.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results
