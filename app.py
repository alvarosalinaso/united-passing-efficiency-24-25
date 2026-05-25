"""
United Passing Network — Complex Network Analysis
Álvaro Salinas Ortiz | github.com/alvarosalinaso
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="United Passing Network",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root {
  --bg:      #0F1117;
  --surface: #1A1D24;
  --border:  #2A2D35;
  --text-1:  #F0F2F6;
  --text-2:  #9BA3B0;
  --red:     #DA291C;
  --yellow:  #FBE122;
  --gold:    #F59E0B;
  --blue:    #4F8BF9;
  --green:   #3FB950;
  --radius:  10px;
}
html,body,[class*="css"] { font-family: 'Inter', system-ui, sans-serif; }
.main, .block-container { background: var(--bg) !important; }
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1200px; }
section[data-testid="stSidebar"] { background: #1A1D24 !important; border-right: 1px solid #2A2D35; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p { color: #9BA3B0 !important; font-size:.85rem !important; }
section[data-testid="stSidebar"] h2 { color: #DA291C !important; font-size:1rem !important; font-weight:700 !important; }
.kpi { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
       padding:1rem 1.25rem; }
.kpi-val   { font-size:1.6rem; font-weight:700; color:var(--text-1); line-height:1.1; }
.kpi-label { font-size:.68rem; font-weight:600; color:var(--text-2); text-transform:uppercase; letter-spacing:.08em; margin-top:.35rem; }
.kpi-delta { font-size:.75rem; font-weight:500; margin-top:.25rem; }
.kpi-delta.up   { color: var(--green); }
.kpi-delta.down { color: var(--red); }
.kpi-delta.neu  { color: var(--text-2); }
.sec-header { font-size:.72rem; font-weight:700; color:var(--text-2); text-transform:uppercase;
              letter-spacing:.1em; border-bottom:2px solid var(--red); padding-bottom:.4rem; margin:1.6rem 0 .9rem; }
.desc-box { background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--blue);
            border-radius: 8px; padding: 0.7rem 1rem; margin: 0.3rem 0 1rem; font-size: 0.82rem; color: #C0C4CC; line-height: 1.5; }
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

SQUAD = [
    {"player":"Onana",      "pos":"GK",  "x":5,  "y":34},
    {"player":"Dalot",      "pos":"RB",  "x":25, "y":3},
    {"player":"Martínez", "pos":"CB",  "x":20, "y":50},
    {"player":"De Ligt",    "pos":"CB",  "x":20, "y":18},
    {"player":"Shaw",       "pos":"LB",  "x":25, "y":65},
    {"player":"Ugarte",     "pos":"CDM", "x":40, "y":34},
    {"player":"Mainoo",     "pos":"CM",  "x":50, "y":55},
    {"player":"Casemiro",   "pos":"CDM", "x":40, "y":14},
    {"player":"Fernandes",  "pos":"CAM", "x":62, "y":34},
    {"player":"Garnacho",   "pos":"RW",  "x":72, "y":65},
    {"player":"Hojlund",    "pos":"ST",  "x":80, "y":34},
]
BASE_PASSES = [
    ("Onana","Martínez",18),("Onana","De Ligt",14),("Onana","Ugarte",8),
    ("Martínez","Fernandes",12),("Martínez","Mainoo",10),("Martínez","Ugarte",9),
    ("De Ligt","Casemiro",11),("De Ligt","Martínez",7),("De Ligt","Shaw",6),
    ("Dalot","Fernandes",9),("Dalot","Mainoo",7),("Dalot","Garnacho",5),
    ("Shaw","Ugarte",8),("Shaw","Casemiro",6),("Shaw","Fernandes",4),
    ("Ugarte","Mainoo",14),("Ugarte","Fernandes",10),("Ugarte","Martínez",5),
    ("Casemiro","Ugarte",9),("Casemiro","De Ligt",4),("Casemiro","Fernandes",7),
    ("Mainoo","Fernandes",16),("Mainoo","Garnacho",8),("Mainoo","Hojlund",5),
    ("Fernandes","Garnacho",14),("Fernandes","Hojlund",11),("Fernandes","Mainoo",9),
    ("Fernandes","Dalot",6),("Garnacho","Hojlund",8),("Garnacho","Fernandes",5),
    ("Hojlund","Fernandes",4),("Hojlund","Mainoo",3),
]
STATS = {
    "Onana":      {"pass_acc":72.4,"prog":4.5,"xT":0.02,"vert":0.95},
    "Dalot":      {"pass_acc":84.1,"prog":4.2,"xT":0.22,"vert":0.61},
    "Martínez": {"pass_acc":93.4,"prog":6.5,"xT":0.15,"vert":0.88},
    "De Ligt":    {"pass_acc":91.0,"prog":3.8,"xT":0.05,"vert":0.55},
    "Shaw":       {"pass_acc":87.1,"prog":4.1,"xT":0.20,"vert":0.70},
    "Ugarte":     {"pass_acc":89.1,"prog":3.4,"xT":0.08,"vert":0.41},
    "Mainoo":     {"pass_acc":85.7,"prog":4.0,"xT":0.24,"vert":0.64},
    "Casemiro":   {"pass_acc":86.5,"prog":3.2,"xT":0.11,"vert":0.45},
    "Fernandes":  {"pass_acc":88.4,"prog":5.1,"xT":0.42,"vert":0.78},
    "Garnacho":   {"pass_acc":74.1,"prog":1.8,"xT":0.35,"vert":0.48},
    "Hojlund":    {"pass_acc":83.1,"prog":3.5,"xT":0.18,"vert":0.58},
}
PL = {
    "Arsenal":     {"poss":60.5,"pass_acc":88.2,"prog":55.4,"xT":2.10},
    "Man City":    {"poss":65.2,"pass_acc":90.1,"prog":62.3,"xT":2.45},
    "Liverpool":   {"poss":61.0,"pass_acc":86.5,"prog":58.1,"xT":2.20},
    "Man United":  {"poss":52.1,"pass_acc":84.5,"prog":42.1,"xT":1.48},
    "Aston Villa": {"poss":54.2,"pass_acc":85.0,"prog":45.2,"xT":1.60},
    "Tottenham":   {"poss":59.8,"pass_acc":86.8,"prog":52.1,"xT":1.90},
    "Chelsea":     {"poss":58.5,"pass_acc":87.1,"prog":50.4,"xT":1.85},
    "Newcastle":   {"poss":51.0,"pass_acc":82.5,"prog":41.2,"xT":1.55},
    "Brighton":    {"poss":58.1,"pass_acc":86.2,"prog":49.8,"xT":1.70},
    "West Ham":    {"poss":45.2,"pass_acc":79.8,"prog":32.5,"xT":1.10},
}

def adjust(tier):
    np.random.seed(42)
    return [(s,t,max(1,int(w*(np.random.uniform(.6,.85) if tier=="Top 6" else np.random.uniform(.95,1.15)))))
            for s,t,w in BASE_PASSES]

def betweenness_simple(passes, players):
    names = [p["player"] for p in players]
    adj   = {n: {} for n in names}
    for s,t,w in passes:
        if s in adj and t in adj:
            adj[s][t] = w
    scores = {n:0 for n in names}
    for start in names:
        for end in names:
            if start == end: continue
            visited, queue = set(), [[start]]
            found = []
            while queue:
                path = queue.pop(0)
                node = path[-1]
                if node == end: found = path; break
                if node in visited: continue
                visited.add(node)
                for nb in adj.get(node, {}):
                    if nb not in visited: queue.append(path+[nb])
            for n in found[1:-1]: scores[n] += 1
    total = max(sum(scores.values()), 1)
    return {k: v/total for k,v in scores.items()}

PT = dict(template="plotly_dark")

PT_L = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(26,29,36,0.6)",
    font=dict(family="Inter, system-ui", color="#F0F2F6", size=12),
)

def kpi(col, val, label, delta="", cls="neu"):
    col.markdown(
        f"<div class='kpi'><div class='kpi-val'>{val}</div>"
        f"<div class='kpi-label'>{label}</div>"
        f"{'<div class=kpi-delta '+cls+'>'+delta+'</div>' if delta else ''}"
        f"</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🕸️ Passing Network")
    st.markdown("---")
    vista = st.selectbox("**Sección**", [
        "🗺️ Red táctica de pases",
        "📐 Métricas individuales",
        "⚖️ vs Premier League",
        "🔄 Resto PL vs Top 6",
    ])

    tier  = "Resto PL"
    min_w = 5
    pos_f = ["CDM","CM","CAM","RW","ST"]
    ex = "xT"
    ey = "prog"

    if vista == "🗺️ Red táctica de pases":
        tier = st.radio("Tipo de rival",
            ["Resto PL", "Top 6"],
            help="Resto PL = rivales de media/baja tabla. Top 6 = Arsenal, City, Liverpool, etc. Contra equipos fuertes el volumen de pases disminuye.")
        min_w = st.slider("Conexiones mínimas (filtrar ruido)", 1, 20, 5,
            help="Muestra solo conexiones con al menos este número de pases. Útil para limpiar el gráfico.")

    elif vista == "📐 Métricas individuales":
        pos_f = st.multiselect("Filtrar por posición",
            ["GK","RB","LB","CB","CDM","CM","CAM","RW","ST"],
            default=["CDM","CM","CAM","RW","ST"],
            help="Seleccioná qué posiciones querés ver en el gráfico.")
        st.markdown("**Ejes del gráfico**")
        ex = st.selectbox("Eje X", ["pass_acc","prog","xT","vert"],
            format_func=lambda x:{"pass_acc":"Precisión de pase %","prog":"Pases progresivos/90","xT":"xT generado","vert":"Verticalidad (0-1)"}[x])
        ey = st.selectbox("Eje Y", ["xT","prog","pass_acc","vert"],
            format_func=lambda x:{"pass_acc":"Precisión de pase %","prog":"Pases progresivos/90","xT":"xT generado","vert":"Verticalidad (0-1)"}[x])

    st.markdown("---")
    with st.expander("ℹ️ ¿Qué hace cada sección?"):
        st.markdown("""
        **🗺️ Red táctica** — Mapa de conexiones de pase entre jugadores. El tamaño del círculo indica qué tan importante es cada jugador en la circulación (betweenness centrality).
        **📐 Métricas** — Gráfico de burbujas para comparar el rendimiento de jugadores en dos métricas a la vez.
        **⚖️ vs PL** — Ranking del Manchester United vs el resto de la Premier League.
        **🔄 Resto vs Top 6** — Compara el rendimiento del equipo contra rivales fuertes vs débiles.
        """)

    st.markdown("---")
    st.markdown("<p style='font-size:.75rem;color:#DA291C;'>Álvaro Salinas Ortiz<br>"
                "<a href='https://github.com/alvarosalinaso' style='color:#4F8BF9;'>github.com/alvarosalinaso</a></p>",
                unsafe_allow_html=True)

passes_net = adjust(tier)
passes_f   = [(s,t,w) for s,t,w in passes_net if w >= min_w]
bet        = betweenness_simple(passes_f, SQUAD)
out_deg    = {p["player"]: sum(w for s,t,w in passes_f if s==p["player"]) for p in SQUAD}
in_deg     = {p["player"]: sum(w for s,t,w in passes_f if t==p["player"]) for p in SQUAD}
top_broker = max(bet, key=bet.get) if bet else "N/A"

st.markdown("""
<div style="display:flex;align-items:center;gap:1.5rem;margin-bottom:.3rem;">
  <img src="https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"
       style="height:80px;width:80px;object-fit:contain;flex-shrink:0;">
  <div>
    <div style="font-size:2.2rem;font-weight:800;color:#DA291C;letter-spacing:-1px;line-height:1.1;">Manchester United</div>
    <div style="color:#9BA3B0;font-size:1rem;margin-top:.2rem;">Red de Pases · Análisis de Redes Complejas · Temporada 2024-25</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.caption("Análisis táctico del Manchester United · Proyecto de Álvaro Salinas · Datos sintéticos basados en rendimiento real")
