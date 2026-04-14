import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx

st.set_page_config(
    page_title="United Passing | Network Analysis",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=IBM+Plex+Mono:wght@300;400&display=swap');
html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; font-size: 16px; }
h1, h2, h3 { font-family: 'Rajdhani', sans-serif; font-weight: 700; color: #E8C547; letter-spacing: 3px; }
.metric-card {
    background: #111318;
    border: 1px solid #2a2d35;
    border-bottom: 2px solid #E8C547;
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #E8C547; font-family: 'IBM Plex Mono', monospace; }
.metric-lab { font-size: 0.7rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1.5px; }
</style>
""", unsafe_allow_html=True)

# ── DATOS ──────────────────────────────────────────────────────────────────────
np.random.seed(99)

SQUAD = [
    {"player": "Onana",     "pos": "GK",  "x": 5,  "y": 34, "age": 28, "apps": 36},
    {"player": "Dalot",     "pos": "RB",  "x": 25, "y": 65, "age": 25, "apps": 35},
    {"player": "L.Martínez","pos": "CB",  "x": 20, "y": 50, "age": 26, "apps": 29},
    {"player": "De Ligt",   "pos": "CB",  "x": 20, "y": 18, "age": 25, "apps": 26},
    {"player": "Shaw",      "pos": "LB",  "x": 25, "y": 3,  "age": 29, "apps": 12},
    {"player": "Ugarte",    "pos": "CDM", "x": 40, "y": 34, "age": 23, "apps": 22},
    {"player": "Mainoo",    "pos": "CM",  "x": 50, "y": 55, "age": 19, "apps": 28},
    {"player": "Casemiro",  "pos": "CDM", "x": 40, "y": 14, "age": 32, "apps": 26},
    {"player": "Bruno",     "pos": "CAM", "x": 62, "y": 34, "age": 30, "apps": 32},
    {"player": "Garnacho",  "pos": "RW",  "x": 72, "y": 65, "age": 20, "apps": 34},
    {"player": "Hojlund",   "pos": "ST",  "x": 80, "y": 34, "age": 22, "apps": 20},
]

PASSING_BASE = [
    ("Onana", "L.Martínez", 18), ("Onana", "De Ligt", 14), ("Onana", "Ugarte", 8),
    ("L.Martínez", "Bruno", 12), ("L.Martínez", "Mainoo", 10), ("L.Martínez", "Ugarte", 9),
    ("De Ligt", "Casemiro", 11), ("De Ligt", "L.Martínez", 7), ("De Ligt", "Shaw", 6),
    ("Dalot", "Bruno", 9), ("Dalot", "Mainoo", 7), ("Dalot", "Garnacho", 5),
    ("Shaw", "Ugarte", 8), ("Shaw", "Casemiro", 6), ("Shaw", "Bruno", 4),
    ("Ugarte", "Mainoo", 14), ("Ugarte", "Bruno", 10), ("Ugarte", "L.Martínez", 5),
    ("Casemiro", "Ugarte", 9), ("Casemiro", "De Ligt", 4), ("Casemiro", "Bruno", 7),
    ("Mainoo", "Bruno", 16), ("Mainoo", "Garnacho", 8), ("Mainoo", "Hojlund", 5),
    ("Bruno", "Garnacho", 14), ("Bruno", "Hojlund", 11), ("Bruno", "Mainoo", 9),
    ("Bruno", "Dalot", 6), ("Garnacho", "Hojlund", 8), ("Garnacho", "Bruno", 5),
    ("Hojlund", "Bruno", 4), ("Hojlund", "Mainoo", 3),
]

PLAYER_STATS = {
    "Onana":      {"pass_acc": 72.4, "prog_passes": 4.5, "xT": 0.02, "vert_idx": 0.95},
    "Dalot":      {"pass_acc": 84.1, "prog_passes": 4.2, "xT": 0.22, "vert_idx": 0.61},
    "L.Martínez": {"pass_acc": 93.4, "prog_passes": 6.5, "xT": 0.15, "vert_idx": 0.88},
    "De Ligt":    {"pass_acc": 91.0, "prog_passes": 3.8, "xT": 0.05, "vert_idx": 0.55},
    "Shaw":       {"pass_acc": 87.1, "prog_passes": 4.1, "xT": 0.20, "vert_idx": 0.70},
    "Ugarte":     {"pass_acc": 89.1, "prog_passes": 3.4, "xT": 0.08, "vert_idx": 0.41},
    "Mainoo":     {"pass_acc": 85.7, "prog_passes": 4.0, "xT": 0.24, "vert_idx": 0.64},
    "Casemiro":   {"pass_acc": 86.5, "prog_passes": 3.2, "xT": 0.11, "vert_idx": 0.45},
    "Bruno":      {"pass_acc": 88.4, "prog_passes": 5.1, "xT": 0.42, "vert_idx": 0.78},
    "Garnacho":   {"pass_acc": 74.1, "prog_passes": 1.8, "xT": 0.35, "vert_idx": 0.48},
    "Hojlund":    {"pass_acc": 83.1, "prog_passes": 3.5, "xT": 0.18, "vert_idx": 0.58},
}

df_squad = pd.DataFrame(SQUAD)

# Rival teams PL
PL_TEAMS = {
    "Arsenal": {"poss": 60.5, "pass_acc": 88.2, "prog_p": 55.4, "xT": 2.1},
    "Man City": {"poss": 65.2, "pass_acc": 90.1, "prog_p": 62.3, "xT": 2.45},
    "Liverpool": {"poss": 61.0, "pass_acc": 86.5, "prog_p": 58.1, "xT": 2.2},
    "Man United": {"poss": 52.1, "pass_acc": 84.5, "prog_p": 42.1, "xT": 1.48},
    "Aston Villa": {"poss": 54.2, "pass_acc": 85.0, "prog_p": 45.2, "xT": 1.6},
    "Tottenham": {"poss": 59.8, "pass_acc": 86.8, "prog_p": 52.1, "xT": 1.9},
    "Chelsea": {"poss": 58.5, "pass_acc": 87.1, "prog_p": 50.4, "xT": 1.85},
    "Newcastle": {"poss": 51.0, "pass_acc": 82.5, "prog_p": 41.2, "xT": 1.55},
    "Brighton": {"poss": 58.1, "pass_acc": 86.2, "prog_p": 49.8, "xT": 1.7},
    "West Ham": {"poss": 45.2, "pass_acc": 79.8, "prog_p": 32.5, "xT": 1.1},
}

# ── SIDEBAR ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🕸️ Filtros")
    st.markdown("---")

    vista = st.selectbox("Vista", [
        "Red táctica de pases", "Métricas individuales",
        "Comparativa vs Premier League", "Análisis por oponente"
    ])

    oponente_tier = st.radio("Tipo de rival", ["Resto PL", "Top 6"])
    min_passes = st.slider("Mínimo de pases para mostrar conexión", 1, 20, 5)

    if vista == "Métricas individuales":
        pos_sel = st.multiselect("Posición", ["GK", "RB", "LB", "CB", "CDM", "CM", "CAM", "RW", "ST"],
                                 default=["CDM", "CM", "CAM"])
        metrica_x = st.selectbox("Eje X", ["pass_acc", "prog_passes", "xT", "vert_idx"])
        metrica_y = st.selectbox("Eje Y", ["xT", "prog_passes", "pass_acc", "vert_idx"])

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#4b5563;'>
    Álvaro Salinas Ortiz<br>
    <a href='https://github.com/alvarosalinaso' style='color:#E8C547;'>github.com/alvarosalinaso</a>
    </div>
    """, unsafe_allow_html=True)

# Ajustar pases según rival
def adjust_passes(base_passes, tier):
    adjusted = []
    for src, tgt, w in base_passes:
        if tier == "Top 6":
            factor = max(0.5, np.random.uniform(0.6, 0.85))
        else:
            factor = np.random.uniform(0.95, 1.15)
        adjusted.append((src, tgt, max(1, int(w * factor))))
    return adjusted

passes = adjust_passes(PASSING_BASE, oponente_tier)
passes_filt = [(s, t, w) for s, t, w in passes if w >= min_passes]

# Construir grafo
G = nx.DiGraph()
for p in SQUAD:
    G.add_node(p["player"])
for s, t, w in passes_filt:
    G.add_edge(s, t, weight=w)

betweenness = nx.betweenness_centrality(G, weight="weight", normalized=True)
pagerank = nx.pagerank(G, weight="weight")
in_deg = dict(G.in_degree(weight="weight"))
out_deg = dict(G.out_degree(weight="weight"))

# ── HEADER ──────────────────────────────────────────────────────────────────────
st.markdown("# UNITED PASSING NETWORK")
st.markdown(f"### {vista.upper()} — vs {oponente_tier}")
st.markdown("---")

# KPIs
total_passes = sum(w for _, _, w in passes)
avg_acc = np.mean([v["pass_acc"] for v in PLAYER_STATS.values()])
top_broker = max(betweenness, key=betweenness.get)
top_xT = max(PLAYER_STATS, key=lambda x: PLAYER_STATS[x]["xT"])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{total_passes}</div><div class='metric-lab'>Pases totales</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{avg_acc:.1f}%</div><div class='metric-lab'>Precisión promedio</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{top_broker}</div><div class='metric-lab'>Broker táctico</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{top_xT}</div><div class='metric-lab'>Mayor xT generado</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── VISTAS ──────────────────────────────────────────────────────────────────────

if vista == "Red táctica de pases":
    pos_layout = {p["player"]: (p["x"], p["y"]) for p in SQUAD}
    max_w = max(w for _, _, w in passes_filt) if passes_filt else 1

    edge_traces = []
    for s, t, w in passes_filt:
        x0, y0 = pos_layout[s]
        x1, y1 = pos_layout[t]
        opacity = 0.15 + (w / max_w) * 0.75
        width = 1 + (w / max_w) * 8
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None], mode="lines",
            line=dict(width=width, color=f"rgba(232,197,71,{opacity:.2f})"),
            hoverinfo="none", showlegend=False
        ))

    node_x = [pos_layout[p["player"]][0] for p in SQUAD]
    node_y = [pos_layout[p["player"]][1] for p in SQUAD]
    node_sizes = [14 + betweenness.get(p["player"], 0) * 80 for p in SQUAD]
    node_colors = [betweenness.get(p["player"], 0) for p in SQUAD]
    node_text = [p["player"] for p in SQUAD]
    node_hover = [
        f"<b>{p['player']}</b> ({p['pos']})<br>"
        f"Betweenness: {betweenness.get(p['player'], 0):.3f}<br>"
        f"PageRank: {pagerank.get(p['player'], 0):.3f}<br>"
        f"Pases salientes: {out_deg.get(p['player'], 0)}<br>"
        f"Pass accuracy: {PLAYER_STATS[p['player']]['pass_acc']}%"
        for p in SQUAD
    ]

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_text, textposition="top center",
        hovertext=node_hover, hoverinfo="text",
        marker=dict(size=node_sizes, color=node_colors,
                    colorscale=[[0, "#1a1a2e"], [0.5, "#DA291C"], [1, "#E8C547"]],
                    colorbar=dict(title="Betweenness", thickness=10, len=0.6),
                    line=dict(width=2, color="white")),
        textfont=dict(size=10, color="white", family="Rajdhani"),
        showlegend=False
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    # Marcas del campo
    for shape_args in [
        dict(type="rect", x0=0, y0=0, x1=100, y1=68, line=dict(color="rgba(255,255,255,0.25)", width=1)),
        dict(type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16, line=dict(color="rgba(255,255,255,0.15)", width=1)),
        dict(type="rect", x0=83.5, y0=13.84, x1=100, y1=54.16, line=dict(color="rgba(255,255,255,0.15)", width=1)),
        dict(type="circle", x0=44, y0=28, x1=56, y1=40, line=dict(color="rgba(255,255,255,0.15)", width=1)),
        dict(type="line", x0=50, y0=0, x1=50, y1=68, line=dict(color="rgba(255,255,255,0.1)", width=1)),
    ]:
        fig.add_shape(**shape_args)

    fig.update_layout(
        title=f"Red táctica de pases — vs {oponente_tier} | Tamaño nodo = Betweenness Centrality",
        plot_bgcolor="#2d5a27", paper_bgcolor="#111318",
        font=dict(color="white", family="Rajdhani"),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-5, 105]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-5, 73]),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabla de centralidades
    st.markdown("#### Métricas de red por jugador")
    metrics_table = pd.DataFrame({
        "Jugador": [p["player"] for p in SQUAD],
        "Posición": [p["pos"] for p in SQUAD],
        "Betweenness": [round(betweenness.get(p["player"], 0), 4) for p in SQUAD],
        "PageRank": [round(pagerank.get(p["player"], 0), 4) for p in SQUAD],
        "Pases salientes": [out_deg.get(p["player"], 0) for p in SQUAD],
        "Pases recibidos": [in_deg.get(p["player"], 0) for p in SQUAD],
    }).sort_values("Betweenness", ascending=False).reset_index(drop=True)
    st.dataframe(metrics_table, use_container_width=True, height=350)

