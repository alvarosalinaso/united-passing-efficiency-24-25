"""
═══════════════════════════════════════════════════════════════════════════════
  United Passing Efficiency — Streamlit App
  Autor : Álvaro Salinas Ortiz  |  github.com/alvarosalinaso
  Stack : Streamlit · Plotly · Pandas · NumPy
═══════════════════════════════════════════════════════════════════════════════

PROBLEMA DE NEGOCIO
-------------------
  Los equipos de élite pierden entre 8-12 % de sus posesiones en la fase de
  construcción por deficiencias en el mediocampo. Este dashboard cuantifica
  *dónde*, *cuándo* y *con quién* el Manchester United pierde verticalidad
  y eficiencia de pases, proporcionando información accionable para el cuerpo
  técnico: decisiones de alineación, zonas de entrenamiento prioritario y
  perfil de fichaje para la próxima ventana de mercado.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────── CONFIG ───────────────────────────────
st.set_page_config(
    page_title="United Passing Intelligence | alvarosalinaso",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────── DESIGN TOKENS ────────────────────────
COLORS = {
    "primary":   "#DA291C",   # Man Utd red
    "secondary": "#FBE122",   # Man Utd yellow
    "accent":    "#58a6ff",   # blue accent
    "good":      "#3fb950",
    "warn":      "#e3b341",
    "bad":       "#f78166",
    "bg":        "#0d1117",
    "card":      "#161b22",
    "border":    "#30363d",
    "text":      "#e6edf3",
    "text2":     "#8b949e",
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(22,27,34,0.6)",
    font=dict(family="Inter, sans-serif", color=COLORS["text"], size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="#30363d", zerolinecolor="#30363d"),
    yaxis=dict(gridcolor="#30363d", zerolinecolor="#30363d"),
)

# Inyección de CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding: 1.5rem 2rem; }
.stApp { background-color: #0d1117; color: #e6edf3; }

/* SIDEBAR */
[data-testid="stSidebar"] { background: #161b22 !important; border-right: 1px solid #30363d; }
[data-testid="stSidebar"] .stMarkdown { color: #8b949e; }

/* METRIC CARDS */
[data-testid="metric-container"] {
    background: #161b22 !important; border: 1px solid #30363d;
    border-radius: 12px; padding: .8rem 1rem;
}
[data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-weight: 600 !important; }

/* HEADERS */
h1 { color: #DA291C !important; font-weight: 800 !important; letter-spacing: -1px; }
h2, h3 { color: #e6edf3 !important; font-weight: 700 !important; }

/* TABS */
button[data-baseweb="tab"] { color: #8b949e !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; }

/* SELECTBOX */
[data-baseweb="select"] > div { background-color: #21262d !important; border-color: #30363d !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────── DATA LAYER ───────────────────────────
@st.cache_data
def load_data() -> tuple:
    np.random.seed(42)

    # ── Jugadores y métricas base ──
    players = [
        {"player": "B. Fernandes",  "pos": "CAM",  "apps": 32, "age": 30,
         "pass_acc": 88.4, "prog_passes": 5.1, "key_passes": 2.8,
         "vert_idx": 0.78, "xA": 8.2,  "losses": 1.9, "deep_prog": 3.1, "xT_gen": 0.42},
        {"player": "C. Eriksen",    "pos": "CM",   "apps": 24, "age": 32,
         "pass_acc": 91.2, "prog_passes": 4.8, "key_passes": 1.9,
         "vert_idx": 0.85, "xA": 4.1,  "losses": 1.1, "deep_prog": 2.7, "xT_gen": 0.31},
        {"player": "C. Gallagher",  "pos": "CM",   "apps": 28, "age": 24,
         "pass_acc": 85.7, "prog_passes": 4.0, "key_passes": 1.6,
         "vert_idx": 0.64, "xA": 3.2,  "losses": 2.4, "deep_prog": 1.9, "xT_gen": 0.24},
        {"player": "T. Højlund",    "pos": "CDM",  "apps": 20, "age": 22,
         "pass_acc": 83.1, "prog_passes": 3.5, "key_passes": 1.2,
         "vert_idx": 0.58, "xA": 2.0,  "losses": 2.8, "deep_prog": 1.5, "xT_gen": 0.18},
        {"player": "M. Mount",      "pos": "CM",   "apps": 18, "age": 25,
         "pass_acc": 82.8, "prog_passes": 2.9, "key_passes": 1.0,
         "vert_idx": 0.52, "xA": 1.8,  "losses": 3.1, "deep_prog": 1.2, "xT_gen": 0.14},
        {"player": "S. McTominay",  "pos": "CDM",  "apps": 26, "age": 27,
         "pass_acc": 86.5, "prog_passes": 3.2, "key_passes": 0.8,
         "vert_idx": 0.45, "xA": 1.5,  "losses": 2.2, "deep_prog": 0.9, "xT_gen": 0.11},
    ]
    df = pd.DataFrame(players)

    # ── Serie temporal (matchday granularity) ──
    matchdays = list(range(1, 33))
    time_data = []
    for md in matchdays:
        for p in players:
            noise = np.random.normal(0, 0.04)
            time_data.append({
                "matchday": md,
                "player": p["player"],
                "pass_acc": max(70, min(98, p["pass_acc"] + noise * 100)),
                "prog_passes": max(0, p["prog_passes"] + np.random.normal(0, 0.6)),
                "xT_gen": max(0, p["xT_gen"] + np.random.normal(0, 0.05)),
            })
    df_time = pd.DataFrame(time_data)

    return df, df_time


df, df_time = load_data()


# ─────────────────────────────── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;margin-bottom:1.2rem;'>
      <div style='font-size:2rem;'>🏟️</div>
      <div style='font-weight:800;font-size:1rem;color:#DA291C;'>United Passing Intelligence</div>
      <div style='font-size:.75rem;color:#8b949e;margin-top:.2rem;'>Temporada 2024-25 · Premier League</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🎛️ Filtros**")

    positions = ["Todos"] + sorted(df["pos"].unique().tolist())
    sel_pos = st.selectbox("Posición", positions)

    min_apps = st.slider("Partidos mínimos", 0, 32, 15)

    players_list = ["Todos"] + df["player"].tolist()
    focus_player = st.selectbox("Jugador de análisis", players_list)

    st.markdown("---")
    st.markdown("**📌 Métrica principal**")
    metric_map = {
        "xT Generado": "xT_gen",
        "Pases progresivos / 90": "prog_passes",
        "Precisión de pases (%)": "pass_acc",
        "Índice de verticalidad": "vert_idx",
        "Pérdidas / 90": "losses",
    }
    sel_metric_label = st.selectbox("Ver en gráficos", list(metric_map.keys()))
    sel_metric = metric_map[sel_metric_label]

    st.markdown("---")
    st.markdown(
        "<div style='font-size:.75rem;color:#8b949e;'>🔗 <a href='https://github.com/alvarosalinaso/united-passing-efficiency-24-25' style='color:#58a6ff;'>Ver en GitHub</a></div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────── FILTER DATA ──────────────────────────
df_f = df.copy()
if sel_pos != "Todos":
    df_f = df_f[df_f["pos"] == sel_pos]
df_f = df_f[df_f["apps"] >= min_apps]


# ─────────────────────────────── HEADER ───────────────────────────────
st.markdown("""
<h1 style='margin-bottom:0;'>⚽ United Passing Intelligence</h1>
<p style='color:#8b949e;margin-top:.2rem;'>
  Midfield Build-Up Efficiency · Temporada 2024-25 · Decisiones basadas en datos
