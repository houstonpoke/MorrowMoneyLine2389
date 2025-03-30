import requests
import pandas as pd
import datetime

token = "a717005e71de111fa6ea4dcc15464caf"

def load_odds_data():
    url = "https://api.the-odds-api.com/v4/sports/basketball_ncaab/odds"
    params = {
        "apiKey": token,
        "regions": "us",
        "markets": "spreads,h2h,totals",
        "oddsFormat": "american"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return pd.DataFrame(), f"Failed to fetch odds: HTTP {response.status_code}"

        data = response.json()

        rows = []
        for game in data:
            home = game.get("home_team", "")
            away = game.get("away_team", "")
            commence = game.get("commence_time", "")
            matchup = f"{away} vs {home}"

            for bookmaker in game.get("bookmakers", []):
                book_name = bookmaker.get("title", "")
                for market in bookmaker.get("markets", []):
                    market_type = market.get("key", "")
                    for outcome in market.get("outcomes", []):
                        rows.append({
                            "Matchup": matchup,
                            "Bookmaker": book_name,
                            "Market": market_type,
                            "Team": outcome.get("name", ""),
                            "Price": outcome.get("price", ""),
                            "Point": outcome.get("point", ""),
                            "Game Time": commence
                        })

        df = pd.DataFrame(rows)
        df["Scraped At"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        df_grouped = df.sort_values(by=["Matchup", "Market", "Bookmaker"]).groupby(
            ["Matchup", "Market", "Team"], as_index=False
        ).first()

        return df_grouped, None

    except Exception as e:
        print("⚠️ Exception in load_odds_data:", e)
        return pd.DataFrame(), str(e)