elif vista == "Métricas individuales":
    df_stats = pd.DataFrame([
        {"player": k, "pos": next(p["pos"] for p in SQUAD if p["player"] == k), **v}
        for k, v in PLAYER_STATS.items()
    ])
    df_f = df_stats[df_stats["pos"].isin(pos_sel)] if pos_sel else df_stats

    label_map = {"pass_acc": "Precisión pase %", "prog_passes": "Pases progresivos/90",
                 "xT": "xT generado", "vert_idx": "Índice verticalidad"}

    fig = px.scatter(df_f, x=metrica_x, y=metrica_y, text="player", color="pos",
                     size=[PLAYER_STATS[p]["pass_acc"] for p in df_f["player"]],
                     title=f"{label_map[metrica_x]} vs {label_map[metrica_y]}",
                     color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="white")))
    fig.add_hline(y=df_f[metrica_y].mean(), line_dash="dash", line_color="#444")
    fig.add_vline(x=df_f[metrica_x].mean(), line_dash="dash", line_color="#444")
    fig.update_layout(template="plotly_dark", paper_bgcolor="#111318",
                      plot_bgcolor="#111318", height=480, font=dict(family="Rajdhani"))
    st.plotly_chart(fig, use_container_width=True)

elif vista == "Comparativa vs Premier League":
    df_pl = pd.DataFrame([{"team": k, **v} for k, v in PL_TEAMS.items()])

    col_a, col_b = st.columns(2)
    with col_a:
        metrica_pl = st.selectbox("Métrica comparativa", ["pass_acc", "prog_p", "xT", "poss"],
                                  format_func=lambda x: {"pass_acc": "Precisión de pase %",
                                                          "prog_p": "Pases progresivos",
                                                          "xT": "xT generado", "poss": "Posesión %"}[x])
    df_pl_sorted = df_pl.sort_values(metrica_pl)
    fig = go.Figure(go.Bar(
        x=df_pl_sorted[metrica_pl], y=df_pl_sorted["team"], orientation="h",
        marker_color=["#E8C547" if t == "Man United" else "#1f2937" for t in df_pl_sorted["team"]],
        text=[f"{v:.1f}" for v in df_pl_sorted[metrica_pl]], textposition="outside"
    ))
    label_pl = {"pass_acc": "Precisión de pase %", "prog_p": "Pases progresivos/partido",
                "xT": "xT generado/partido", "poss": "Posesión %"}
    fig.update_layout(template="plotly_dark", paper_bgcolor="#111318", plot_bgcolor="#111318",
                      title=f"Premier League — {label_pl[metrica_pl]}",
                      height=420, font=dict(family="Rajdhani"))
    st.plotly_chart(fig, use_container_width=True)

    utd = PL_TEAMS["Man United"]
    others = [v for k, v in PL_TEAMS.items() if k != "Man United"]
    st.info(f"Man United vs promedio PL — Precisión pase: **{utd['pass_acc']}%** vs **{np.mean([o['pass_acc'] for o in others]):.1f}%** | "
            f"xT: **{utd['xT']}** vs **{np.mean([o['xT'] for o in others]):.2f}**")