st.divider()

st.markdown("""
<div class="desc-box" style="border-left-color:#DA291C;">
<strong>🏟️ ¿De qué trata esto?</strong> Este dashboard analiza cómo circula el balón en el <strong>Manchester United</strong>
durante la temporada 2024-25 usando teoría de redes (Complex Network Analysis). Podés ver <strong>quién conecta con quién</strong>,
<strong>qué jugadores son más importantes</strong> en la circulación y <strong>cómo rinde el equipo</strong> comparado con
la Premier League. Los datos son sintéticos pero están basados en métricas reales de rendimiento.
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
kpi(c1, sum(w for _,_,w in passes_net), "Pases totales en muestra")
kpi(c2, f"{np.mean([v['pass_acc'] for v in STATS.values()]):.1f}%", "Precisión pase promedio")
kpi(c3, top_broker, "Broker táctico (betweenness)",
    "Jugador más crítico en el flujo", "neu")
kpi(c4, max(STATS,key=lambda x:STATS[x]["xT"]), "Mayor xT generado")
st.markdown("<br>", unsafe_allow_html=True)

if vista == "🗺️ Red táctica de pases":
    st.markdown("<div class='sec-header'>¿Qué ves aquí?</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="desc-box">
    <strong>Red de pases sobre el campo:</strong> Cada círculo es un jugador. <strong>Tamaño</strong> = betweenness centrality
    (qué tan importante es en el flujo de pases). <strong>Color</strong> = nivel de centralidad.
    <strong>Líneas</strong> = conexiones de pase; más gruesas = más volumen.
    </div>
    """, unsafe_allow_html=True)

    pos_xy  = {p["player"]: (p["x"],p["y"]) for p in SQUAD}
    max_w   = max((w for _,_,w in passes_f), default=1)

    edge_traces = []
    for s,t,w in passes_f:
        x0,y0 = pos_xy[s]; x1,y1 = pos_xy[t]
        op = .15 + (w/max_w)*.7
        wd = .8  + (w/max_w)*7
        edge_traces.append(go.Scatter(
            x=[x0,x1,None], y=[y0,y1,None], mode="lines",
            line=dict(width=wd, color=f"rgba(79,139,249,{op:.2f})"),
            hoverinfo="none", showlegend=False,
        ))

    node_s = [14 + max(bet.get(p["player"],0),0)*85 for p in SQUAD]
    node_c = [bet.get(p["player"],0) for p in SQUAD]
    hover  = [
        f"<b>{p['player']}</b> ({p['pos']})<br>"
        f"Betweenness: {bet.get(p['player'],0):.3f}<br>"
        f"Pases salientes: {out_deg.get(p['player'],0)}<br>"
        f"Precisión: {STATS[p['player']]['pass_acc']}%<br>"
        f"xT: {STATS[p['player']]['xT']}"
        for p in SQUAD
    ]

    node_trace = go.Scatter(
        x=[pos_xy[p["player"]][0] for p in SQUAD],
        y=[pos_xy[p["player"]][1] for p in SQUAD],
        mode="markers+text",
        text=[p["player"] for p in SQUAD], textposition="top center",
        hovertext=hover, hoverinfo="text",
        textfont=dict(size=10, color="#F0F2F6"),
        marker=dict(
            size=node_s, color=node_c,
            colorscale=[[0,"#4F8BF9"],[.5,"#DA291C"],[1,"#FBE122"]],
            colorbar=dict(title="Betweenness", thickness=10, len=.55, x=1.01,
                          tickfont=dict(color="#9BA3B0")),
            line=dict(width=2, color="#1A1D24"),
        ),
        showlegend=False,
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    for sh in [
        dict(type="rect", x0=0,y0=0,x1=100,y1=68, line=dict(color="rgba(79,139,249,.25)",width=1.5)),
        dict(type="rect", x0=0,y0=13.84,x1=16.5,y1=54.16, line=dict(color="rgba(79,139,249,.15)",width=1)),
        dict(type="rect", x0=83.5,y0=13.84,x1=100,y1=54.16, line=dict(color="rgba(79,139,249,.15)",width=1)),
        dict(type="circle",x0=44,y0=28,x1=56,y1=40, line=dict(color="rgba(79,139,249,.15)",width=1)),
        dict(type="line",x0=50,y0=0,x1=50,y1=68, line=dict(color="rgba(79,139,249,.10)",width=1)),
    ]: fig.add_shape(**sh)

    fig.update_layout(
        plot_bgcolor="#1A1D24", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-5,110]),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-5,73]),
        height=560, font=dict(family="Inter"),
        title=f"Conexiones con ≥{min_w} pases — vs {tier}",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='sec-header'>Métricas de centralidad por jugador</div>", unsafe_allow_html=True)
    tbl = pd.DataFrame([{
        "Jugador": p["player"], "Pos": p["pos"],
        "Betweenness": round(bet.get(p["player"],0),4),
        "Pases salientes": out_deg.get(p["player"],0),
        "Pases recibidos": in_deg.get(p["player"],0),
        "Pass acc %": STATS[p["player"]]["pass_acc"],
        "xT": STATS[p["player"]]["xT"],
    } for p in SQUAD]).sort_values("Betweenness",ascending=False).reset_index(drop=True)
    st.dataframe(tbl, use_container_width=True, hide_index=True)

