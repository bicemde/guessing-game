import streamlit as st



st.header("Guess the Animal!")
st.title("🐶🐱🐭🐻🐼🦁🐨🐵🐯")

st.markdown("""
Welcome to my animal guessing game and my very first Streamlit project! 🐾

Now, think of an animal and I'll try to guess what it is. :rainbow[Let's play!]
"""
)


guess = st.text_input(
    "Write your guess here!",
)