elif vista == "Análisis por oponente":
    rivals_data = []
    for tier in ["Resto PL", "Top 6"]:
        adj = adjust_passes(PASSING_BASE, tier)
        acc_mod = 0 if tier == "Resto PL" else -4.2
        rivals_data.append({
            "rival": tier,
            "total_passes": sum(w for _, _, w in adj),
            "avg_acc": avg_acc + acc_mod,
            "xT_total": sum(PLAYER_STATS[p]["xT"] for p in PLAYER_STATS) * (1.0 if tier == "Resto PL" else 0.78),
        })

    df_riv = pd.DataFrame(rivals_data)

    fig = make_subplots(rows=1, cols=3, subplot_titles=["Total pases", "Precisión promedio %", "xT total"])
    colors = ["#E8C547", "#DA291C"]
    for i, col_name in enumerate(["total_passes", "avg_acc", "xT_total"]):
        fig.add_trace(go.Bar(x=df_riv["rival"], y=df_riv[col_name],
                             marker_color=colors, showlegend=False), row=1, col=i+1)

    fig.update_layout(template="plotly_dark", paper_bgcolor="#111318", plot_bgcolor="#111318",
                      title="Rendimiento de pases: Resto PL vs Top 6",
                      height=380, font=dict(family="Rajdhani"))
    st.plotly_chart(fig, use_container_width=True)

    st.warning(f"Contra el **Top 6**, United reduce su precisión de pase en ~4pp y su xT generado cae un 22%. "
               f"El análisis de red muestra que **{top_broker}** es el jugador cuya neutralización más impacta el flujo ofensivo.")
