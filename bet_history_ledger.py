import pandas as pd
from datetime import datetime

LEDGER_FILE = "bet_history.csv"

def update_ledger(bet_data):
    try:
        df = pd.read_csv(LEDGER_FILE)
    except FileNotFoundError:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([bet_data])], ignore_index=True)
    df.to_csv(LEDGER_FILE, index=False)

def get_current_bankroll(starting_bankroll=500):
    try:
        df = pd.read_csv(LEDGER_FILE)
        profit = df["Profit"].sum()
        return starting_bankroll + profit
    except Exception:
        return starting_bankroll

def delete_bet(index):
    try:
        df = pd.read_csv(LEDGER_FILE)
        df = df.drop(index)
        df.to_csv(LEDGER_FILE, index=False)
        return True
    except Exception as e:
        print("Error deleting bet:", e)
        return False