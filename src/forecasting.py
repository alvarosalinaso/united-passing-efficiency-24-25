"""
Forecasting de metricas de pases.
ARIMA + Exponential Smoothing para predecir eficiencia futura.
"""

import json
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.holtwinters import ExponentialSmoothing  # noqa: F401
    from statsmodels.tsa.stattools import adfuller

    AVAILABLE = True
except ImportError:
    AVAILABLE = False


def run_forecasting(
    data_dir: Path = Path("data/export"), output_dir: Path = Path("data/export")
) -> dict:
    if not AVAILABLE:
        print("[FORECAST] statsmodels no instalado")
        return {}

    results = {}
    csv_files = list(data_dir.glob("*.csv"))
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, encoding="utf-8")
        name = csv_file.stem
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) < 1 or len(df) < 5:
            continue

        ts = df[num_cols[0]].dropna()
        if len(ts) < 5:
            continue

        try:
            adf_p = adfuller(ts.values)[1]
            model = ARIMA(ts.values, order=(1, 1, 1))
            fit = model.fit()
            forecast = fit.forecast(steps=3)
            results[name] = {
                "metric": num_cols[0],
                "adf_p_value": round(adf_p, 4),
                "forecast_next_3": [round(float(v), 4) for v in forecast],
                "aic": round(float(fit.aic), 2),
            }
            print(f"[FORECAST] {name}: next 3 = {[round(float(v), 3) for v in forecast]}")
        except Exception as e:
            print(f"[FORECAST] {name} error: {e}")

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "forecasting_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results


if __name__ == "__main__":
    run_forecasting()
