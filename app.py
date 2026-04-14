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
  --bg:      #F8FAFC;
  --surface: #FFFFFF;
  --border:  #E2E8F0;
  --text-1:  #0F172A;
  --text-2:  #475569;
  --purple:  #6D28D9;
  --purple-l:#EDE9FE;
  --teal:    #0F766E;
  --ok:      #15803D;
  --danger:  #B91C1C;
  --radius:  10px;
  --shadow:  0 1px 3px rgba(0,0,0,.08);
}
html,body,[class*="css"] { font-family: 'Inter', system-ui, sans-serif; }
.main, .block-container { background: var(--bg) !important; }
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1200px; }
section[data-testid="stSidebar"] { background: #1E1B4B !important; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p { color: #C4B5FD !important; font-size:.85rem !important; }
section[data-testid="stSidebar"] h2 { color: #EDE9FE !important; font-size:1rem !important; font-weight:600 !important; }
.kpi { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
       padding:1.1rem 1.25rem; box-shadow:var(--shadow); }
.kpi-val   { font-size:1.9rem; font-weight:700; color:var(--text-1); line-height:1.1; }
.kpi-label { font-size:.7rem; font-weight:600; color:var(--text-2); text-transform:uppercase; letter-spacing:.08em; margin-top:.35rem; }
.kpi-delta { font-size:.78rem; font-weight:500; margin-top:.25rem; }
.kpi-delta.up   { color: var(--ok); }
.kpi-delta.down { color: var(--danger); }
.kpi-delta.neu  { color: var(--text-2); }
.sec-header { font-size:.7rem; font-weight:700; color:var(--text-2); text-transform:uppercase;
              letter-spacing:.1em; border-bottom:2px solid var(--purple-l); padding-bottom:.4rem; margin:1.6rem 0 .9rem; }
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

# ─── DATOS ────────────────────────────────────────────────────────────────────
SQUAD = [
    {"player":"Onana",      "pos":"GK",  "x":5,  "y":34},
    {"player":"Dalot",      "pos":"RB",  "x":25, "y":65},
    {"player":"L.Martínez", "pos":"CB",  "x":20, "y":50},
    {"player":"De Ligt",    "pos":"CB",  "x":20, "y":18},
    {"player":"Shaw",       "pos":"LB",  "x":25, "y":3 },
    {"player":"Ugarte",     "pos":"CDM", "x":40, "y":34},
    {"player":"Mainoo",     "pos":"CM",  "x":50, "y":55},
    {"player":"Casemiro",   "pos":"CDM", "x":40, "y":14},
    {"player":"Bruno",      "pos":"CAM", "x":62, "y":34},
    {"player":"Garnacho",   "pos":"RW",  "x":72, "y":65},
    {"player":"Hojlund",    "pos":"ST",  "x":80, "y":34},
]
BASE_PASSES = [
    ("Onana","L.Martínez",18),("Onana","De Ligt",14),("Onana","Ugarte",8),
    ("L.Martínez","Bruno",12),("L.Martínez","Mainoo",10),("L.Martínez","Ugarte",9),
    ("De Ligt","Casemiro",11),("De Ligt","L.Martínez",7),("De Ligt","Shaw",6),
    ("Dalot","Bruno",9),("Dalot","Mainoo",7),("Dalot","Garnacho",5),
    ("Shaw","Ugarte",8),("Shaw","Casemiro",6),("Shaw","Bruno",4),
    ("Ugarte","Mainoo",14),("Ugarte","Bruno",10),("Ugarte","L.Martínez",5),
    ("Casemiro","Ugarte",9),("Casemiro","De Ligt",4),("Casemiro","Bruno",7),
    ("Mainoo","Bruno",16),("Mainoo","Garnacho",8),("Mainoo","Hojlund",5),
    ("Bruno","Garnacho",14),("Bruno","Hojlund",11),("Bruno","Mainoo",9),
    ("Bruno","Dalot",6),("Garnacho","Hojlund",8),("Garnacho","Bruno",5),
    ("Hojlund","Bruno",4),("Hojlund","Mainoo",3),
]
STATS = {
    "Onana":      {"pass_acc":72.4,"prog":4.5,"xT":0.02,"vert":0.95},
    "Dalot":      {"pass_acc":84.1,"prog":4.2,"xT":0.22,"vert":0.61},
    "L.Martínez": {"pass_acc":93.4,"prog":6.5,"xT":0.15,"vert":0.88},
    "De Ligt":    {"pass_acc":91.0,"prog":3.8,"xT":0.05,"vert":0.55},
    "Shaw":       {"pass_acc":87.1,"prog":4.1,"xT":0.20,"vert":0.70},
    "Ugarte":     {"pass_acc":89.1,"prog":3.4,"xT":0.08,"vert":0.41},
    "Mainoo":     {"pass_acc":85.7,"prog":4.0,"xT":0.24,"vert":0.64},
    "Casemiro":   {"pass_acc":86.5,"prog":3.2,"xT":0.11,"vert":0.45},
    "Bruno":      {"pass_acc":88.4,"prog":5.1,"xT":0.42,"vert":0.78},
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
    """Centralidad de intermediación aproximada sin networkx"""
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

PT = dict(
    template="plotly_white", paper_bgcolor="white", plot_bgcolor="white",
    font=dict(family="Inter, system-ui", color="#0F172A", size=12),
    margin=dict(t=44, b=30, l=10, r=10),
    colorway=["#6D28D9","#0F766E","#C41E3A","#D97706","#0891B2","#15803D","#DC2626"],
)

def kpi(col, val, label, delta="", cls="neu"):
    col.markdown(
        f"<div class='kpi'><div class='kpi-val'>{val}</div>"
        f"<div class='kpi-label'>{label}</div>"
        f"{'<div class=kpi-delta '+cls+'>'+delta+'</div>' if delta else ''}"
        f"</div>", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🕸️ Passing Network")
    st.markdown("---")
    vista = st.selectbox("**Sección**", [
        "🗺️ Red táctica de pases",
        "📐 Métricas individuales",
        "⚖️ vs Premier League",
        "🔄 Resto PL vs Top 6",
    ])
    tier    = st.radio("Tipo de rival", ["Resto PL","Top 6"],
                        help="Filtra el volumen de pases según dificultad del rival")
    min_w   = st.slider("Mínimo de pases (mostrar conexión)", 1, 20, 5,
                         help="Oculta conexiones con menos de N pases para reducir ruido visual")

    if vista == "📐 Métricas individuales":
        pos_f = st.multiselect("Posición", ["GK","RB","LB","CB","CDM","CM","CAM","RW","ST"],
                                default=["CDM","CM","CAM","RW","ST"])
        ex = st.selectbox("Eje X", ["pass_acc","prog","xT","vert"],
                           format_func=lambda x:{"pass_acc":"Precisión pase %","prog":"Pas. prog./90",
                                                   "xT":"xT generado","vert":"Verticalidad"}[x])
        ey = st.selectbox("Eje Y", ["xT","prog","pass_acc","vert"],
                           format_func=lambda x:{"pass_acc":"Precisión pase %","prog":"Pas. prog./90",
                                                   "xT":"xT generado","vert":"Verticalidad"}[x])
    st.markdown("---")
    st.markdown("<p style='font-size:.75rem;color:#7C3AED;'>Álvaro Salinas Ortiz<br>"
                "<a href='https://github.com/alvarosalinaso' style='color:#A78BFA;'>github.com/alvarosalinaso</a></p>",
                unsafe_allow_html=True)

# ─── COMPUTE ──────────────────────────────────────────────────────────────────
passes    = adjust(tier)
passes_f  = [(s,t,w) for s,t,w in passes if w >= min_w]
bet       = betweenness_simple(passes_f, SQUAD)
out_deg   = {p["player"]: sum(w for s,t,w in passes_f if s==p["player"]) for p in SQUAD}
in_deg    = {p["player"]: sum(w for s,t,w in passes_f if t==p["player"]) for p in SQUAD}
top_broker= max(bet, key=bet.get)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("# 🕸️ United Passing Network")
st.caption(f"Complex Network Analysis · vs {tier}")
st.divider()

c1,c2,c3,c4 = st.columns(4)
kpi(c1, sum(w for _,_,w in passes), "Pases totales en muestra")
kpi(c2, f"{np.mean([v['pass_acc'] for v in STATS.values()]):.1f}%", "Precisión pase promedio")
kpi(c3, top_broker, "Broker táctico (betweenness)",
    "Jugador más crítico en el flujo", "neu")
kpi(c4, max(STATS,key=lambda x:STATS[x]["xT"]), "Mayor xT generado")
st.markdown("<br>", unsafe_allow_html=True)

# ─── VISTAS ───────────────────────────────────────────────────────────────────

if vista == "🗺️ Red táctica de pases":
    st.markdown("<div class='sec-header'>Red de pases sobre el campo — tamaño del nodo = Betweenness Centrality</div>",
                unsafe_allow_html=True)
    st.caption("Betweenness mide cuántas rutas de pase pasan por ese jugador. Un valor alto = punto crítico táctico.")

    pos_xy  = {p["player"]: (p["x"],p["y"]) for p in SQUAD}
    max_w   = max((w for _,_,w in passes_f), default=1)

    edge_traces = []
    for s,t,w in passes_f:
        x0,y0 = pos_xy[s]; x1,y1 = pos_xy[t]
        op = .12 + (w/max_w)*.72
        wd = .8  + (w/max_w)*8
        edge_traces.append(go.Scatter(
            x=[x0,x1,None], y=[y0,y1,None], mode="lines",
            line=dict(width=wd, color=f"rgba(109,40,217,{op:.2f})"),
            hoverinfo="none", showlegend=False,
        ))

    node_s = [14 + bet.get(p["player"],0)*85 for p in SQUAD]
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
        textfont=dict(size=10, color="#0F172A"),
        marker=dict(
            size=node_s, color=node_c,
            colorscale=[[0,"#EDE9FE"],[.5,"#7C3AED"],[1,"#4C1D95"]],
            colorbar=dict(title="Betweenness", thickness=10, len=.55, x=1.01),
            line=dict(width=2, color="white"),
        ),
        showlegend=False,
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    for sh in [
        dict(type="rect", x0=0,y0=0,x1=100,y1=68, line=dict(color="rgba(109,40,217,.25)",width=1.5)),
        dict(type="rect", x0=0,y0=13.84,x1=16.5,y1=54.16, line=dict(color="rgba(109,40,217,.15)",width=1)),
        dict(type="rect", x0=83.5,y0=13.84,x1=100,y1=54.16, line=dict(color="rgba(109,40,217,.15)",width=1)),
        dict(type="circle",x0=44,y0=28,x1=56,y1=40, line=dict(color="rgba(109,40,217,.15)",width=1)),
        dict(type="line",x0=50,y0=0,x1=50,y1=68, line=dict(color="rgba(109,40,217,.10)",width=1)),
    ]: fig.add_shape(**sh)

    fig.update_layout(
        plot_bgcolor="#E8F5E2", paper_bgcolor="#F8FAFC",
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
    stats_df = pd.DataFrame([
        {"player":k,"pos":next(p["pos"] for p in SQUAD if p["player"]==k),**v}
        for k,v in STATS.items()
    ])
    dff = stats_df[stats_df["pos"].isin(pos_f)] if pos_f else stats_df
    lm  = {"pass_acc":"Precisión pase %","prog":"Pases progresivos/90","xT":"xT generado","vert":"Verticalidad (0–1)"}
    fig = px.scatter(dff, x=ex, y=ey, color="pos", text="player",
                     size=[STATS[p]["pass_acc"] for p in dff["player"]],
                     title=f"{lm.get(ex,ex)} vs {lm.get(ey,ey)}",
                     labels={ex:lm.get(ex,ex), ey:lm.get(ey,ey), "pos":"Posición"},
                     **PT)
    fig.update_traces(textposition="top center", marker=dict(line=dict(width=1,color="white")))
    fig.add_hline(y=dff[ey].mean(), line_dash="dot", line_color="#94A3B8",
                  annotation_text="Promedio", annotation_font_size=9)
    fig.add_vline(x=dff[ex].mean(), line_dash="dot", line_color="#94A3B8")
    fig.update_layout(height=460, legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

elif vista == "⚖️ vs Premier League":
    df_pl = pd.DataFrame([{"equipo":k,**v} for k,v in PL.items()])
    metrica_pl = st.selectbox("Métrica",["pass_acc","prog","xT","poss"],
        format_func=lambda x:{"pass_acc":"Precisión pase %","prog":"Pases progresivos/partido",
                               "xT":"xT generado/partido","poss":"Posesión %"}[x])
    df_s = df_pl.sort_values(metrica_pl)
    fig = go.Figure(go.Bar(
        x=df_s[metrica_pl], y=df_s["equipo"], orientation="h",
        marker_color=["#6D28D9" if t=="Man United" else "#EDE9FE" for t in df_s["equipo"]],
        text=[f"{v:.1f}" for v in df_s[metrica_pl]], textposition="outside", textfont_size=11,
    ))
    lm2={"pass_acc":"Precisión pase %","prog":"Pases prog./partido","xT":"xT/partido","poss":"Posesión %"}
    fig.update_layout(title=f"Premier League — {lm2[metrica_pl]}", **PT, height=420)
    st.plotly_chart(fig, use_container_width=True)

    utd     = PL["Man United"]
    others  = [v for k,v in PL.items() if k!="Man United"]
    avg_acc = np.mean([o["pass_acc"] for o in others])
    avg_xT  = np.mean([o["xT"] for o in others])
    st.info(f"Man United — Precisión: **{utd['pass_acc']}%** vs promedio PL **{avg_acc:.1f}%** | "
            f"xT: **{utd['xT']}** vs promedio **{avg_xT:.2f}**")

elif vista == "🔄 Resto PL vs Top 6":
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
    COLORS_BAR = ["#6D28D9","#C41E3A"]
    for i,col in enumerate(["Pases totales","Precisión media %","xT total"]):
        fig.add_trace(go.Bar(x=df_r["Rival"],y=df_r[col],
            marker_color=COLORS_BAR,showlegend=False,
            text=[f"{v:.1f}" for v in df_r[col]],textposition="outside"),row=1,col=i+1)
    fig.update_layout(title="Rendimiento de pases: Resto PL vs Top 6",
                      paper_bgcolor="white",plot_bgcolor="white",
                      font=dict(family="Inter",color="#0F172A",size=12),
                      margin=dict(t=60,b=40,l=10,r=10),height=380)
    st.plotly_chart(fig, use_container_width=True)

    st.warning(
        f"Contra el **Top 6**, United reduce su precisión de pase ~4pp y su xT generado cae un **22%**. "
        f"**{top_broker}** es el jugador cuya neutralización más interrumpe el flujo ofensivo "
        f"(Betweenness: {bet[top_broker]:.3f})."
    )
