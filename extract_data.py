import pandas as pd, numpy as np, os

def dump_passing():
    np.random.seed(42)

    squad = [
        {"player": "B. Fernandes", "pos": "CAM", "apps": 32, "age": 30, "pass_acc": 88.4, "prog_passes": 5.1, "key_passes": 2.8, "vert_idx": 0.78, "xA": 8.2,  "losses": 1.9, "deep_prog": 3.1, "xT_gen": 0.42, "resil": 0.8},
        {"player": "C. Eriksen",   "pos": "CM",  "apps": 24, "age": 32, "pass_acc": 91.2, "prog_passes": 4.8, "key_passes": 1.9, "vert_idx": 0.85, "xA": 4.1,  "losses": 1.1, "deep_prog": 2.7, "xT_gen": 0.31, "resil": 0.6},
        {"player": "K. Mainoo",    "pos": "CM",  "apps": 28, "age": 19, "pass_acc": 85.7, "prog_passes": 4.0, "key_passes": 1.6, "vert_idx": 0.64, "xA": 3.2,  "losses": 2.4, "deep_prog": 1.9, "xT_gen": 0.24, "resil": 0.95},
        {"player": "T. Højlund",   "pos": "ST",  "apps": 20, "age": 22, "pass_acc": 83.1, "prog_passes": 3.5, "key_passes": 1.2, "vert_idx": 0.58, "xA": 2.0,  "losses": 2.8, "deep_prog": 1.5, "xT_gen": 0.18, "resil": 0.7},
        {"player": "M. Mount",     "pos": "CM",  "apps": 18, "age": 25, "pass_acc": 82.8, "prog_passes": 2.9, "key_passes": 1.0, "vert_idx": 0.52, "xA": 1.8,  "losses": 3.1, "deep_prog": 1.2, "xT_gen": 0.14, "resil": 0.65},
        {"player": "Casemiro",     "pos": "CDM", "apps": 26, "age": 32, "pass_acc": 86.5, "prog_passes": 3.2, "key_passes": 0.8, "vert_idx": 0.45, "xA": 1.5,  "losses": 2.2, "deep_prog": 0.9, "xT_gen": 0.11, "resil": 0.4},
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
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/passing_players.csv", index=False)
    df_t.to_csv("data/raw/passing_timeline.csv", index=False)
    print("Mocks in place.")

if __name__ == "__main__": dump_passing()
