# Manchester United Passing Network Analysis 2024-25

[![CI](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/united-passing-efficiency-24-25/actions/workflows/ci.yml) [![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org) [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## What is this?

EN: I wanted to visualize Manchester United's passing network and see who the key connectors are. Using FBref data, I built a graph with NetworkX, calculated centrality metrics, and compared performance against the rest of the Premier League.

ES: Quería visualizar la red de pases del Manchester United y ver quiénes son los conectores clave. Con datos de FBref, construí un grafo con NetworkX, calculé métricas de centralidad y comparé el rendimiento contra el resto de la Premier League.

---

## Questions I asked

1. **Broker identification:** Which midfielders are structural brokers (high betweenness centrality)? What happens if they're removed?
2. **Expected threat distribution:** Who generates the most xT, and does that player also occupy the most central network position?
3. **Performance by opposition tier:** Does passing quality drop against Top 6 teams?

**Hypothesis:** United's network has a single dominant broker rather than distributed hubs, concentrating creative risk.

---

## How it works

### Data

FBref passing data for 36 Manchester United players (2024-25 season).

### Graph construction

```python
G = nx.DiGraph()
for _, row in passes.iterrows():
    G.add_edge(row["passer"], row["recipient"], weight=row["volume"])
```

### Centrality metrics

| Metric | What it tells us |
|--------|-----------------|
| Betweenness | Who bridges different parts of the team |
| Degree | Who passes/receives most |
| PageRank | Who is most important in the network flow |
| Communities | Which clusters form naturally |

---

## Key findings

- Bruno Fernandes is the dominant broker (~45% betweenness)
- 3 communities detected (defense, midfield, attack)
- Passing accuracy drops ~8% against Top 6 opposition
- Single-broker structure creates fragility

---

## Visualizations

<details>
<summary><strong>Datawrapper — PL Benchmark</strong></summary>

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;">
  <iframe src="https://datawrapper.dwcdn.net/BlxD1/" title="PL Benchmark" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" loading="lazy" allowfullscreen></iframe>
</div>
</details>

<details>
<summary><strong>Observable — Interactive graph</strong></summary>

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;">
  <iframe src="https://observablehq.com/@alvarosalinaso/passing-network" title="Passing Network" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" loading="lazy" allowfullscreen></iframe>
</div>
</details>

---

## How to run

```bash
git clone https://github.com/alvarosalinaso/united-passing-efficiency-24-25
cd united-passing-efficiency-24-25
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/data.py
python src/graph_analysis.py
python src/benchmark.py
```

---

## Project structure

```
united-passing-efficiency-24-25/
├── src/
│   ├── data.py              # ETL + normalization
│   ├── graph_analysis.py    # NetworkX graph + centrality
│   ├── benchmark.py         # PL comparison
│   └── export_visualizations.py
├── data/raw/passing.csv     # FBref source data
├── tests/
└── requirements.txt
```

---

> **Álvaro Salinas Ortiz**
> [LinkedIn](https://www.linkedin.com/in/alvaro-salinas-ortiz) | [Portfolio](https://alvarosalinaso.github.io/portfolio-web/)
