
import streamlit as st
import game
from questions import QUESTIONS
import llm

# Initialize and manage the game state using streamlit's session_state
# This keeps important game information, like user answers, remaining
# animal candidates, questions, and game history, available across reruns.
# Each variable is initialized only once to avoid resetting the game state.

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

if "guess_result" not in st.session_state:
    st.session_state.guess_result = None

if "llm_candidates" not in st.session_state:
    st.session_state.llm_candidates = None

if "llm_question" not in st.session_state:
    st.session_state.llm_question = None

if "llm_asked" not in st.session_state:
    st.session_state.llm_asked = []

if "game_history" not in st.session_state:
    st.session_state.game_history = []

if "game_recorded" not in st.session_state:
    st.session_state.game_recorded = False

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
# Records the result of a completed game, including the guessed animal, the total number of questions asked and whether the guess was correct.
# The game_recorded flag prevent the same game from being added to the
# history multiple times during Streamlit reruns:

def record_current_game(animal, success):
    if not st.session_state.game_recorded:
        questions_asked = (
            len(st.session_state.answers)
            + len(st.session_state.llm_asked)
        )

        game.save_game_result(
            st.session_state.game_history,
            animal,
            questions_asked,
            success
        )

        st.session_state.game_recorded = True

def reset_game(): 
    st.session_state.game_started = False
    st.session_state.answers = {}
    st.session_state.question_index = 0
    st.session_state.possible_animals = st.session_state.animals.copy()
    st.session_state.guess_result = None 
    st.session_state.llm_candidates = None
    st.session_state.llm_question = None
    st.session_state.llm_asked = []
    st.session_state.game_recorded = False


def set_guess_result(value):
    st.session_state.guess_result = value


# Displays the welcome screen of the game.
# Custom HTML and CSS stylings are used to create a visually appealing user interface.

def game_initialize():

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

    col1, col2, col3 = st.columns([1, 1, 1]) # centers the 'play' button

    with col2:
        if st.button("PLAY 🐾", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()


if not st.session_state.game_started:
    game_initialize()
else:

    # Checks whether there are predefined questions remaining.
    if st.session_state.question_index < len(QUESTIONS): 
        # retrieves the current question based on the question index:
        current_question = game.call_current_question( 
            st.session_state.question_index
    )
        # and displays it in the center of the page with custom styling.
        st.markdown( 
            f"""
            <h2 style='text-align: center; color: #C45B83;'>
                {current_question["question"]}
            </h2>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)  # Creates two columns for the yes/no buttons 

        #custom CSS styling to Streamlit buttons
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

        # Stores the user's Yes - No answer for the current question
        # updates the question index, and reruns the app to display the next question
        with col1:
            if st.button("YES", use_container_width=True):
                st.session_state.answers[current_question["trait"]] = True
                st.session_state.question_index += 1
                st.rerun()

        with col2:
            if st.button("NO", use_container_width=True):
                st.session_state.answers[current_question["trait"]] = False
                st.session_state.question_index += 1
                st.rerun()

    # Once all predefined questions have been answered, filters the animal
    # dataset using the user's answers to identify the remaining candidates.
    # Initializes the LLM candidate list with the names of these animals
    # and prepares the final guessing stage
    else:
        possible_animals = game.filter_answers(st.session_state.animals, st.session_state.answers)

        if st.session_state.llm_candidates is None:
            st.session_state.llm_candidates = [a["name"] for a in possible_animals]
        names = st.session_state.llm_candidates

        guess = None

        # If only one animal remains, it is selected as the final guess
        if len(names) == 1:
            guess = names[0]

        # If multiple candidates remain, the LLM generates an additional question to distinguish between them. 
        # The question is generated only once and displayed to the user while the LLM is processing.
        elif len(names) > 1:
            if st.session_state.llm_question is None:
                with st.spinner("I am thinking.."):
                    st.session_state.llm_question = llm.make_question(names, st.session_state.llm_asked)


            q = st.session_state.llm_question
            st.markdown(f"<h2 style='text-align:center; color:#C45B83;'>{q}</h2>", unsafe_allow_html=True)

            # Processes the user's Yes-No response to an LLM-generated question. The LLM filters the remaining animal candidates based on the answer.
            # The question is added to the game history, the current LLM question is reset and the app reruns to continue the guessing process.
            c1, c2 = st.columns(2)
            with c1:
                if st.button("YES", key="llm_yes", use_container_width=True):
                    st.session_state.llm_candidates = llm.filter_candidates(names, q, True)
                    st.session_state.llm_asked.append(q)
                    st.session_state.llm_question = None
                    st.rerun()
            with c2:
                if st.button("NO", key="llm_no", use_container_width=True):
                    st.session_state.llm_candidates = llm.filter_candidates(names, q, False)
                    st.session_state.llm_asked.append(q)
                    st.session_state.llm_question = None
                    st.rerun()

        # the situation where the application cannot identify the animal.
        # Asks the user to enter the correct animal name and records the game as an unsuccessful guess, allowing the game history to be updated.
        else:
            st.markdown("Sorry! I couldn't guess your animal! ")
            st.write("What was the animal you were thinking of?")
            with st.form("animal_form"):
                animal_name = st.text_input("Your animal:")

                submitted = st.form_submit_button("Submit 🐾")

                if submitted:
                    if animal_name.strip():
                        record_current_game(animal_name.strip(), False)
                        st.success(f"Ahh, it was a {animal_name}! Thanks for teaching!")
                else:
                    st.warning("Please enter an animal name!")

        # shows the application's final animal guess and asks the user to confirm whether it is correct.
        if guess is not None:
            if st.session_state.guess_result is None:
                st.markdown(f"## Is your animal a {guess}? 🐾")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("YES", key="guess_yes", use_container_width=True):
                        record_current_game(guess, True)
                        st.session_state.guess_result = True
                        st.rerun()
                with c2:
                    if st.button("NO", key="guess_no", use_container_width=True):
                        record_current_game(guess, False)
                        st.session_state.guess_result = False
                        st.rerun()
            elif st.session_state.guess_result is True:
                st.markdown("# YAY! 🥳")
                giphy_url = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmdob2xjcTR0dGZmNWkzcW1zNjQ3ZmF4djMwNGw0aWt3OTlleG16eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT5LMQ8rHYTDGFG07e/giphy.gif"
                st.image(giphy_url, width=400)
            else:
                giphy_url = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXU4cm44MXFyOTh0YzN0aTlnM3d0am82dnNxbTVrdGUzdGlucmJsOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT5LMLMPdRh2VRNVLi/giphy.gif"
                st.image(giphy_url, width=400)






# The Reset button: starts a new game by clearing the current game state
# The Stats button: navigates to the statistics page.

left, middle, right = st.columns([2, 2, 2])

with middle:
    col1, col2 = st.columns(2)

    with col1:
        st.button("Reset", on_click=reset_game)

    with col2:
        if st.button("Stats"):
            st.switch_page("pages/stats.py")

            
            




        
# to do :
# reset button at the end
# stats button
# can be added animal image - with ai
