import streamlit as st
from src.streamlit.dashboard_data import load_streamlit_data
from src.streamlit.dashboard_plots import graficar_ranking, graficar_radar, graficar_heatmap_zonas, graficar_heatmap_xt, graficar_red_pases, graficar_evolucion

st.set_page_config(page_title="United Passing Data", page_icon="🏟️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0d1117; color: #e6edf3; }
[data-testid="metric-container"] { background: #161b22 !important; border: 1px solid #30363d; border-radius: 8px; padding: 1rem; }
[data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: 800 !important; }
.section-header { font-weight: 800; font-size: 1.8rem; color: #DA291C; margin-top: 3rem; border-bottom: 1px solid #30363d; padding-bottom: 0.5rem; }
.section-text { font-size: 1.05rem; color: #8b949e; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

df_all, df_t, k_dict = load_streamlit_data()

with st.sidebar:
    st.markdown("<h2 style='color:#DA291C;text-align:center;'>United Passing Stats</h2><hr>", unsafe_allow_html=True)

    pos_filter = st.selectbox("Posición", ["Todos"] + sorted(df_all["pos"].unique().tolist()))
    min_games = st.slider("Min Partidos", 0, 32, 15)
    f_player = st.selectbox("Foco (Radar)", ["Todos"] + df_all["player"].unique().tolist())
    
    st.markdown("---")
    opp_tier = st.radio("Dificultad de Partido", ["Resto PL", "Top 6"])
    
    st.markdown("---")
    m_map = {"xT Generado": "xT_gen", "Pases Prog": "prog_passes", "Precisión": "pass_acc", "Verticalidad": "vert_idx", "Pérdidas": "losses"}
    target_stat = st.selectbox("Métrica Foco", list(m_map.keys()))
    sel_var = m_map[target_stat]

# filtro core
cur_val = opp_tier.replace("Top 6", "Top 6")
df_work = df_all[df_all["opponent_tier"] == cur_val].copy()

if pos_filter != "Todos": df_work = df_work[df_work["pos"] == pos_filter]
df_work = df_work[df_work["apps"] >= min_games]

st.title("⚽ United: Analytics de Plantilla Completa")
st.markdown("Métricas transaccionales de toda la plantilla de Old Trafford. Análisis duro sin fanatismos.")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Acc%", f"{df_work['pass_acc'].mean():.1f}%")
c2.metric("ProgP/90", f"{df_work['prog_passes'].mean():.1f}")
c3.metric("xT/90", f"{df_work['xT_gen'].mean():.3f}")
c4.metric("Índice Vert", f"{df_work['vert_idx'].mean():.2f}")
c5.metric("Pérdidas/90", f"{df_work['losses'].mean():.1f}", delta_color="inverse")

st.markdown("<div class='section-header'>1. Leaderboards</div>", unsafe_allow_html=True)
ca, cb = st.columns([3, 2])
with ca:
    r_df = df_work.sort_values(sel_var, ascending=(sel_var == "losses"))
    st.plotly_chart(graficar_ranking(r_df, sel_var, target_stat), use_container_width=True)
with cb: st.plotly_chart(graficar_radar(df_work, f_player), use_container_width=True)

with st.expander("Tabla Raw"):
    cols = {"player": "Jugador", "pos": "Pos", "apps": "PJ", "pass_acc": "Acc%", "prog_passes": "Prog/90", "vert_idx": "Vert", "xT_gen": "xT", "losses": "Pérdidas"}
    disp = df_work[list(cols.keys())].rename(columns=cols).round(2)
    st.dataframe(disp.style.background_gradient(cmap='viridis', subset=disp.select_dtypes('number').columns).format(precision=2), use_container_width=True, hide_index=True)

st.markdown("<div class='section-header'>2. Zonas de Amenaza (xT)</div>", unsafe_allow_html=True)
p_sel = st.selectbox("Jugador para heatmap táctico", df_work["player"].unique().tolist())
p_row = df_work[df_work["player"] == p_sel].iloc[0]

h1, h2 = st.columns(2)
with h1: st.plotly_chart(graficar_heatmap_zonas(p_row), use_container_width=True)
with h2: st.plotly_chart(graficar_heatmap_xt(p_row), use_container_width=True)

st.markdown("<div class='section-header'>3. Red de Flujo</div>", unsafe_allow_html=True)
st.plotly_chart(graficar_red_pases(df_all), use_container_width=True)

st.markdown("<div class='section-header'>4. Tracking Estacional</div>", unsafe_allow_html=True)
tr_c1, tr_c2 = st.columns([1,1])
with tr_c1: p_track = st.multiselect("Benchmark jugadores", df_work["player"].tolist(), default=df_work["player"].tolist()[:2])
with tr_c2: m_track_lb = st.selectbox("Benchmark Métrica", ["Precisión", "Pases Prog", "xT generado"])

m_track_col = {"Precisión": "pass_acc", "Pases Prog": "prog_passes", "xT generado": "xT_gen"}[m_track_lb]
if p_track: st.plotly_chart(graficar_evolucion(df_t, df_work, p_track, m_track_col, m_track_lb), use_container_width=True)
else: st.warning("Mete a alguien para trazar la curva.")
