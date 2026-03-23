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
[data-testid="metric-container"] { background: #161b22 !important; border: 1px solid #30363d; border-radius: 12px; padding: 1rem; }
[data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-weight: 600 !important; }

/* Text & Sections */
h1 { color: #DA291C !important; font-weight: 800 !important; letter-spacing: -1px; }
.section-header {
    font-weight: 800;
    font-size: 1.8rem;
    color: #DA291C;
    margin-top: 3rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #30363d;
    padding-bottom: 0.5rem;
}
.section-text { font-size: 1.05rem; color: #8b949e; margin-bottom: 1.5rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────── DATA LAYER ───────────────────────────
df, df_time, kpis = load_streamlit_data()

# ─────────────────────────────── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;margin-bottom:1.2rem;'>
      <div style='font-size:3rem;'>🏟️</div>
      <div style='font-weight:800;font-size:1.2rem;color:#DA291C;'>United Passing Intelligence</div>
      <div style='font-size:.8rem;color:#8b949e;margin-top:.2rem;'>Temporada 2024-25 · Premier League</div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("**🎛️ Filtros Globales**")
    sel_pos = st.selectbox("Posición Táctica", ["Todos"] + sorted(df["pos"].unique().tolist()))
    min_apps = st.slider("Partidos Mínimos Jugados", 0, 32, 15)
    focus_player = st.selectbox("Jugador en Foco (Radares)", ["Todos"] + df["player"].unique().tolist())

    st.markdown("---")
    st.markdown("**⚔️ Contexto Opositor (Filtro Senior)**")
    sel_context = st.radio("Nivel de Presión Rival", ["Resto PL", "Top 6 (Alta Presión)"], help="Audita qué jugador 'infla' sus estadísticas frente a equipos de baja tabal y quién sobrevive a la presión asfixiante de la élite de Inglaterra.")

    st.markdown("---")
    st.markdown("**📌 Métrica de Enfoque Principal**")
    metric_map = {
        "xT Generado (Ameaza Esperada)": "xT_gen", "Pases Progresivos / 90": "prog_passes",
        "Precisión de pases (%)": "pass_acc", "Índice de Verticalidad": "vert_idx",
        "Pérdidas / 90": "losses"
    }
    sel_metric_label = st.selectbox("Seleccionar", list(metric_map.keys()))
    sel_metric = metric_map[sel_metric_label]

# ─────────────────────────────── FILTER ───────────────────────────────
df_f = df.copy()

# 1. Filtro Contextual (Crucial para el análisis Senior)
target_tier = sel_context.replace(" (Alta Presión)", "")
df_f = df_f[df_f["opponent_tier"] == target_tier]

if sel_pos != "Todos":
    df_f = df_f[df_f["pos"] == sel_pos]
df_f = df_f[df_f["apps"] >= min_apps]

# ─────────────────────────────── HERO SECTION ───────────────────────────────
st.markdown("<h1 style='margin-bottom:0;'>⚽ Manchester United: Midfield Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.1rem; color:#8b949e; margin-top:.2rem;'>Un análisis interactivo del comportamiento en la construcción de juego durante la temporada 2024-25. Evalúa qué mediocampistas rompen líneas, quiénes retienen la posesión, y cómo fluye el balón en Old Trafford.</p><hr>", unsafe_allow_html=True)

# KPI ROW
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Precisión Promedio", f"{df_f['pass_acc'].mean():.1f}%", delta=f"{df_f['pass_acc'].mean() - 87.0:+.1f}% vs liga")
k2.metric("Prog. Passes / 90", f"{df_f['prog_passes'].mean():.1f}", delta=f"{df_f['prog_passes'].mean() - 3.8:+.1f} vs avg")
k3.metric("xT Promedio / 90", f"{df_f['xT_gen'].mean():.3f}", delta="+2.1% vs prev")
avg_vert = df_f['vert_idx'].mean()
k4.metric("Índice Vertical", f"{avg_vert:.2f}", delta=f"{'↑ alto' if avg_vert > 0.65 else '↓ bajo'}")
total_losses = df_f["losses"].mean()
k5.metric("Pérdidas / 90", f"{total_losses:.1f}", delta=f"{-(total_losses - 2.1):+.1f} vs prev", delta_color="inverse")

st.info("💡 **Metodología Avanzada:** El **xT (Expected Threat)** cuantifica cuánto aumenta la probabilidad de que el United anote un gol producto directo de la zona a la que el jugador envía el pase. El **Índice de Verticalidad** castiga los pases horizontales de seguridad, premiando a los jugadores que asumen riesgos hacia el área rival.")

# ─────────────────────────────── SECCIÓN 1 ───────────────────────────────
st.markdown("<div class='section-header'>1. Rankings y Perfiles Multidimensionales 📊</div>", unsafe_allow_html=True)
st.markdown("<div class='section-text'>Todo análisis comienza aislando a los líderes estadísticos. Compara lado a lado cómo la plantilla rinde en la métrica seleccionada en el menú lateral, y evalúa el polígono de rendimiento completo del jugador en foco frente al resto de sus compañeros.</div>", unsafe_allow_html=True)

col_l, col_r = st.columns([3, 2])
with col_l:
    df_rank = df_f.sort_values(sel_metric, ascending=(sel_metric == "losses"))
    st.plotly_chart(graficar_ranking(df_rank, sel_metric, sel_metric_label), use_container_width=True)

with col_r:
    st.plotly_chart(graficar_radar(df_f, focus_player), use_container_width=True)

with st.expander("Ver tabla completa de datos consolidados"):
    display_cols = {"player": "Jugador", "pos": "Pos.", "apps": "PJ", "pass_acc": "Precisión %", "prog_passes": "Prog/90", "key_passes": "Claves/90", "vert_idx": "Verticalidad", "xT_gen": "xT generado", "xA": "xA", "losses": "Pérdidas/90"}
    df_disp = df_f[list(display_cols.keys())].rename(columns=display_cols).round(2)
    if not df_disp.empty:
        cols_numericas = df_disp.select_dtypes(include=['number']).columns.tolist()
        try:
            styled_df = df_disp.style.background_gradient(cmap='viridis', subset=cols_numericas if cols_numericas else None).format(precision=2)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        except ValueError:
            st.dataframe(df_disp, use_container_width=True, hide_index=True)

# ─────────────────────────────── SECCIÓN 2 ───────────────────────────────
st.markdown("<div class='section-header'>2. Radiografía Táctica Funcional 🔥</div>", unsafe_allow_html=True)
st.markdown("<div class='section-text'>El fútbol no se juega en una hoja de Excel, sino en el césped. Aisla a un jugador para observar empíricamente en qué zonas específicas del campo ejecuta sus entregas de balón (izquierda) y en qué cuadrantes genera el mayor grado de amenaza xT contra el arco rival (derecha).</div>", unsafe_allow_html=True)

col_sel, _ = st.columns([2, 5])
hm_player = col_sel.selectbox("Filtrar jugador para los mapas de calor tácticos", df_f["player"].unique().tolist(), key="hm_player")
player_row = df_f[df_f["player"] == hm_player].iloc[0]

h1, h2 = st.columns(2)
with h1:
    st.plotly_chart(graficar_heatmap_zonas(player_row), use_container_width=True)
with h2:
    st.plotly_chart(graficar_heatmap_xt(player_row), use_container_width=True)

# ─────────────────────────────── SECCIÓN 3 ───────────────────────────────
st.markdown("<div class='section-header'>3. Red de Asociaciones en el Campo 🕸️</div>", unsafe_allow_html=True)
st.markdown("<div class='section-text'>La fortaleza de un mediocampo radica en sus triángulos de asociación. Observa el flujo microscópico de la pelota entre nuestras figuras. <b>El grosor del cable</b> señala el colosal volumen de pases exitosos completados entre ambos jugadores. <b>El tamaño del nodo</b> de cada jugador simboliza su contribución directa de xT en cada toque.</div>", unsafe_allow_html=True)

st.plotly_chart(graficar_red_pases(df), use_container_width=True)

# ─────────────────────────────── SECCIÓN 4 ───────────────────────────────
st.markdown("<div class='section-header'>4. Consistencia y Evolución a lo largo de la Premier League 📈</div>", unsafe_allow_html=True)
st.markdown("<div class='section-text'>Incluso las mayores estrellas sufren caídas de rendimiento. Compara a tus jugadores favoritos a lo largo de todos los partidos de la temporada usando una <b>Media Móvil de 5 Jornadas</b> que purga el ruido y clarifica la genuina curva de forma de los jugadores. Selecciona libremente qué métrica temporal contrastar.</div>", unsafe_allow_html=True)

ec1, ec2, _ = st.columns([2, 2, 6])
with ec1:
    players_evo = st.multiselect("Vincular jugadores a comparar", df_f["player"].tolist(), default=df_f["player"].tolist()[:2], key="evo_players")
with ec2:
    mevo_label = st.selectbox("Seleccionar Métrica a medir", ["Precisión %", "Pases prog/90", "xT generado"], key="metric_evo")
    
mevo_col = {"Precisión %": "pass_acc", "Pases prog/90": "prog_passes", "xT generado": "xT_gen"}[mevo_label]

if players_evo:
    st.plotly_chart(graficar_evolucion(df_time, df_f, players_evo, mevo_col, mevo_label), use_container_width=True)
else:
    st.warning("Selecciona al menos un jugador para graficar su curva de evolución.")
