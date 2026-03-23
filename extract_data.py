import pandas as pd, numpy as np, os

def dump_passing():
    np.random.seed(42)

    squad = [
        # Forwards / Wingers
        {"player": "M. Rashford",  "pos": "LW",  "apps": 30, "age": 27, "pass_acc": 76.5, "prog_passes": 2.1, "key_passes": 1.4, "vert_idx": 0.45, "xA": 3.0,  "losses": 4.1, "deep_prog": 1.1, "xT_gen": 0.28, "duels_won": 41.0, "interceptions": 0.2, "recoveries": 1.5, "resil": 0.6},
        {"player": "A. Garnacho",  "pos": "RW",  "apps": 34, "age": 20, "pass_acc": 74.1, "prog_passes": 1.8, "key_passes": 1.1, "vert_idx": 0.48, "xA": 4.5,  "losses": 4.5, "deep_prog": 1.5, "xT_gen": 0.35, "duels_won": 43.5, "interceptions": 0.3, "recoveries": 2.1, "resil": 0.5},
        {"player": "T. Højlund",   "pos": "ST",  "apps": 20, "age": 22, "pass_acc": 83.1, "prog_passes": 3.5, "key_passes": 1.2, "vert_idx": 0.58, "xA": 2.0,  "losses": 2.8, "deep_prog": 1.5, "xT_gen": 0.18, "duels_won": 48.0, "interceptions": 0.1, "recoveries": 1.0, "resil": 0.7},
        {"player": "A. Diallo",    "pos": "RW",  "apps": 22, "age": 22, "pass_acc": 81.2, "prog_passes": 2.5, "key_passes": 1.5, "vert_idx": 0.55, "xA": 3.1,  "losses": 3.2, "deep_prog": 1.4, "xT_gen": 0.28, "duels_won": 45.1, "interceptions": 0.5, "recoveries": 2.5, "resil": 0.7},
        {"player": "J. Zirkzee",   "pos": "ST",  "apps": 18, "age": 23, "pass_acc": 79.5, "prog_passes": 2.8, "key_passes": 1.1, "vert_idx": 0.60, "xA": 1.5,  "losses": 3.8, "deep_prog": 1.0, "xT_gen": 0.15, "duels_won": 50.2, "interceptions": 0.3, "recoveries": 1.8, "resil": 0.6},
        {"player": "Antony",       "pos": "RW",  "apps": 11, "age": 24, "pass_acc": 78.0, "prog_passes": 1.5, "key_passes": 0.8, "vert_idx": 0.40, "xA": 1.1,  "losses": 3.0, "deep_prog": 0.9, "xT_gen": 0.12, "duels_won": 51.5, "interceptions": 0.6, "recoveries": 3.2, "resil": 0.5},
        # Midfielders
        {"player": "B. Fernandes", "pos": "CAM", "apps": 32, "age": 30, "pass_acc": 88.4, "prog_passes": 5.1, "key_passes": 2.8, "vert_idx": 0.78, "xA": 8.2,  "losses": 1.9, "deep_prog": 3.1, "xT_gen": 0.42, "duels_won": 47.0, "interceptions": 0.9, "recoveries": 4.5, "resil": 0.8},
        {"player": "C. Eriksen",   "pos": "CM",  "apps": 24, "age": 32, "pass_acc": 91.2, "prog_passes": 4.8, "key_passes": 1.9, "vert_idx": 0.85, "xA": 4.1,  "losses": 1.1, "deep_prog": 2.7, "xT_gen": 0.31, "duels_won": 42.1, "interceptions": 0.8, "recoveries": 3.8, "resil": 0.6},
        {"player": "K. Mainoo",    "pos": "CM",  "apps": 28, "age": 19, "pass_acc": 85.7, "prog_passes": 4.0, "key_passes": 1.6, "vert_idx": 0.64, "xA": 3.2,  "losses": 2.4, "deep_prog": 1.9, "xT_gen": 0.24, "duels_won": 58.4, "interceptions": 1.2, "recoveries": 5.1, "resil": 0.95},
        {"player": "M. Ugarte",    "pos": "CDM", "apps": 22, "age": 23, "pass_acc": 89.1, "prog_passes": 3.4, "key_passes": 0.6, "vert_idx": 0.41, "xA": 0.8,  "losses": 1.2, "deep_prog": 0.8, "xT_gen": 0.08, "duels_won": 65.2, "interceptions": 2.8, "recoveries": 8.5, "resil": 0.85},
        {"player": "Casemiro",     "pos": "CDM", "apps": 26, "age": 32, "pass_acc": 86.5, "prog_passes": 3.2, "key_passes": 0.8, "vert_idx": 0.45, "xA": 1.5,  "losses": 2.2, "deep_prog": 0.9, "xT_gen": 0.11, "duels_won": 59.8, "interceptions": 1.9, "recoveries": 6.4, "resil": 0.4},
        # Defenders
        {"player": "L. Martinez",  "pos": "CB",  "apps": 29, "age": 26, "pass_acc": 93.4, "prog_passes": 6.5, "key_passes": 0.4, "vert_idx": 0.88, "xA": 0.5,  "losses": 0.8, "deep_prog": 4.2, "xT_gen": 0.15, "duels_won": 66.4, "interceptions": 2.4, "recoveries": 6.1, "resil": 0.9},
        {"player": "D. Dalot",     "pos": "RB",  "apps": 35, "age": 25, "pass_acc": 84.1, "prog_passes": 4.2, "key_passes": 1.2, "vert_idx": 0.61, "xA": 2.5,  "losses": 1.8, "deep_prog": 2.1, "xT_gen": 0.22, "duels_won": 55.2, "interceptions": 1.8, "recoveries": 5.4, "resil": 0.85},
        {"player": "M. de Ligt",   "pos": "CB",  "apps": 26, "age": 25, "pass_acc": 91.0, "prog_passes": 3.8, "key_passes": 0.2, "vert_idx": 0.55, "xA": 0.2,  "losses": 0.6, "deep_prog": 1.8, "xT_gen": 0.05, "duels_won": 71.0, "interceptions": 1.5, "recoveries": 4.8, "resil": 0.75},
        {"player": "N. Mazraoui",  "pos": "LB",  "apps": 18, "age": 26, "pass_acc": 86.5, "prog_passes": 3.9, "key_passes": 0.9, "vert_idx": 0.65, "xA": 1.8,  "losses": 1.5, "deep_prog": 1.9, "xT_gen": 0.18, "duels_won": 58.1, "interceptions": 1.6, "recoveries": 5.0, "resil": 0.8},
        {"player": "H. Maguire",   "pos": "CB",  "apps": 15, "age": 31, "pass_acc": 85.2, "prog_passes": 3.1, "key_passes": 0.1, "vert_idx": 0.40, "xA": 0.1,  "losses": 1.0, "deep_prog": 1.2, "xT_gen": 0.04, "duels_won": 75.8, "interceptions": 1.2, "recoveries": 4.1, "resil": 0.5},
        {"player": "L. Shaw",      "pos": "LB",  "apps": 12, "age": 29, "pass_acc": 87.1, "prog_passes": 4.1, "key_passes": 1.3, "vert_idx": 0.70, "xA": 2.2,  "losses": 1.1, "deep_prog": 2.5, "xT_gen": 0.20, "duels_won": 62.0, "interceptions": 1.4, "recoveries": 5.8, "resil": 0.8},
        {"player": "J. Evans",     "pos": "CB",  "apps": 10, "age": 36, "pass_acc": 82.5, "prog_passes": 2.5, "key_passes": 0.1, "vert_idx": 0.35, "xA": 0.0,  "losses": 0.5, "deep_prog": 0.5, "xT_gen": 0.02, "duels_won": 68.5, "interceptions": 1.8, "recoveries": 3.9, "resil": 0.4},
        # GK
        {"player": "A. Onana",     "pos": "GK",  "apps": 36, "age": 28, "pass_acc": 72.4, "prog_passes": 4.5, "key_passes": 0.0, "vert_idx": 0.95, "xA": 0.0,  "losses": 5.2, "deep_prog": 5.5, "xT_gen": 0.02, "duels_won": 80.0, "interceptions": 0.1, "recoveries": 8.0, "resil": 0.65},
    ]

    out = []
    # easy opponents
    for b in squad:
        r = b.copy()
        r["opponent_tier"] = "Resto PL"
        r["pass_acc"] = min(98, r["pass_acc"] + 2.0)
        r["xT_gen"] *= 1.15
        r["losses"] = max(0, r["losses"] - 0.5)
        out.append(r)

    # top tier
    for b in squad:
        r = b.copy()
        r["opponent_tier"] = "Top 6"
        p = 1 - r.pop("resil")
        r["pass_acc"] -= (10 * p)
        r["xT_gen"] -= (r["xT_gen"] * 0.4 * p)
        r["losses"] += (3 * p)
        out.append(r)
        
    df = pd.DataFrame([ {k:v for k,v in x.items() if k != "resil"} for x in out ])

    # series
    logs = []
    for d in range(1, 33):
        for x in out:
            n = np.random.normal(0, 0.04)
            logs.append({"matchday": d, "player": x["player"], "pass_acc": max(70, min(98, x["pass_acc"] + n * 100)), "prog_passes": max(0, x["prog_passes"] + np.random.normal(0, 0.6)), "xT_gen": max(0, x["xT_gen"] + np.random.normal(0, 0.05))})
            
    df_t = pd.DataFrame(logs)

    team_data = [{"team": "Manchester Utd", "poss": 52.1, "pass_acc": 84.5, "prog_passes": 42.1, "xT_gen": 1.48}]
    pl_teams = [
        ("Arsenal", 60.5, 88.2, 55.4, 2.1), ("Man City", 65.2, 90.1, 62.3, 2.45), ("Liverpool", 61.0, 86.5, 58.1, 2.2),
        ("Aston Villa", 54.2, 85.0, 45.2, 1.6), ("Tottenham", 59.8, 86.8, 52.1, 1.9), ("Chelsea", 58.5, 87.1, 50.4, 1.85),
        ("Newcastle", 51.0, 82.5, 41.2, 1.55), ("West Ham", 45.2, 79.8, 32.5, 1.1), ("Brighton", 58.1, 86.2, 49.8, 1.7),
        ("Bournemouth", 48.5, 80.1, 38.4, 1.25), ("Fulham", 51.5, 83.0, 43.1, 1.3), ("Wolves", 47.2, 81.5, 36.5, 1.15),
        ("Crystal Palace", 46.5, 80.8, 35.1, 1.2), ("Everton", 42.1, 76.5, 29.8, 0.95), ("Brentford", 45.8, 79.2, 33.4, 1.05),
        ("N. Forest", 41.5, 75.8, 28.5, 0.9), ("Luton", 39.2, 72.1, 25.4, 0.75), ("Burnley", 44.5, 78.5, 31.2, 0.85),
        ("Sheff Utd", 36.5, 71.2, 22.1, 0.65)
    ]
    for t in pl_teams: team_data.append({"team": t[0], "poss": t[1], "pass_acc": t[2], "prog_passes": t[3], "xT_gen": t[4]})
    df_teams = pd.DataFrame(team_data)

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/passing_players.csv", index=False)
    df_t.to_csv("data/raw/passing_timeline.csv", index=False)
    df_teams.to_csv("data/raw/pl_teams.csv", index=False)
    print("Mocks in place.")

if __name__ == "__main__": dump_passing()
