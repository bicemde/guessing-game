# Animal Guessing Game

An interactive animal guessing game built with **Python, Streamlit and a Large Language Model (LLM)**.

The application combines a predefined question-based system with an LLM to identify an animal the user has in mind. It also tracks game results and displays statistics.

## Features

- **Play:** An interactive animal guessing game.
- **Rule-based questions:** The game starts with five predefined yes/no questions to narrow down the possible animals.
- **LLM integration:** If multiple possible animals remain after the predefined questions, the LLM generates additional questions to distinguish between the remaining candidates and make a final guess.
- **Game statistics:** Tracks the number of games played, successful guesses, and questions asked per game.
- **Stats page:** Displays game history, accuracy, and visualizations of game results.

## How It Works

The game follows a hybrid approach, combining traditional Python logic with LLM-based question generation.

1. The user thinks of an animal and starts the game.
2. The application asks five predefined yes/no questions, such as:
   - Can your animal fly?
   - Can your animal swim?
   - Does your animal lay eggs?
   - Is your animal domesticated?
   - Is your animal active at night?
3. Python filters the animal dataset based on the user's answers and narrows down the possible candidates.
4. If only one candidate remains, the application makes its guess.
5. If multiple candidates remain after the five predefined questions, the LLM takes over. It generates additional questions based on the remaining candidates and uses the user's answers to narrow them down further.
6. The application presents its final guess and records the game result.


## Installation

### 1. Clone the repository

```bash
git clone https://github.com/bicemde/guessing-game.git
cd guessing-game
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

The LLM integration requires an API key for the university's LiteLLM endpoint.

Create a file named `.env` in the project root directory:

```env
LLM_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key.

**Important:** Never commit your `.env` file or share your API key publicly. Make sure `.env` is included in `.gitignore`.

### 5. Run the application

```bash
streamlit run play.py
```

The application will open in your browser.


## Notes

- The game initially relies on a predefined set of questions and a structured animal dataset.
- The LLM is only used when the predefined questions are insufficient to identify a single animal.
- A valid API key and access to the university's LLM endpoint are required for the LLM functionality.
- Game statistics are stored in the Streamlit session state and are therefore not permanently saved across separate sessions or application restarts.
