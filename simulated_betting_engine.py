# simulated_betting_engine.py

import pandas as pd
from bet_history_ledger import update_ledger

LEDGER_FILE = "bet_history.csv"

def init_ledger():
    try:
        pd.read_csv(LEDGER_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "Date", "Sport", "Matchup", "Wager", "Odds", "Stake", "Expected Value",
            "Morrow Edge", "Kelly %", "Result", "Profit", "CLV", "Bookmaker"
        ])
        df.to_csv(LEDGER_FILE, index=False)

def run_auto_bet(df):
    for _, row in df.iterrows():
        if row.get("Recommended", False):  # Only auto-bet marked bets
            bet_data = {
                "Date": row.get("Game Time", ""),
                "Sport": row.get("Sport", "NCAAB"),
                "Matchup": row.get("Matchup", ""),
                "Wager": f"{row.get('Team', '')} ({row.get('Market', '')})",
                "Odds": row.get("Price", ""),
                "Stake": row.get("Stake", 0.0),
                "Expected Value": row.get("EV", 0.0),
                "Morrow Edge": row.get("Morrow Edge", 0.0),
                "Kelly %": row.get("Kelly %", 0.0),
                "Result": "Pending",
                "Profit": 0.0,
                "CLV": row.get("CLV", 0.0),
                "Bookmaker": row.get("Bookmaker", "")
            }
            update_ledger(bet_data)

def show_bet_history():
    try:
        df = pd.read_csv(LEDGER_FILE)
        if df.empty:
            return "No bets placed yet.", pd.DataFrame()
        return "", df
    except Exception as e:
        return f"Error reading bet history: {str(e)}", pd.DataFrame()