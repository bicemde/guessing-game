
import streamlit as st
import game
from questions import QUESTIONS

if "game_started" not in st.session_state: # session memory of the streamlit: allows us to preserve the values of variables when the pages or the application are re-run
    st.session_state.game_started = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "animals" not in st.session_state:
    st.session_state.animals = game.load_animals()

if "possible_animals" not in st.session_state:
    st.session_state.possible_animals = st.session_state.animals.copy()

# background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FCE4EC;
    }
    </style>
    """,
    unsafe_allow_html=True  # to make the html code work properly in streamlit
)


if not st.session_state.game_started:

    st.markdown(
        """
        <h1 style='text-align: center; color: #FF8C69; font-size: 55px;'>
            Guess the Animal! 🐾
        </h1>
        """,
        unsafe_allow_html=True 
    )

    st.markdown(
        """
        <h1 style='text-align: center; font-size: 65px;'>
            🐶 🐱 🐭 🐻 🐼 🦁 🐨 🐵
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='text-align: center; font-size: 22px;'>
            Welcome to the animal guessing game and our very first Streamlit project! 🐾
            <br><br>
            Now, think of an animal and I'll try to guess what it is.
            <br>
            <span style='color: #D96C9D; font-weight: bold;'>
                Let's play! ♡
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("PLAY 🐾", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()


else:

    current_question = game.call_current_question(
        st.session_state.question_index
    )
    if st.session_state.question_index < len(QUESTIONS):

        current_question = game.call_current_question(
            st.session_state.question_index
    )
    
        st.markdown(
            f"""
            <h2 style='text-align: center; color: #C45B83;'>
                {current_question["question"]}
            </h2>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        st.markdown("""
        <style>
        .stButton > button {
            background-color: #F8BBD0;
            color: #7B3655;
            border-radius: 15px;
            border: none;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
        }

        .stButton > button:hover {
            background-color: #F48FB1;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)


        with col1:
            if st.button("YES 💗", use_container_width=True):
                st.session_state.answers[current_question["trait"]] = True
                st.session_state.question_index += 1
                st.rerun()

        with col2:
            if st.button("NO 💗", use_container_width=True):
                st.session_state.answers[current_question["trait"]] = False
                st.session_state.question_index += 1
                st.rerun()



    else: 
        possible_animals = game.filter_answers(st.session_state.animals, st.session_state.answers)
        if possible_animals:
            st.markdown("### My guess is:")
            st.markdown(f"## {possible_animals[0]['name']} 🐾")
    
        else:
            st.write("Sorry! I couldn't guess your animal! You can write your animal here:")

        

# reset button at the end
# stats button
# can be added animal image - with ai
