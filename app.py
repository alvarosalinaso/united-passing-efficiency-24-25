import streamlit as st

# Modulos internos (Clean Architecture)
from src.streamlit.dashboard_data import load_streamlit_data
from src.streamlit.dashboard_plots import (
    graficar_ranking,
    graficar_radar,
    graficar_heatmap_zonas,
    graficar_heatmap_xt,
    graficar_red_pases,
    graficar_evolucion
)

# ─────────────────────────────── CONFIG ───────────────────────────────
st.set_page_config(
    page_title="United Passing Intelligence | alvarosalinaso",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding: 1.5rem 2rem; }
.stApp { background-color: #0d1117; color: #e6edf3; }

/* SIDEBAR & METRICS */
[data-testid="stSidebar"] { background: #161b22 !important; border-right: 1px solid #30363d; }
[data-testid="metric-container"] { background: #161b22 !important; border: 1px solid #30363d; border-radius: 12px; padding: .8rem 1rem; }
[data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-weight: 600 !important; }

/* Text */
h1 { color: #DA291C !important; font-weight: 800 !important; letter-spacing: -1px; }
button[data-baseweb="tab"][aria-selected="true"] { color: #58a6ff !important; border-bottom-color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────── DATA LAYER ───────────────────────────
df, df_time, kpis = load_streamlit_data()

# ─────────────────────────────── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;margin-bottom:1.2rem;'>
      <div style='font-size:2rem;'>🏟️</div>
      <div style='font-weight:800;font-size:1rem;color:#DA291C;'>United Passing Intelligence</div>
      <div style='font-size:.75rem;color:#8b949e;margin-top:.2rem;'>Temporada 2024-25 · Premier League</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("**🎛️ Filtros**")
    sel_pos = st.selectbox("Posición", ["Todos"] + sorted(df["pos"].unique().tolist()))
    min_apps = st.slider("Partidos mínimos", 0, 32, 15)
    focus_player = st.selectbox("Jugador de análisis", ["Todos"] + df["player"].tolist())

    st.markdown("---")
    st.markdown("**📌 Métrica principal**")
    metric_map = {
        "xT Generado": "xT_gen", "Pases progresivos / 90": "prog_passes",
        "Precisión de pases (%)": "pass_acc", "Índice de verticalidad": "vert_idx",
        "Pérdidas / 90": "losses"
    }
    sel_metric_label = st.selectbox("Ver en gráficos", list(metric_map.keys()))
    sel_metric = metric_map[sel_metric_label]

    st.markdown("---")
    st.markdown("<div style='font-size:.75rem;color:#8b949e;'>🔗 <a href='https://github.com/alvarosalinaso/united-passing-efficiency-24-25' style='color:#58a6ff;'>Ver en GitHub</a></div>", unsafe_allow_html=True)

# ─────────────────────────────── FILTER ───────────────────────────────
df_f = df.copy()
if sel_pos != "Todos":
    df_f = df_f[df_f["pos"] == sel_pos]
df_f = df_f[df_f["apps"] >= min_apps]

# ─────────────────────────────── HEADER ───────────────────────────────
st.markdown("<h1 style='margin-bottom:0;'>⚽ United Passing Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e;margin-top:.2rem;'>Midfield Build-Up Efficiency · Temporada 2024-25 · Decisiones basadas en datos</p><hr>", unsafe_allow_html=True)

# ─────────────────────────────── KPI ROW ──────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Precisión prom.", f"{df_f['pass_acc'].mean():.1f}%", delta=f"{df_f['pass_acc'].mean() - 87.0:+.1f}% vs liga")
k2.metric("Prog. passes / 90", f"{df_f['prog_passes'].mean():.1f}", delta=f"{df_f['prog_passes'].mean() - 3.8:+.1f} vs avg")
k3.metric("xT generado / 90", f"{df_f['xT_gen'].mean():.3f}", delta="+2.1% vs prev")
avg_vert = df_f['vert_idx'].mean()
k4.metric("Índice verticalidad", f"{avg_vert:.2f}", delta=f"{'↑ alto' if avg_vert > 0.65 else '↓ bajo'}")
total_losses = df_f["losses"].mean()
k5.metric("Pérdidas / 90", f"{total_losses:.1f}", delta=f"{-(total_losses - 2.1):+.1f} vs prev", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)
st.info("ℹ️ **Sobre estas métricas:** El *xT (Expected Threat)* mide cuánto aumenta la probabilidad estadística de marcar gol tras un pase. Los *Pases progresivos* son aquellos que acercan significativamente el balón a la portería rival (+10m en campo rival). El *Índice de verticalidad* relaciona los pases directos hacia adelante vs pases de seguridad laterales/atrás.")

# ─────────────────────────────── TABS ─────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking & Comparativa", "🔥 Mapa de Calor de Zonas", "🕸️ Red de Pases", "📈 Evolución Temporal"])

# ══════════════════════ TAB 1: RANKING ══════════════════════
with tab1:
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown(f"#### Ranking por {sel_metric_label}")
        df_rank = df_f.sort_values(sel_metric, ascending=(sel_metric == "losses"))
        st.plotly_chart(graficar_ranking(df_rank, sel_metric, sel_metric_label), use_container_width=True)

    with col_r:
        st.markdown("#### Perfil multidimensional")
        st.plotly_chart(graficar_radar(df_f, focus_player), use_container_width=True)

    # Tabla detallada
    st.markdown("#### 📋 Tabla de métricas completas")
    display_cols = {"player": "Jugador", "pos": "Pos.", "apps": "PJ", "pass_acc": "Precisión %", "prog_passes": "Prog/90", "key_passes": "Claves/90", "vert_idx": "Verticalidad", "xT_gen": "xT generado", "xA": "xA", "losses": "Pérdidas/90"}
    df_disp = df_f[list(display_cols.keys())].rename(columns=display_cols).round(2)
    
    if not df_disp.empty:
        cols_numericas = df_disp.select_dtypes(include=['number']).columns.tolist()
        try:
            styled_df = df_disp.style.background_gradient(cmap='viridis', subset=cols_numericas if cols_numericas else None).format(precision=2)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        except ValueError:
            st.dataframe(df_disp, use_container_width=True, hide_index=True)
    else:
        st.error("No hay datos para mostrar con los filtros actuales.")

# ══════════════════════ TAB 2: HEATMAP ══════════════════════
with tab2:
    st.markdown("#### 🔥 Mapa de calor de zonas de pase y xT")
    col_sel, _ = st.columns([2, 3])
    hm_player = col_sel.selectbox("Seleccionar jugador", df_f["player"].tolist(), key="hm_player")
    player_row = df_f[df_f["player"] == hm_player].iloc[0]

    h1, h2 = st.columns(2)
    with h1:
        st.plotly_chart(graficar_heatmap_zonas(player_row), use_container_width=True)
    with h2:
        st.plotly_chart(graficar_heatmap_xt(player_row), use_container_width=True)

# ══════════════════════ TAB 3: RED DE PASES ══════════════════════
with tab3:
    st.markdown("#### 🕸️ Red de interacción de pases (mediocampo)")
    st.plotly_chart(graficar_red_pases(df), use_container_width=True)
    with st.expander("🕸️ ¿Cómo interpretar la Red de Pases?"):
        st.markdown("*   **Nodos (Círculos):** Diámetro señala la responsabilidad de peligro (`xT`).\n*   **Aristas (Líneas):** Grosor simboliza volumen de pases exitosos completados.")

# ══════════════════════ TAB 4: EVOLUCIÓN ══════════════════════
with tab4:
    st.markdown("#### 📈 Evolución temporal por jornada")
    players_evo = st.multiselect("Comparar jugadores", df_f["player"].tolist(), default=df_f["player"].tolist()[:2], key="evo_players")
    mevo_label = st.selectbox("Métrica", ["Precisión %", "Pases prog/90", "xT generado"], key="metric_evo")
    mevo_col = {"Precisión %": "pass_acc", "Pases prog/90": "prog_passes", "xT generado": "xT_gen"}[mevo_label]
    
    if players_evo:
        st.plotly_chart(graficar_evolucion(df_time, df_f, players_evo, mevo_col, mevo_label), use_container_width=True)
