import streamlit as st
st.set_page_config(page_title="Morrow's Moneyline", layout="wide")

import pandas as pd
from odds_api_scraper import load_odds_data
from simulated_betting_engine import init_ledger, run_auto_bet, show_bet_history
from gpt_assistant_panel import assistant_chat
from ocr_bet_uploader import upload_and_parse_bet, show_cover_status
from bet_history_ledger import get_current_bankroll, delete_bet

# Morrow Edge Calculation Function
def calculate_morrow_edge(df):
    if df.empty:
        return df

    df["EV"] = df["Price"].apply(lambda x: round((abs(x) / 100) * 0.05, 3) if isinstance(x, (int, float)) else 0)
    df["CLV"] = 0.02
    df["SimConfidence"] = 0.6
    df["Morrow Edge"] = (
        0.5 * df["EV"].fillna(0) +
        0.3 * df["CLV"].fillna(0) +
        0.2 * df["SimConfidence"].fillna(0)
    )
    return df

# Styling
st.markdown("""
    <style>
    * {
        font-family: 'Rubik', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize the bet history ledger
init_ledger()

# Sidebar
st.sidebar.image("https://emojicdn.elk.sh/%F0%9F%A4%A0", width=48)
st.sidebar.title("Morrow's Moneyline")
selection = st.sidebar.radio("Navigate", ["🏠 Dashboard", "🏀 NCAA Basketball", "🏈 NFL", "📈 Assistant", "🧾 Upload Bet", "📚 Bet History"])

# Load odds
df_odds, err = load_odds_data()
if not df_odds.empty:
    df_odds = calculate_morrow_edge(df_odds)

# Dashboard Views
if selection == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    if err:
        st.error(err)
    elif df_odds.empty:
        st.warning("No odds available.")
    else:
        st.subheader("🔍 Recommended Bets")
        if "Morrow Edge" in df_odds.columns:
            sorted_df = df_odds.sort_values(by="Morrow Edge", ascending=False).head(10)
        else:
            st.warning("⚠️ Morrow Edge not found in odds data. Displaying raw lines.")
            sorted_df = df_odds.head(10)

        for i, row in sorted_df.iterrows():
            with st.expander(f"{row['Matchup']} | {row['Market']} | {row['Team']}"):
                st.write(f"Odds: {row['Price']}")
                st.write(f"Bookmaker: {row['Bookmaker']}")
                st.write(f"Expected Value: {row.get('EV', 'N/A')}")
                st.write(f"Morrow Edge: {row.get('Morrow Edge', 'N/A')}")
                if st.button(f"✅ Add to Bet History", key=i):
                    run_auto_bet(pd.DataFrame([row]))

elif selection == "🏀 NCAA Basketball":
    st.title("🏀 NCAA Basketball")
    if df_odds.empty:
        st.info("Odds will display here when available.")
    else:
        st.dataframe(df_odds[df_odds["Matchup"].str.contains("vs")])

elif selection == "🏈 NFL":
    st.title("🏈 NFL")
    st.info("Odds for NFL games coming soon.")

elif selection == "📈 Assistant":
    assistant_chat()

elif selection == "🧾 Upload Bet":
    upload_and_parse_bet()
    show_cover_status()

elif selection == "📚 Bet History":
    st.title("📚 Bet History")
    msg, history = show_bet_history()
    if msg:
        st.warning(msg)
    else:
        st.dataframe(history)
        st.subheader("🗑️ Delete a Bet")
        delete_index = st.number_input("Row number to delete", min_value=0, step=1)
        if st.button("Delete Bet"):
            if delete_bet(delete_index):
                st.success("Bet deleted successfully!")
            else:
                st.error("Failed to delete bet.")
