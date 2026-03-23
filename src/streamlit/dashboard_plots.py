import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mplsoccer import Pitch

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

def graficar_heatmap_zonas(player_row):
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0d1117', line_color='#30363d')
    fig, ax = pitch.draw(figsize=(6, 4))
    fig.patch.set_facecolor('#0d1117')
    
    np.random.seed(int(hash(player_row["player"])) % 999)
    num_passes = int(player_row["prog_passes"] * 15) + 30
    
    # Bias distribution based on metrics
    x = np.random.normal(50 + player_row["vert_idx"] * 25, 20, num_passes)
    y = np.random.normal(40, 25, num_passes)
    x = np.clip(x, 0, 120); y = np.clip(y, 0, 80)
    
    pitch.hexbin(x, y, ax=ax, edgecolors='#0d1117', gridsize=(8, 6), cmap='magma', alpha=0.8)
    ax.set_title(f"Distribución de Pases — {player_row['player']}", color="#e6edf3", size=12, pad=5)
    return fig

def graficar_heatmap_xt(player_row):
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0d1117', line_color='#30363d', half=True)
    fig, ax = pitch.draw(figsize=(6, 4))
    fig.patch.set_facecolor('#0d1117')
    
    np.random.seed(int(hash(player_row["player"])) % 999 + 1)
    num_events = int(player_row["xT_gen"] * 120) + 5
    
    x = np.random.normal(95, 12, num_events)
    y = np.random.normal(40, 25, num_events)
    x = np.clip(x, 60, 120); y = np.clip(y, 0, 80)
    
    sizes = np.random.uniform(30, 180, num_events)
    pitch.scatter(x, y, s=sizes, c='#DA291C', edgecolors='#0d1117', alpha=0.75, ax=ax)
    ax.set_title(f"Nodos de xT — {player_row['player']}", color="#e6edf3", size=12, pad=5)
    return fig

def graficar_red_pases(df):
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#0d1117', line_color='#30363d')
    fig, ax = pitch.draw(figsize=(10, 6))
    fig.patch.set_facecolor('#0d1117')

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

    max_w = max(c[2] for c in combos)

    for p1, p2, w in combos:
        if p1 not in positions_xy or p2 not in positions_xy: continue
        x1, y1 = positions_xy[p1]; x2, y2 = positions_xy[p2]
        pitch.lines(x1, y1, x2, y2, lw=max(1.5, int((w/max_w)*8)), color='#58a6ff', 
                    alpha=0.3 + 0.6*(w/max_w), comet=True, transparent=True, zorder=2, ax=ax)
        
    for p, (x, y) in positions_xy.items():
        row = df[df["player"] == p]
        xt_val = row["xT_gen"].values[0] if len(row) else 0
        node_size = max(80, 200 + xt_val * 600)
        
        color = COLORS["primary"] if "Fernandes" in p or "Mainoo" in p else COLORS["accent"]
        pitch.scatter(x, y, s=node_size, c=color, edgecolors='#0d1117', linewidth=2, zorder=3, ax=ax)
        
        name = p.split(".")[1].strip() if "." in p else p
        ax.text(x, y - 5, name, color="#e6edf3", fontsize=9, ha='center', va='center', zorder=4)

    ax.set_title("Red de Flujo y Construcción (4-2-3-1)", color="#e6edf3", size=14, pad=10)
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
