import plotly.express as px
import plotly.graph_objects as go
import numpy as np
COLORS = {
    "primary":   "#DA291C", "secondary": "#FBE122", "accent":    "#58a6ff",
    "good":      "#3fb950", "warn":      "#e3b341", "bad":       "#f78166",
    "bg":        "#0d1117", "card":      "#161b22", "border":    "#30363d",
    "text":      "#e6edf3", "text2":     "#8b949e",
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(22,27,34,0.6)",
    font=dict(family="Inter, sans-serif", color=COLORS["text"], size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="#30363d", zerolinecolor="#30363d"),
    yaxis=dict(gridcolor="#30363d", zerolinecolor="#30363d"),
)

def graficar_ranking(df_rank, sel_metric, sel_metric_label):
    fig_bar = go.Figure(go.Bar(
        x=df_rank[sel_metric], y=df_rank["player"], orientation="h",
        marker=dict(
            color=df_rank[sel_metric],
            colorscale=[[0, "#f78166"], [0.5, "#e3b341"], [1.0, "#3fb950"]],
            showscale=True,
            colorbar=dict(thickness=10, len=0.6, bgcolor="rgba(0,0,0,0)", tickfont=dict(color="#8b949e"))
        ),
        text=df_rank[sel_metric].round(2), textposition="outside",
        textfont=dict(color="#e6edf3", size=11)
    ))
    fig_bar.update_layout(**PLOTLY_THEME, title=f"Jugadores por {sel_metric_label}", height=340, bargap=0.35)
    return fig_bar

def graficar_radar(df_f, players_sel, profile="Completo (Mixto)"):
    if not players_sel: players_sel = df_f["player"].tolist()[:1]
    
    if profile == "Creador (Pases, xT)":
        categories = ["Precisión", "Prog/90", "Verticalidad", "Pases clave", "xT", "xA"]
        norm_cols  = ["pass_acc", "prog_passes", "vert_idx", "key_passes", "xT_gen", "xA"]
    elif profile == "Destructor (Duelos, Rec)":
        categories = ["Duelos%", "Rec/90", "Int/90", "Precisión", "Prog/90", "Retención (Inv Pérdida)"]
        norm_cols  = ["duels_won", "recoveries", "interceptions", "pass_acc", "prog_passes", "losses"]
    else:
        categories = ["Precisión", "Prog/90", "xT", "Duelos%", "Rec/90", "Retención (Inv Pérdida)"]
        norm_cols  = ["pass_acc", "prog_passes", "xT_gen", "duels_won", "recoveries", "losses"]
    
    fig_radar = go.Figure()
    palette = [COLORS["primary"], COLORS["accent"], COLORS["good"], COLORS["secondary"], COLORS["warn"], COLORS["bad"]]

    for i, player in enumerate(players_sel[:4]):
        row = df_f[df_f["player"] == player].iloc[0]
        vals = [round(100 - (row[col] / (df_f[col].max() or 1) * 100), 1) if col == "losses" else round(row[col] / (df_f[col].max() or 1) * 100, 1) for col in norm_cols]
        vals += [vals[0]]
        
        hex_color = palette[i % len(palette)].lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        fig_radar.add_trace(go.Scatterpolar(
            r=vals, theta=categories + [categories[0]], fill="toself", name=player,
            line=dict(color=palette[i % len(palette)], width=2),
            fillcolor=f"rgba({r},{g},{b},0.12)"
        ))

    fig_radar.update_layout(
        **PLOTLY_THEME,
        polar=dict(
            bgcolor="rgba(22,27,34,0.5)",
            radialaxis=dict(visible=True, range=[0, 100], color="#8b949e", gridcolor="#30363d", tickfont=dict(size=9)),
            angularaxis=dict(color="#e6edf3", gridcolor="#30363d")
        ),
        showlegend=True, legend=dict(x=1.05, y=1), height=340
    )
    return fig_radar

