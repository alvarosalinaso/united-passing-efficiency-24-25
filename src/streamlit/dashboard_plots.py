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

def graficar_radar(df_f, players_sel):
    if not players_sel: players_sel = df_f["player"].tolist()[:1]
    categories = ["Precisión", "Prog/90", "Verticalidad", "Pases clave", "xT", "xA"]
    norm_cols  = ["pass_acc", "prog_passes", "vert_idx", "key_passes", "xT_gen", "xA"]
    
    fig_radar = go.Figure()
    palette = [COLORS["primary"], COLORS["accent"], COLORS["good"], COLORS["secondary"], COLORS["warn"], COLORS["bad"]]

    for i, player in enumerate(players_sel[:4]):
        row = df_f[df_f["player"] == player].iloc[0]
        vals = [round(row[col] / (df_f[col].max() or 1) * 100, 1) for col in norm_cols]
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

def graficar_heatmap_zonas(player_row):
    zones_y = ["Bloque Bajo", "Zona Construc.", "Zona Ataque", "Último Tercio"]
    zones_x = ["Banda Izq.", "Semi-izq.", "Centro Izq.", "Centro Der.", "Semi-der.", "Banda Der."]

    np.random.seed(int(hash(player_row["player"])) % 999)
    base, vert = player_row["prog_passes"] * 3, player_row["vert_idx"]
    heat = np.random.exponential(base, (4, 6))
    heat[2:, 2:4] *= (1 + vert * 2)
    heat[:1, :] *= 0.4
    heat = np.clip(heat, 0, 35)

    fig_hm = go.Figure(go.Heatmap(
        z=heat, x=zones_x, y=zones_y,
        colorscale=[[0, "#0d1117"], [0.25, "#1a3a5c"], [0.5, "#1f6feb"], [0.75, "#DA291C"], [1.0, "#FBE122"]],
        showscale=True, colorbar=dict(title="Intens.", thickness=14, bgcolor="rgba(0,0,0,0)"),
        hoverongaps=False
    ))
    # Lineas tácticas
    fig_hm.add_shape(type="rect", x0=-0.5, x1=5.5, y0=-0.5, y1=3.5, line=dict(color="#30363d", width=1))
    fig_hm.add_shape(type="line", x0=-0.5, x1=5.5, y0=0.5, y1=0.5, line=dict(color="#30363d", dash="dot", width=1))
    fig_hm.add_shape(type="line", x0=-0.5, x1=5.5, y0=1.5, y1=1.5, line=dict(color="#30363d", dash="dot", width=1))
    fig_hm.add_shape(type="line", x0=-0.5, x1=5.5, y0=2.5, y1=2.5, line=dict(color="#DA291C", dash="dash", width=1.5))
    
    fig_hm.update_layout(**PLOTLY_THEME, title=f"Pases progresivos — {player_row['player']}", height=400)
    fig_hm.update_xaxes(side="top", gridcolor="rgba(0,0,0,0)"); fig_hm.update_yaxes(gridcolor="rgba(0,0,0,0)")
    return fig_hm

def graficar_heatmap_xt(player_row):
    zones_y = ["Bloque Bajo", "Zona Construc.", "Zona Ataque", "Último Tercio"]
    zones_x = ["Banda Izq.", "Semi-izq.", "Centro Izq.", "Centro Der.", "Semi-der.", "Banda Der."]

    xT_zones = np.random.exponential(player_row["xT_gen"] * 5, (4, 6))
    xT_zones[3, 2:4] *= 2.5

    fig_xt = go.Figure(go.Heatmap(
        z=xT_zones, x=zones_x, y=zones_y,
        colorscale=[[0, "#161b22"], [0.4, "#3fb950"], [0.8, "#FBE122"], [1, "#DA291C"]],
        colorbar=dict(title="xT", thickness=14, bgcolor="rgba(0,0,0,0)"),
    ))
    fig_xt.update_layout(**PLOTLY_THEME, height=360, title=f"xT Generado — {player_row['player']}")
    fig_xt.update_xaxes(side="top", gridcolor="rgba(0,0,0,0)"); fig_xt.update_yaxes(gridcolor="rgba(0,0,0,0)")
    return fig_xt

def graficar_red_pases(df):
    positions_xy = {
        "B. Fernandes": (60, 80), "C. Eriksen": (50, 58), "K. Mainoo": (70, 62),
        "T. Højlund": (55, 45),  "M. Mount": (65, 72),  "Casemiro": (55, 35),
    }
    combos = [
        ("B. Fernandes", "C. Eriksen",   85), ("B. Fernandes", "K. Mainoo", 62),
        ("C. Eriksen",   "T. Højlund",   70), ("K. Mainoo", "B. Fernandes", 55),
        ("T. Højlund",   "Casemiro",     90), ("M. Mount",     "B. Fernandes", 48),
        ("C. Eriksen",   "M. Mount",     40), ("Casemiro",     "C. Eriksen",   65),
        ("K. Mainoo",    "T. Højlund",   38),
    ]

    fig_net = go.Figure()
    max_w = max(c[2] for c in combos)

    for p1, p2, w in combos:
        if p1 not in positions_xy or p2 not in positions_xy: continue
        x1, y1 = positions_xy[p1]; x2, y2 = positions_xy[p2]
        fig_net.add_trace(go.Scatter(x=[x1, x2, None], y=[y1, y2, None], mode="lines",
                                     line=dict(color=f"rgba(88,166,255,{0.2 + 0.7 * (w/max_w):.2f})", width=max(1, int(w/15))),
                                     hoverinfo="skip", showlegend=False))
        
    node_colors = [COLORS["primary"], COLORS["accent"], COLORS["good"], COLORS["warn"], COLORS["bad"], "#d2a8ff"]
    for i, (player, (x, y)) in enumerate(positions_xy.items()):
        row = df[df["player"] == player]
        xt_val = row["xT_gen"].values[0] if len(row) else 0
        fig_net.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text",
                                     marker=dict(size=20 + xt_val * 60, color=node_colors[i % len(node_colors)], line=dict(color="#0d1117", width=2)),
                                     text=[player.split(".")[1].strip() if "." in player else player], textposition="bottom center",
                                     textfont=dict(color="#e6edf3", size=10), name=player))

    field_shapes = [
        dict(type="rect", x0=25, x1=95, y0=5, y1=100, line=dict(color="#30363d", width=1.5), fillcolor="rgba(22,27,34,0.0)"),
        dict(type="line", x0=25, x1=95, y0=52, y1=52, line=dict(color="#30363d", dash="dash", width=1)),
        dict(type="rect", x0=42, x1=78, y0=5, y1=20, line=dict(color="#30363d", width=1)),
        dict(type="rect", x0=42, x1=78, y0=84, y1=100, line=dict(color="#30363d", width=1)),
    ]
    fig_net.update_layout(**PLOTLY_THEME, height=500, showlegend=False, title="Red de pases — Mediocampo Manchester United", shapes=field_shapes)
    fig_net.update_xaxes(range=[20, 100], showgrid=False, zeroline=False, showticklabels=False)
    fig_net.update_yaxes(range=[0, 105], showgrid=False, zeroline=False, showticklabels=False)
    return fig_net

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
