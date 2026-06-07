from pybaseball import statcast_batter
import pandas as pd
import numpy as np
from datetime import datetime

def get_statcast_data(start_date, end_date):
    df = statcast_batter(start_date, end_date)
    return df


def compute_metrics(df):
    if df is None or df.empty:
        return {
            "avg_exit_velocity": 0,
            "hard_hit_pct": 0,
            "barrel_pct": 0,
            "power_index": 0
        }

    df = df.copy()

    # Exit velocity
    avg_ev = float(df["launch_speed"].mean()) if "launch_speed" in df else 0

    # Hard hit %
    hard_hit = float((df["launch_speed"] >= 95).mean() * 100) if "launch_speed" in df else 0

    # Barrel proxy
    if "launch_speed" in df and "launch_angle" in df:
        barrels = df[(df["launch_speed"] >= 98) & (df["launch_angle"].between(15, 35))]
        barrel_pct = float(len(barrels) / len(df) * 100) if len(df) > 0 else 0
    else:
        barrel_pct = 0

    # Simple power index
    power_index = round((avg_ev * 0.4) + (hard_hit * 0.3) + (barrel_pct * 0.3), 2)

    return {
        "avg_exit_velocity": avg_ev,
        "hard_hit_pct": hard_hit,
        "barrel_pct": barrel_pct,
        "power_index": power_index
    }


def build_statcast_payload(player_id, start_date, end_date):
    df = get_statcast_data(start_date, end_date)
    metrics = compute_metrics(df)

    return {
        "player_id": player_id,
        "start_date": start_date,
        "end_date": end_date,
        "metrics": metrics,
        "generated_at": datetime.utcnow().isoformat()
    }
