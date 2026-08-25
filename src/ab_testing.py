"""
A/B Testing: Comparacion de estilos de pase.
United vs Promedio PL con tests formales.
"""

import json
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
    from scipy import stats

    AVAILABLE = True
except ImportError:
    AVAILABLE = False


def run_ab_testing(
    data_dir: Path = Path("data/export"), output_dir: Path = Path("data/export")
) -> dict:
    if not AVAILABLE:
        print("[AB] scipy no instalado")
        return {}

    results = {}
    csv_files = list(data_dir.glob("*.csv"))
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, encoding="utf-8")
        name = csv_file.stem
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(num_cols) < 2:
            continue

        # Split into high vs low performers based on median of first numeric column
        median_val = df[num_cols[0]].median()
        group_high = df[df[num_cols[0]] >= median_val]
        group_low = df[df[num_cols[0]] < median_val]

        test_results = []
        for col in num_cols[1:]:
            high_vals = group_high[col].dropna()
            low_vals = group_low[col].dropna()
            if len(high_vals) > 2 and len(low_vals) > 2:
                t_stat, p_val = stats.ttest_ind(high_vals, low_vals, equal_var=False)
                cohens_d = (
                    (high_vals.mean() - low_vals.mean())
                    / np.sqrt((high_vals.std() ** 2 + low_vals.std() ** 2) / 2)
                    if high_vals.std() > 0 and low_vals.std() > 0
                    else 0
                )
                test_results.append(
                    {
                        "metric": col,
                        "t_statistic": round(t_stat, 4),
                        "p_value": round(p_val, 6),
                        "significant": p_val < 0.05,
                        "cohens_d": round(cohens_d, 4),
                        "effect_size": "grande"
                        if abs(cohens_d) > 0.8
                        else "mediano"
                        if abs(cohens_d) > 0.5
                        else "pequeno",
                    }
                )

        results[name] = {
            "split_metric": num_cols[0],
            "threshold": round(median_val, 4),
            "n_high": len(group_high),
            "n_low": len(group_low),
            "tests": test_results,
            "n_significant": sum(1 for t in test_results if t["significant"]),
        }
        print(
            f"[AB] {name}: {results[name]['n_significant']}/{len(test_results)} metricas significativas"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "ab_testing_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results


if __name__ == "__main__":
    run_ab_testing()