elif vista == "📐 Métricas individuales":
    st.markdown("<div class='sec-header'>¿Qué ves aquí?</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="desc-box">
    <strong>Scatter plot de rendimiento:</strong> Cada punto es un jugador. <strong>Ejes X/Y</strong> los elegís vos.
    <strong>Tamaño</strong> del punto = precisión de pase. <strong>Color</strong> = posición.
    </div>
    """, unsafe_allow_html=True)

    stats_df = pd.DataFrame([
        {"player":k, "pos":next(p["pos"] for p in SQUAD if p["player"]==k), **v}
        for k,v in STATS.items()
    ])
    dff = stats_df[stats_df["pos"].isin(pos_f)] if pos_f else stats_df

    if dff.empty:
        st.warning("Selecciona al menos una posición para ver el gráfico.")
    else:
        lm  = {"pass_acc":"Precisión pase %","prog":"Pases progresivos/90","xT":"xT generado","vert":"Verticalidad (0–1)"}
        sizes = [max(STATS[p]["pass_acc"], 0) * 1.5 for p in dff["player"]]
        fig = px.scatter(dff, x=ex, y=ey, color="pos", text="player",
                         size=sizes, size_max=18,
                         color_discrete_sequence=["#DA291C","#F59E0B","#4F8BF9","#3FB950","#A78BFA","#EC4899"],
                         title=f"{lm.get(ex,ex)} vs {lm.get(ey,ey)}",
                         labels={ex:lm.get(ex,ex), ey:lm.get(ey,ey), "pos":"Posición"},
                         **PT)
        fig.update_traces(textposition="top center", marker=dict(line=dict(width=1,color="#1A1D24")))
        fig.add_hline(y=dff[ey].mean(), line_dash="dot", line_color="#9BA3B0",
                      annotation_text="Promedio", annotation_font_size=9)
        fig.add_vline(x=dff[ex].mean(), line_dash="dot", line_color="#9BA3B0")
        fig.update_layout(height=460, legend=dict(orientation="h", y=-0.2), **PT_L)
        st.plotly_chart(fig, use_container_width=True)

elif vista == "⚖️ vs Premier League":
    st.markdown("<div class='sec-header'>¿Qué ves aquí?</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="desc-box">
    <strong>Benchmarking vs Premier League:</strong> Compara al Manchester United con el resto de la liga
    en posesión, precisión de pase, pases progresivos y xT. United aparece destacado en rojo.
    </div>
    """, unsafe_allow_html=True)

    df_pl = pd.DataFrame([{"equipo":k,**v} for k,v in PL.items()])
    metrica_pl = st.selectbox("Métrica",["pass_acc","prog","xT","poss"],
        format_func=lambda x:{"pass_acc":"Precisión pase %","prog":"Pases progresivos/partido",
                               "xT":"xT generado/partido","poss":"Posesión %"}[x])
    df_s = df_pl.sort_values(metrica_pl)
    fig = go.Figure(go.Bar(
        x=df_s[metrica_pl], y=df_s["equipo"], orientation="h",
        marker_color=["#DA291C" if t=="Man United" else "#2A2D35" for t in df_s["equipo"]],
        text=[f"{v:.1f}" for v in df_s[metrica_pl]], textposition="outside", textfont_size=11,
    ))
    lm2={"pass_acc":"Precisión pase %","prog":"Pases prog./partido","xT":"xT/partido","poss":"Posesión %"}
    fig.update_layout(title=f"Premier League — {lm2[metrica_pl]}", **PT_L, height=420)
    fig.update_xaxes(gridcolor="#2A2D35")
    fig.update_yaxes(gridcolor="#2A2D35")
    st.plotly_chart(fig, use_container_width=True)

    utd     = PL["Man United"]
    others  = [v for k,v in PL.items() if k!="Man United"]
    avg_acc = np.mean([o["pass_acc"] for o in others])
    avg_xT  = np.mean([o["xT"] for o in others])
    st.info(f"Man United — Precisión: **{utd['pass_acc']}%** vs promedio PL **{avg_acc:.1f}%** | "
            f"xT: **{utd['xT']}** vs promedio **{avg_xT:.2f}**")