def _add_plotly_pitch(fig):
    line_color = "#30363d"
    # Outer bound
    fig.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color=line_color, width=1.5), layer="below")
    # Half-way line
    fig.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color=line_color, width=1.5), layer="below")
    # Center circle
    fig.add_shape(type="circle", x0=50, y0=30, x1=70, y1=50, line=dict(color=line_color, width=1.5), layer="below")
    fig.add_shape(type="circle", x0=59.5, y0=39.5, x1=60.5, y1=40.5, fillcolor=line_color, line_color=line_color, layer="below")
    # Left Penalty Area
    fig.add_shape(type="rect", x0=0, y0=18, x1=18, y1=62, line=dict(color=line_color, width=1.5), layer="below")
    fig.add_shape(type="rect", x0=0, y0=30, x1=6, y1=50, line=dict(color=line_color, width=1.5), layer="below")
    fig.add_shape(type="circle", x0=11.5, y0=39.5, x1=12.5, y1=40.5, fillcolor=line_color, line_color=line_color, layer="below")
    # Right Penalty Area
    fig.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color=line_color, width=1.5), layer="below")
    fig.add_shape(type="rect", x0=114, y0=30, x1=120, y1=50, line=dict(color=line_color, width=1.5), layer="below")
    fig.add_shape(type="circle", x0=107.5, y0=39.5, x1=108.5, y1=40.5, fillcolor=line_color, line_color=line_color, layer="below")
    
    fig.update_xaxes(range=[-5, 125], showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(range=[-5, 85], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1)

def graficar_heatmap_zonas(player_row):
    np.random.seed(int(hash(player_row["player"])) % 999)
    num_passes = int(player_row["prog_passes"] * 15) + 30
    x = np.random.normal(50 + player_row["vert_idx"] * 25, 20, num_passes)
    y = np.random.normal(40, 25, num_passes)
    x = np.clip(x, 0, 120); y = np.clip(y, 0, 80)
    
    fig = go.Figure(go.Histogram2d(
        x=x, y=y, colorscale="Magma", nbinsx=15, nbinsy=10, 
        zsmooth="best", showscale=False, opacity=0.85, hoverinfo="none"
    ))
    _add_plotly_pitch(fig)
    fig.update_layout(**PLOTLY_THEME, title=f"Zonas de Operación — {player_row['player']}", height=320)
    return fig

def graficar_heatmap_xt(player_row):
    np.random.seed(int(hash(player_row["player"])) % 999 + 1)
    num_events = int(player_row["xT_gen"] * 120) + 5
    x = np.random.normal(95, 12, num_events)
    y = np.random.normal(40, 25, num_events)
    x = np.clip(x, 60, 120); y = np.clip(y, 0, 80)
    sizes = np.random.uniform(10, 30, num_events)
    
    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="markers", 
        marker=dict(size=sizes, color=COLORS["primary"], opacity=0.75, line=dict(color="#0d1117", width=1)),
        text=[f"Pos: ({int(xi)}, {int(yi)}) <br>Acción xT" for xi, yi in zip(x, y)], hoverinfo="text"
    ))
    
    _add_plotly_pitch(fig)
    fig.update_layout(**PLOTLY_THEME, title=f"Nodos de Generación xT — {player_row['player']}", height=320)
    fig.update_xaxes(range=[60, 125]) # Half pitch view
    return fig

