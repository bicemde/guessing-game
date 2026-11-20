import streamlit as st
import pandas as pd



st.title("Animal Guessing Game Statistics") # Page title


game_history = st.session_state.get("game_history", []) # Load game history


df = pd.DataFrame(game_history) # Create DataFrame


# Calculate statistics

total_games = len(game_history) # Total number of games

correct_games = 0 # Number of correct guesses

for game in game_history:
    if game.get("success") is True:
        correct_games += 1

# Calculate accuracy
if total_games > 0:
    accuracy = (correct_games / total_games) * 100
else:
    accuracy = 0.0



# Display statistics

st.subheader("Game Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Games",
        value=total_games
    )

with col2:
    st.metric(
        label="Accuracy",
        value=f"{accuracy:.2f}%" if total_games > 0 else "N/A"
    )

with col3:
    st.metric(
        label="Correct Guesses",
        value=correct_games
    )



# Display game history

st.subheader("Game History")

if total_games > 0:
    st.dataframe(df)
else:
    st.info("No games played yet.")



# Animal Guess Frequency in Bar Chart

st.subheader("How many times was each animal guessed?")

if total_games > 0 and "animal" in df.columns:

    guess_frequency = df["animal"].dropna().value_counts()

    if not guess_frequency.empty:
        st.bar_chart(
        guess_frequency,
        color="#C45B83"
)
    else:
        st.info("No animals have been guessed yet.")

else:
    st.info("Play a game to see the chart!")



# Back to game and play again button

if st.button("Back to Game"):
    st.switch_page("play.py")