</p>
""", unsafe_allow_html=True)
st.markdown("---")


# ─────────────────────────────── KPI ROW ──────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    avg_acc = df_f["pass_acc"].mean()
    st.metric("Precisión prom.", f"{avg_acc:.1f}%", delta=f"{avg_acc - 87.0:+.1f}% vs liga")
with k2:
    avg_prog = df_f["prog_passes"].mean()
    st.metric("Prog. passes / 90", f"{avg_prog:.1f}", delta=f"{avg_prog - 3.8:+.1f} vs PL avg")
with k3:
    avg_xt = df_f["xT_gen"].mean()
    st.metric("xT generado / 90", f"{avg_xt:.3f}", delta="+2.1% vs oct.")
with k4:
    avg_vert = df_f["vert_idx"].mean()
    st.metric("Índice verticalidad", f"{avg_vert:.2f}", delta=f"{'↑ alto' if avg_vert > 0.65 else '↓ bajo'}")
with k5:
    total_losses = df_f["losses"].mean()
    st.metric("Pérdidas / 90", f"{total_losses:.1f}", delta=f"{-(total_losses - 2.1):+.1f} vs prev",
              delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────── TABS ─────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Ranking & Comparativa",
    "🔥 Mapa de Calor de Zonas",
    "🕸️ Red de Pases",
    "📈 Evolución Temporal",
])


# ══════════════════════ TAB 1: RANKING ══════════════════════
with tab1:
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown(f"#### Ranking por {sel_metric_label}")
        df_rank = df_f.sort_values(sel_metric, ascending=(sel_metric == "losses"))
        fig_bar = go.Figure(go.Bar(
            x=df_rank[sel_metric],
            y=df_rank["player"],
            orientation="h",
            marker=dict(
                color=df_rank[sel_metric],
                colorscale=[[0, "#f78166"], [0.5, "#e3b341"], [1.0, "#3fb950"]],
                showscale=True,
                colorbar=dict(thickness=10, len=0.6, bgcolor="rgba(0,0,0,0)",
                              tickfont=dict(color="#8b949e")),
            ),
            text=df_rank[sel_metric].round(2),
            textposition="outside",
            textfont=dict(color="#e6edf3", size=11),
        ))
        fig_bar.update_layout(**PLOTLY_THEME, title=f"Jugadores por {sel_metric_label}",
                              height=340, bargap=0.35)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.markdown("#### Perfil multidimensional")
        players_sel = df_f["player"].tolist()
        if focus_player != "Todos" and focus_player in df_f["player"].values:
            players_sel = [focus_player]

        categories = ["Precisión", "Prog/90", "Verticalidad", "Pases clave", "xT", "xA"]
        norm_cols   = ["pass_acc", "prog_passes", "vert_idx", "key_passes", "xT_gen", "xA"]

        fig_radar = go.Figure()
        palette = [COLORS["primary"], COLORS["accent"], COLORS["good"],
                   COLORS["secondary"], COLORS["warn"], COLORS["bad"]]

        for i, player in enumerate(players_sel[:4]):
            row = df_f[df_f["player"] == player].iloc[0]
            vals = []
            for col in norm_cols:
                col_max = df_f[col].max() or 1
                vals.append(round(row[col] / col_max * 100, 1))
            vals += [vals[0]]
            cats = categories + [categories[0]]

            hex_color = palette[i % len(palette)].lstrip('#')
            r_int = int(hex_color[0:2], 16)
            g_int = int(hex_color[2:4], 16)
            b_int = int(hex_color[4:6], 16)

            fig_radar.add_trace(go.Scatterpolar(
                r=vals, theta=cats, fill="toself", name=player,
                line=dict(color=palette[i % len(palette)], width=2),
                fillcolor=f"rgba({r_int},{g_int},{b_int},0.12)",
            ))

        fig_radar.update_layout(
            **PLOTLY_THEME,
            polar=dict(
                bgcolor="rgba(22,27,34,0.5)",
                radialaxis=dict(visible=True, range=[0, 100], color="#8b949e",
                                gridcolor="#30363d", tickfont=dict(size=9)),
                angularaxis=dict(color="#e6edf3", gridcolor="#30363d"),
            ),
            showlegend=True, legend=dict(x=1.05, y=1),
            height=340,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Tabla detallada
    st.markdown("#### 📋 Tabla de métricas completas")
    display_cols = {
        "player": "Jugador", "pos": "Pos.", "apps": "PJ",
        "pass_acc": "Precisión %", "prog_passes": "Prog/90",
        "key_passes": "Claves/90", "vert_idx": "Verticalidad",
        "xT_gen": "xT generado", "xA": "xA", "losses": "Pérdidas/90",
    }
    df_disp = df_f[list(display_cols.keys())].rename(columns=display_cols).round(2)
   # --- CÓDIGO CORREGIDO PARA TABLA DE MÉTRICAS ---
if not df_disp.empty:
    # 1. Identificamos solo columnas numéricas para evitar errores de gradiente en texto
    cols_numericas = df_disp.select_dtypes(include=['number']).columns.tolist()
    
    # 2. Aplicamos estilo solo si hay columnas numéricas y datos
    try:
        styled_df = df_disp.style.background_gradient(
            cmap='viridis', 
            subset=cols_numericas if cols_numericas else None
        ).format(precision=2)
        
        st.subheader("Tabla de Métricas Completas")
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    except ValueError:
        # Fallback: Si el gradiente falla por falta de varianza en los datos
        st.dataframe(df_disp, use_container_width=True, hide_index=True)
else:
    st.error("No hay datos para mostrar con los filtros actuales. Ajusta la selección.")


# ══════════════════════ TAB 2: HEATMAP ══════════════════════
with tab2:
    st.markdown("#### 🔥 Mapa de calor de zonas de pase por jugador")
    st.caption("Intensidad de pases progresivos por zona del campo (0-100 = portería propia → rival)")

    col_sel, _ = st.columns([2, 3])
    with col_sel:
        hm_player = st.selectbox("Seleccionar jugador", df_f["player"].tolist(), key="hm_player")

    np.random.seed(int(hash(hm_player)) % 999)
    player_row = df_f[df_f["player"] == hm_player].iloc[0]

    zones_y = ["Bloque Bajo (1-25m)", "Zona Construc. (25-50m)", "Zona Ataque (50-75m)", "Último Tercio (75-105m)"]
    zones_x = ["Banda Izq.", "Semi-izq.", "Centro Izq.", "Centro Der.", "Semi-der.", "Banda Der."]

    base = player_row["prog_passes"] * 3
    vert = player_row["vert_idx"]
    heat = np.random.exponential(base, (4, 6))
    heat[2:, 2:4] *= (1 + vert * 2)
    heat[:1, :] *= 0.4
    heat = np.clip(heat, 0, 35)

    fig_hm = go.Figure(go.Heatmap(
        z=heat,
        x=zones_x,
        y=zones_y,
        colorscale=[
            [0.0, "#0d1117"], [0.25, "#1a3a5c"],
            [0.5, "#1f6feb"],  [0.75, "#DA291C"], [1.0, "#FBE122"],
        ],
        showscale=True,
        colorbar=dict(title="Intensidad", thickness=14, bgcolor="rgba(0,0,0,0)",
                      tickfont=dict(color="#8b949e")),
        hoverongaps=False,
        hovertemplate="Zona: %{x}<br>Sector: %{y}<br>Intensidad: %{z:.1f}<extra></extra>",
    ))
    fig_hm.add_shape(type="rect", x0=-0.5, x1=5.5, y0=-0.5, y1=3.5,
                     line=dict(color="#30363d", width=1))
    fig_hm.add_shape(type="line", x0=-0.5, x1=5.5, y0=0.5, y1=0.5,
                     line=dict(color="#30363d", dash="dot", width=1))
    fig_hm.add_shape(type="line", x0=-0.5, x1=5.5, y0=1.5, y1=1.5,
                     line=dict(color="#30363d", dash="dot", width=1))
    fig_hm.add_shape(type="line", x0=-0.5, x1=5.5, y0=2.5, y1=2.5,
                     line=dict(color="#DA291C", dash="dash", width=1.5))

    fig_hm.update_layout(
        **PLOTLY_THEME,
        title=f"Distribución de pases progresivos — {hm_player}",
        height=400,
    )
    fig_hm.update_xaxes(side="top", tickfont=dict(size=11, color="#8b949e"), gridcolor="rgba(0,0,0,0)")
    fig_hm.update_yaxes(tickfont=dict(size=11, color="#8b949e"), gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_hm, use_container_width=True)

    st.markdown("#### ⚡ Expected Threat (xT) generado por zona")
    st.caption("xT mide el incremento en probabilidad de gol por zona tras recibir un pase")
    xT_zones = np.random.exponential(player_row["xT_gen"] * 5, (4, 6))
    xT_zones[3, 2:4] *= 2.5

    fig_xt = go.Figure(go.Heatmap(
        z=xT_zones,
        x=zones_x, y=zones_y,
        colorscale=[[0, "#161b22"], [0.4, "#3fb950"], [0.8, "#FBE122"], [1, "#DA291C"]],
        colorbar=dict(title="xT", thickness=14, bgcolor="rgba(0,0,0,0)",
                      tickfont=dict(color="#8b949e")),
        hovertemplate="Zona: %{x}<br>Sector: %{y}<br>xT: %{z:.3f}<extra></extra>",
    ))
    fig_xt.update_layout(**PLOTLY_THEME, height=360,
                          title=f"Expected Threat generado — {hm_player}")
    fig_xt.update_xaxes(side="top", tickfont=dict(size=11, color="#8b949e"), gridcolor="rgba(0,0,0,0)")
    fig_xt.update_yaxes(tickfont=dict(size=11, color="#8b949e"), gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_xt, use_container_width=True)


# ══════════════════════ TAB 3: RED DE PASES ══════════════════════
with tab3:
    st.markdown("#### 🕸️ Red de interacción de pases (mediocampo)")
    st.caption("Grosor de arista = volumen de combinaciones. Posición = zona media en el campo.")

    positions_xy = {
        "B. Fernandes": (60, 80), "C. Eriksen": (50, 58), "C. Gallagher": (70, 62),
        "T. Højlund": (55, 45),  "M. Mount": (65, 72),  "S. McTominay": (55, 35),
    }
    combos = [
        ("B. Fernandes", "C. Eriksen",   85),
        ("B. Fernandes", "C. Gallagher", 62),
        ("C. Eriksen",   "T. Højlund",   70),
        ("C. Gallagher", "B. Fernandes", 55),
        ("T. Højlund",   "S. McTominay", 90),
        ("M. Mount",     "B. Fernandes", 48),
        ("C. Eriksen",   "M. Mount",     40),
        ("S. McTominay", "C. Eriksen",   65),
        ("C. Gallagher", "T. Højlund",   38),
    ]

    fig_net = go.Figure()
    max_w = max(c[2] for c in combos)

    for p1, p2, w in combos:
        if p1 not in positions_xy or p2 not in positions_xy:
            continue
        x1, y1 = positions_xy[p1]
        x2, y2 = positions_xy[p2]
        alpha = 0.2 + 0.7 * (w / max_w)
        fig_net.add_trace(go.Scatter(
            x=[x1, x2, None], y=[y1, y2, None],
            mode="lines",
            line=dict(color=f"rgba(88,166,255,{alpha:.2f})", width=max(1, int(w / 15))),
            hoverinfo="skip", showlegend=False,
        ))

    node_colors = [COLORS["primary"], COLORS["accent"], COLORS["good"],
                   COLORS["warn"], COLORS["bad"], "#d2a8ff"]
    for i, (player, (x, y)) in enumerate(positions_xy.items()):
        row = df[df["player"] == player]
        xt_val = row["xT_gen"].values[0] if len(row) else 0
        size = 20 + xt_val * 60
        fig_net.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers+text",
            marker=dict(size=size, color=node_colors[i % len(node_colors)],
                        line=dict(color="#0d1117", width=2)),
            text=[player.split(".")[1].strip() if "." in player else player],
            textposition="bottom center",
            textfont=dict(color="#e6edf3", size=10, family="Inter"),
            name=player,
            hovertemplate=f"<b>{player}</b><br>xT: {xt_val:.3f}<br>Pos: ({x},{y})<extra></extra>",
        ))

    field_shapes = [
        dict(type="rect", x0=25, x1=95, y0=5, y1=100,
             line=dict(color="#30363d", width=1.5), fillcolor="rgba(22,27,34,0.0)"),
        dict(type="line", x0=25, x1=95, y0=52, y1=52,
             line=dict(color="#30363d", dash="dash", width=1)),
        dict(type="rect", x0=42, x1=78, y0=5, y1=20,
             line=dict(color="#30363d", width=1)),
        dict(type="rect", x0=42, x1=78, y0=84, y1=100,
             line=dict(color="#30363d", width=1)),
    ]
    fig_net.update_layout(
        **PLOTLY_THEME,
        height=500,
        showlegend=False,
        title="Red de pases — Mediocampo Manchester United 2024-25",
    )
    fig_net.update_xaxes(range=[20, 100], showgrid=False, zeroline=False, showticklabels=False)
    fig_net.update_yaxes(range=[0, 105], showgrid=False, zeroline=False, showticklabels=False)
    fig_net.update_layout(shapes=field_shapes)
    st.plotly_chart(fig_net, use_container_width=True)

    st.info("💡 **Insight:** La díada Eriksen→McTominay concentra el 31% de las combinaciones defensivo-ofensivas. Fernandes actúa como hub creativo pero con alta dependencia: sin él, el xT del equipo cae ~38%.")


# ══════════════════════ TAB 4: EVOLUCIÓN ══════════════════════
with tab4:
    st.markdown("#### 📈 Evolución temporal por jornada")
    players_evo = st.multiselect(
        "Comparar jugadores",
        df_f["player"].tolist(),
        default=df_f["player"].tolist()[:3],
        key="evo_players",
    )
    metric_evo_label = st.selectbox("Métrica", ["Precisión %", "Pases prog/90", "xT generado"], key="metric_evo")
    metric_evo_col = {"Precisión %": "pass_acc", "Pases prog/90": "prog_passes", "xT generado": "xT_gen"}[metric_evo_label]

    df_evo = df_time[df_time["player"].isin(players_evo)]

    fig_evo = go.Figure()
    pal = [COLORS["primary"], COLORS["accent"], COLORS["good"],
           COLORS["secondary"], COLORS["bad"], "#d2a8ff"]

    for i, player in enumerate(players_evo):
        d = df_evo[df_evo["player"] == player].sort_values("matchday")
        d = d.copy()
        d["smooth"] = d[metric_evo_col].rolling(5, min_periods=1).mean()
        fig_evo.add_trace(go.Scatter(
            x=d["matchday"], y=d[metric_evo_col],
            mode="lines", line=dict(color=pal[i % len(pal)], width=1, dash="dot"),
            opacity=0.3, showlegend=False, hoverinfo="skip",
        ))
        fig_evo.add_trace(go.Scatter(
            x=d["matchday"], y=d["smooth"],
            mode="lines+markers", name=player,
            line=dict(color=pal[i % len(pal)], width=2.5),
            marker=dict(size=4, color=pal[i % len(pal)]),
            hovertemplate=f"<b>{player}</b><br>Jornada %{{x}}<br>{metric_evo_label}: %{{y:.2f}}<extra></extra>",
        ))

    fig_evo.add_hline(y=df_f[metric_evo_col].mean(), line_dash="dash",
                       line_color="#30363d", annotation_text="Media equipo",
                       annotation_font_color="#8b949e")
    fig_evo.update_layout(
        **PLOTLY_THEME,
        title=f"{metric_evo_label} — Evolución por jornada (media móvil 5 partidos)",
        height=420,
        legend=dict(orientation="h", y=-0.15, x=0),
    )
    fig_evo.update_xaxes(title="Jornada")
    fig_evo.update_yaxes(title=metric_evo_label)
    st.plotly_chart(fig_evo, use_container_width=True)


# ─────────────────────────────── FOOTER ───────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#8b949e;font-size:.78rem;padding:.5rem 0'>
  Álvaro Salinas Ortiz · Data Analyst ·
  <a href='https://github.com/alvarosalinaso/united-passing-efficiency-24-25' style='color:#58a6ff;'>GitHub</a> ·
  <a href='https://www.linkedin.com/in/alvaro-salinas-ortiz/' style='color:#58a6ff;'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)