def graficar_red_pases(df):
    positions_xy = {
        "A. Onana": (10, 40),
        "D. Dalot": (35, 70), "M. de Ligt": (25, 55), "L. Martinez": (25, 25), "N. Mazraoui": (35, 10),
        "M. Ugarte": (50, 50), "K. Mainoo": (55, 30),
        "A. Garnacho": (75, 75), "B. Fernandes": (70, 40), "M. Rashford": (75, 5),
        "T. Højlund": (95, 40)
    }

    combos = [
        ("A. Onana", "L. Martinez", 60), ("A. Onana", "M. de Ligt", 45),
        ("L. Martinez", "N. Mazraoui", 55), ("M. de Ligt", "D. Dalot", 65),
        ("L. Martinez", "K. Mainoo", 70), ("M. de Ligt", "M. Ugarte", 50),
        ("N. Mazraoui", "M. Rashford", 60), ("D. Dalot", "A. Garnacho", 50),
        ("K. Mainoo", "B. Fernandes", 85), ("M. Ugarte", "K. Mainoo", 75),
        ("M. Ugarte", "B. Fernandes", 60), ("B. Fernandes", "A. Garnacho", 65),
        ("B. Fernandes", "M. Rashford", 70), ("B. Fernandes", "T. Højlund", 55),
        ("A. Garnacho", "T. Højlund", 35), ("M. Rashford", "T. Højlund", 40),
        ("K. Mainoo", "M. Rashford", 45), ("M. Ugarte", "D. Dalot", 55)
    ]

    fig = go.Figure()
    max_w = max(c[2] for c in combos)

    # Draw Edges
    for p1, p2, w in combos:
        if p1 not in positions_xy or p2 not in positions_xy: continue
        x1, y1 = positions_xy[p1]; x2, y2 = positions_xy[p2]
        opaq = 0.2 + 0.6*(w/max_w)
        wd = max(1.5, int((w/max_w)*8))
        fig.add_trace(go.Scatter(
            x=[x1, x2, None], y=[y1, y2, None], mode="lines",
            line=dict(color=f"rgba(88,166,255,{opaq:.2f})", width=wd),
            hoverinfo="skip", showlegend=False
        ))
        
    # Draw Nodes
    for p, (x, y) in positions_xy.items():
        row = df[df["player"] == p]
        xt_val = row["xT_gen"].values[0] if len(row) else 0
        node_size = max(18, 25 + xt_val * 70)
        color = COLORS["primary"] if "Fernandes" in p or "Mainoo" in p else COLORS["accent"]
        
        name = p.split(".")[1].strip() if "." in p else p
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers+text",
            marker=dict(size=node_size, color=color, line=dict(color="#0d1117", width=2)),
            text=[name], textposition="bottom center", textfont=dict(color="#e6edf3", size=11),
            hoverinfo="text", hovertext=f"{p}<br>Pases Progresivos: {row['prog_passes'].values[0] if len(row) else 0}<br>xT: {xt_val}", name=p, showlegend=False
        ))

    _add_plotly_pitch(fig)
    fig.update_layout(**PLOTLY_THEME, height=520, title="Red de Flujo y Pases 4-2-3-1 (Interactiva)")
    return fig

def graficar_evolucion(df_time, df_f, players_evo, metric_evo_col, metric_label):
    df_evo = df_time[df_time["player"].isin(players_evo)]
    fig_evo = go.Figure()
    pal = [COLORS["primary"], COLORS["accent"], COLORS["good"], COLORS["secondary"], COLORS["bad"], "#d2a8ff"]

    for i, player in enumerate(players_evo):
        d = df_evo[df_evo["player"] == player].sort_values("matchday").copy()
        d["smooth"] = d[metric_evo_col].rolling(5, min_periods=1).mean()
        
        # Raw data line (dotted)
        fig_evo.add_trace(go.Scatter(x=d["matchday"], y=d[metric_evo_col], mode="lines",
                                     line=dict(color=pal[i % len(pal)], width=1, dash="dot"), opacity=0.3, showlegend=False, hoverinfo="skip"))
        # Smooth data line
        fig_evo.add_trace(go.Scatter(x=d["matchday"], y=d["smooth"], mode="lines+markers", name=player,
                                     line=dict(color=pal[i % len(pal)], width=2.5), marker=dict(size=4, color=pal[i % len(pal)])))

    fig_evo.add_hline(y=df_f[metric_evo_col].mean(), line_dash="dash", line_color="#30363d", annotation_text="Media equipo", annotation_font_color="#8b949e")
    fig_evo.update_layout(**PLOTLY_THEME, title=f"{metric_label} — Media móvil 5 partidos", height=420, legend=dict(orientation="h", y=-0.15, x=0))
    fig_evo.update_xaxes(title="Jornada"); fig_evo.update_yaxes(title=metric_label)
    return fig_evo
