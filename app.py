import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="United Passing Network", page_icon="🕸️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;800&family=Inter:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#f5f3ff;}
.block-container{padding-top:1.5rem;background:#f5f3ff;}
h1,h2,h3{font-family:'Syne',sans-serif;font-weight:800;color:#1e1b4b;}
.kpi{background:#fff;border-radius:14px;padding:1.1rem 1.3rem;border:1.5px solid #ddd6fe;box-shadow:0 2px 8px rgba(109,40,217,.07);}
.kpi-v{font-size:2.1rem;font-weight:800;color:#6d28d9;letter-spacing:-1px;}
.kpi-l{font-size:0.68rem;color:#6b7280;text-transform:uppercase;letter-spacing:1.5px;margin-top:3px;}
section[data-testid="stSidebar"]{background:#1e1b4b!important;}
section[data-testid="stSidebar"] *{color:#e0e7ff!important;}
</style>""", unsafe_allow_html=True)

np.random.seed(99)

SQUAD=[{"player":"Onana","pos":"GK","x":5,"y":34},{"player":"Dalot","pos":"RB","x":25,"y":65},
       {"player":"L.Martínez","pos":"CB","x":20,"y":50},{"player":"De Ligt","pos":"CB","x":20,"y":18},
       {"player":"Shaw","pos":"LB","x":25,"y":3},{"player":"Ugarte","pos":"CDM","x":40,"y":34},
       {"player":"Mainoo","pos":"CM","x":50,"y":55},{"player":"Casemiro","pos":"CDM","x":40,"y":14},
       {"player":"Bruno","pos":"CAM","x":62,"y":34},{"player":"Garnacho","pos":"RW","x":72,"y":65},
       {"player":"Hojlund","pos":"ST","x":80,"y":34}]

BASE=[("Onana","L.Martínez",18),("Onana","De Ligt",14),("Onana","Ugarte",8),
      ("L.Martínez","Bruno",12),("L.Martínez","Mainoo",10),("L.Martínez","Ugarte",9),
      ("De Ligt","Casemiro",11),("De Ligt","L.Martínez",7),("De Ligt","Shaw",6),
      ("Dalot","Bruno",9),("Dalot","Mainoo",7),("Dalot","Garnacho",5),
      ("Shaw","Ugarte",8),("Shaw","Casemiro",6),("Shaw","Bruno",4),
      ("Ugarte","Mainoo",14),("Ugarte","Bruno",10),("Ugarte","L.Martínez",5),
      ("Casemiro","Ugarte",9),("Casemiro","De Ligt",4),("Casemiro","Bruno",7),
      ("Mainoo","Bruno",16),("Mainoo","Garnacho",8),("Mainoo","Hojlund",5),
      ("Bruno","Garnacho",14),("Bruno","Hojlund",11),("Bruno","Mainoo",9),
      ("Bruno","Dalot",6),("Garnacho","Hojlund",8),("Garnacho","Bruno",5),
      ("Hojlund","Bruno",4),("Hojlund","Mainoo",3)]

STATS={"Onana":{"pass_acc":72.4,"prog":4.5,"xT":0.02,"vert":0.95},
       "Dalot":{"pass_acc":84.1,"prog":4.2,"xT":0.22,"vert":0.61},
       "L.Martínez":{"pass_acc":93.4,"prog":6.5,"xT":0.15,"vert":0.88},
       "De Ligt":{"pass_acc":91.0,"prog":3.8,"xT":0.05,"vert":0.55},
       "Shaw":{"pass_acc":87.1,"prog":4.1,"xT":0.20,"vert":0.70},
       "Ugarte":{"pass_acc":89.1,"prog":3.4,"xT":0.08,"vert":0.41},
       "Mainoo":{"pass_acc":85.7,"prog":4.0,"xT":0.24,"vert":0.64},
       "Casemiro":{"pass_acc":86.5,"prog":3.2,"xT":0.11,"vert":0.45},
       "Bruno":{"pass_acc":88.4,"prog":5.1,"xT":0.42,"vert":0.78},
       "Garnacho":{"pass_acc":74.1,"prog":1.8,"xT":0.35,"vert":0.48},
       "Hojlund":{"pass_acc":83.1,"prog":3.5,"xT":0.18,"vert":0.58}}

PL={"Arsenal":{"poss":60.5,"pass_acc":88.2,"prog":55.4,"xT":2.1},
    "Man City":{"poss":65.2,"pass_acc":90.1,"prog":62.3,"xT":2.45},
    "Liverpool":{"poss":61.0,"pass_acc":86.5,"prog":58.1,"xT":2.2},
    "Man United":{"poss":52.1,"pass_acc":84.5,"prog":42.1,"xT":1.48},
    "Aston Villa":{"poss":54.2,"pass_acc":85.0,"prog":45.2,"xT":1.6},
    "Tottenham":{"poss":59.8,"pass_acc":86.8,"prog":52.1,"xT":1.9},
    "Chelsea":{"poss":58.5,"pass_acc":87.1,"prog":50.4,"xT":1.85},
    "Newcastle":{"poss":51.0,"pass_acc":82.5,"prog":41.2,"xT":1.55},
    "Brighton":{"poss":58.1,"pass_acc":86.2,"prog":49.8,"xT":1.7},
    "West Ham":{"poss":45.2,"pass_acc":79.8,"prog":32.5,"xT":1.1}}

def calc_betweenness(passes_list, players):
    """Betweenness centrality simplificado sin networkx"""
    names=[p["player"] for p in players]
    scores={n:0 for n in names}
    adj={n:{} for n in names}
    for s,t,w in passes_list:
        if s in adj and t in adj:
            adj[s][t]=w
    for start in names:
        for end in names:
            if start==end: continue
            path=[]
            visited=set(); queue=[[start]]
            while queue:
                p=queue.pop(0)
                node=p[-1]
                if node==end: path=p; break
                if node in visited: continue
                visited.add(node)
                for nb in adj.get(node,{}):
                    if nb not in visited:
                        queue.append(p+[nb])
            for n in path[1:-1]:
                scores[n]+=1
    total=max(sum(scores.values()),1)
    return {k:v/total for k,v in scores.items()}

def adj_passes(tier):
    result=[]
    for s,t,w in BASE:
        f=np.random.uniform(0.6,0.85) if tier=="Top 6" else np.random.uniform(0.95,1.15)
        result.append((s,t,max(1,int(w*f))))
    return result

with st.sidebar:
    st.markdown("## 🕸️ Controles")
    vista=st.selectbox("Vista",["Red táctica","Métricas individuales","vs Premier League","Resto PL vs Top 6"])
    tier=st.radio("Tipo de rival",["Resto PL","Top 6"])
    min_p=st.slider("Mínimo pases (conexión)",1,20,5)
    if vista=="Métricas individuales":
        pos_f=st.multiselect("Posición",["GK","RB","LB","CB","CDM","CM","CAM","RW","ST"],
                             default=["CDM","CM","CAM","RW","ST"])
        ex=st.selectbox("Eje X",["pass_acc","prog","xT","vert"])
        ey=st.selectbox("Eje Y",["xT","prog","pass_acc","vert"])

passes=adj_passes(tier)
passes_f=[(s,t,w) for s,t,w in passes if w>=min_p]
bet=calc_betweenness(passes_f,SQUAD)
out_deg={p["player"]:sum(w for s,t,w in passes_f if s==p["player"]) for p in SQUAD}
in_deg={p["player"]:sum(w for s,t,w in passes_f if t==p["player"]) for p in SQUAD}
top_broker=max(bet,key=bet.get)

st.markdown("# 🕸️ United Passing Network")
st.markdown(f"### {vista} — vs {tier}")
st.divider()

c1,c2,c3,c4=st.columns(4)
for col,val,lab in zip([c1,c2,c3,c4],
    [sum(w for _,_,w in passes),f"{np.mean([v['pass_acc'] for v in STATS.values()]):.1f}%",
     top_broker,max(STATS,key=lambda x:STATS[x]["xT"])],
    ["Total pases","Precisión promedio","Broker táctico","Mayor xT"]):
    col.markdown(f"<div class='kpi'><div class='kpi-v'>{val}</div><div class='kpi-l'>{lab}</div></div>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)

PURPLE="#6d28d9"; INDIGO="#4f46e5"; VIOLET="#7c3aed"; AMBER="#d97706"; ROSE="#e11d48"
COLORS=[PURPLE,INDIGO,VIOLET,AMBER,ROSE,"#059669","#0284c7","#dc2626","#ea580c","#16a34a","#9333ea"]

if vista=="Red táctica":
    pos_layout={p["player"]:(p["x"],p["y"]) for p in SQUAD}
    max_w=max((w for _,_,w in passes_f),default=1)
    edge_traces=[]
    for s,t,w in passes_f:
        x0,y0=pos_layout[s]; x1,y1=pos_layout[t]
        op=0.1+(w/max_w)*0.75; wd=0.5+(w/max_w)*7
        edge_traces.append(go.Scatter(x=[x0,x1,None],y=[y0,y1,None],mode="lines",
            line=dict(width=wd,color=f"rgba(109,40,217,{op:.2f})"),hoverinfo="none",showlegend=False))
    node_sizes=[12+bet.get(p["player"],0)*90 for p in SQUAD]
    node_trace=go.Scatter(
        x=[pos_layout[p["player"]][0] for p in SQUAD],
        y=[pos_layout[p["player"]][1] for p in SQUAD],
        mode="markers+text",text=[p["player"] for p in SQUAD],textposition="top center",
        hovertext=[f"<b>{p['player']}</b> ({p['pos']})<br>Betweenness: {bet.get(p['player'],0):.3f}<br>Pass acc: {STATS[p['player']]['pass_acc']}%"
                   for p in SQUAD],hoverinfo="text",
        marker=dict(size=node_sizes,color=[bet.get(p["player"],0) for p in SQUAD],
                    colorscale=[[0,"#ddd6fe"],[0.5,INDIGO],[1,PURPLE]],
                    colorbar=dict(title="Betweenness",thickness=10,len=0.6),
                    line=dict(width=2,color="white")),
        textfont=dict(size=10,color="#1e1b4b",family="Syne"),showlegend=False)
    fig=go.Figure(data=edge_traces+[node_trace])
    for sh in [dict(type="rect",x0=0,y0=0,x1=100,y1=68,line=dict(color="rgba(78,65,206,.3)",width=1)),
               dict(type="rect",x0=0,y0=13.84,x1=16.5,y1=54.16,line=dict(color="rgba(78,65,206,.2)",width=1)),
               dict(type="rect",x0=83.5,y0=13.84,x1=100,y1=54.16,line=dict(color="rgba(78,65,206,.2)",width=1)),
               dict(type="circle",x0=44,y0=28,x1=56,y1=40,line=dict(color="rgba(78,65,206,.2)",width=1)),
               dict(type="line",x0=50,y0=0,x1=50,y1=68,line=dict(color="rgba(78,65,206,.15)",width=1))]:
        fig.add_shape(**sh)
    fig.update_layout(plot_bgcolor="#e8f5e2",paper_bgcolor="#f5f3ff",
                      xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-5,105]),
                      yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-5,73]),
                      height=560,font=dict(family="Inter"),
                      title=f"Red de pases vs {tier} — tamaño nodo = Betweenness")
    st.plotly_chart(fig,use_container_width=True)
    tbl=pd.DataFrame([{"Jugador":p["player"],"Pos":p["pos"],
        "Betweenness":round(bet.get(p["player"],0),4),
        "Pases salientes":out_deg.get(p["player"],0),
        "Pases recibidos":in_deg.get(p["player"],0),
        "Pass acc %":STATS[p["player"]]["pass_acc"],
        "xT":STATS[p["player"]]["xT"]} for p in SQUAD]).sort_values("Betweenness",ascending=False).reset_index(drop=True)
    st.dataframe(tbl,use_container_width=True,height=340)

elif vista=="Métricas individuales":
    stats_df=pd.DataFrame([{"player":k,"pos":next(p["pos"] for p in SQUAD if p["player"]==k),**v}
                            for k,v in STATS.items()])
    dff=stats_df[stats_df["pos"].isin(pos_f)] if pos_f else stats_df
    lm={"pass_acc":"Precisión pase %","prog":"Pases progresivos/90","xT":"xT generado","vert":"Verticalidad"}
    fig=px.scatter(dff,x=ex,y=ey,text="player",color="pos",
                   size=[STATS[p]["pass_acc"] for p in dff["player"]],
                   title=f"{lm.get(ex,ex)} vs {lm.get(ey,ey)}",
                   color_discrete_sequence=COLORS)
    fig.update_traces(textposition="top center",marker=dict(line=dict(width=1,color="white")))
    fig.add_hline(y=dff[ey].mean(),line_dash="dash",line_color="#ddd6fe")
    fig.add_vline(x=dff[ex].mean(),line_dash="dash",line_color="#ddd6fe")
    fig.update_layout(plot_bgcolor="#fff",paper_bgcolor="#f5f3ff",height=480,font=dict(family="Inter"))
    st.plotly_chart(fig,use_container_width=True)

elif vista=="vs Premier League":
    df_pl=pd.DataFrame([{"team":k,**v} for k,v in PL.items()])
    metrica_pl=st.selectbox("Métrica",["pass_acc","prog","xT","poss"],
        format_func=lambda x:{"pass_acc":"Precisión pase %","prog":"Pases progresivos","xT":"xT","poss":"Posesión %"}[x])
    df_s=df_pl.sort_values(metrica_pl)
    fig=go.Figure(go.Bar(x=df_s[metrica_pl],y=df_s["team"],orientation="h",
        marker_color=[PURPLE if t=="Man United" else "#ddd6fe" for t in df_s["team"]],
        text=[f"{v:.1f}" for v in df_s[metrica_pl]],textposition="outside"))
    fig.update_layout(plot_bgcolor="#fff",paper_bgcolor="#f5f3ff",height=420,
                      font=dict(family="Inter"),title="Premier League — comparativa de métricas")
    st.plotly_chart(fig,use_container_width=True)

elif vista=="Resto PL vs Top 6":
    rows=[]
    for t in ["Resto PL","Top 6"]:
        adj=adj_passes(t)
        acc_mod=0 if t=="Resto PL" else -4.2
        rows.append({"rival":t,"total_pases":sum(w for _,_,w in adj),
            "prec_media":np.mean([v["pass_acc"] for v in STATS.values()])+acc_mod,
            "xT_total":sum(v["xT"] for v in STATS.values())*(1.0 if t=="Resto PL" else 0.78)})
    df_r=pd.DataFrame(rows)
    fig=make_subplots(rows=1,cols=3,subplot_titles=["Total pases","Precisión promedio %","xT total"])
    for i,col in enumerate(["total_pases","prec_media","xT_total"]):
        fig.add_trace(go.Bar(x=df_r["rival"],y=df_r[col],
            marker_color=[PURPLE,ROSE],showlegend=False),row=1,col=i+1)
    fig.update_layout(plot_bgcolor="#fff",paper_bgcolor="#f5f3ff",height=360,
                      font=dict(family="Inter"),title="Rendimiento vs tipo de rival")
    st.plotly_chart(fig,use_container_width=True)
    st.info(f"Contra el **Top 6**, United reduce su xT generado un ~22% y cae ~4pp en precisión de pase. "
            f"**{top_broker}** es el jugador cuya neutralización más impacta el flujo ofensivo.")