elif vista == "🔄 Resto PL vs Top 6":
    st.markdown("<div class='sec-header'>¿Qué ves aquí?</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="desc-box">
    <strong>Rendimiento contra la élite:</strong> Cómo cambian los pases totales, precisión y xT cuando
    el United enfrenta al Top 6 vs el resto de la liga.
    </div>
    """, unsafe_allow_html=True)

    avg_acc = np.mean([v["pass_acc"] for v in STATS.values()])
    rows = []
    for t in ["Resto PL","Top 6"]:
        adj   = adjust(t)
        acc_m = 0 if t=="Resto PL" else -4.2
        rows.append({"Rival":t,
                     "Pases totales":sum(w for _,_,w in adj),
                     "Precisión media %":round(avg_acc+acc_m,1),
                     "xT total":round(sum(v["xT"] for v in STATS.values())*(1.0 if t=="Resto PL" else .78),2)})
    df_r = pd.DataFrame(rows)

    fig = make_subplots(rows=1, cols=3,
        subplot_titles=["Pases totales","Precisión media %","xT total"])
    C_BAR = ["#DA291C","#F59E0B"]
    for i,col in enumerate(["Pases totales","Precisión media %","xT total"]):
        fig.add_trace(go.Bar(x=df_r["Rival"],y=df_r[col],
            marker_color=C_BAR,showlegend=False,
            text=[f"{v:.1f}" for v in df_r[col]],textposition="outside",
            textfont=dict(color="#F0F2F6")),row=1,col=i+1)
    fig.update_layout(title="Rendimiento de pases: Resto PL vs Top 6",
                      **PT_L, margin=dict(t=60,b=40,l=10,r=10),height=380)
    fig.update_xaxes(gridcolor="#2A2D35")
    fig.update_yaxes(gridcolor="#2A2D35")
    st.plotly_chart(fig, use_container_width=True)

    st.warning(
        f"Contra el **Top 6**, United reduce su precisión de pase ~4pp y su xT generado cae un **22%**. "
        f"**{top_broker}** es el jugador cuya neutralización más interrumpe el flujo ofensivo "
        f"(Betweenness: {bet[top_broker]:.3f})."
    )

st.markdown("---")
st.markdown("<div style='text-align:center;color:#5A5F6B;font-size:.75rem;padding:.5rem 0'>"
            "Álvaro Salinas Ortiz · Data Analyst · "
            "<a href='https://github.com/alvarosalinaso' style='color:#4F8BF9;'>GitHub</a> · "
            "<a href='https://linkedin.com/in/alvaro-salinas-ortiz/' style='color:#4F8BF9;'>LinkedIn</a>"
            "</div>", unsafe_allow_html=True)
