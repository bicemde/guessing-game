import json
from questions import QUESTIONS

# The animal.json file was created with Chatgpt.

def load_animals():
    with open("animals.json", "r", encoding="utf-8") as f:
        animals_data = json.load(f)
        return animals_data["animals"]

# Filters the animal dataset based on a specific trait and its expected value (true or false)
def filter_animals(animals, trait, value):
    filtered_animals = []
    for animal in animals:
        if trait in animal["traits"]:
            correct_value = animal["traits"][trait]

        else:
            correct_value = animal[trait]

        if isinstance(correct_value, list): # Checks both nested traits and top-level animal attributes, supporting single values as well as lists and returns only the matching animals.
            for val in correct_value:
                if val == value:
                    filtered_animals.append(animal)
                    break

        elif correct_value == value:
            filtered_animals.append(animal)

    return filtered_animals
                       

# Applies all the user's answers to the animal dataset.

def filter_answers(animals, answers):
    possible_animals = animals
    for trait, value in answers.items():
        possible_animals = filter_animals(possible_animals, trait, value)
    return possible_animals



# Gets the next question from the QUESTIONS dictionary.
# Uses the question_index to access the corresponding key (trait) and retrieves its question text. 
# Returns both the trait and the question so the answer can later be matched to the correct animal attribute. 
# Returns None when all predefined questions are used.
def call_current_question(question_index):
    question_keys = list(QUESTIONS.keys())

    if question_index < len(question_keys):
        trait = question_keys[question_index]

        return {
            "trait": trait,
            "question": QUESTIONS[trait]
        }

    return None

# Stores the user's answer (True/False) in the answers dictionary
def save_answer(answers, trait, user_answer):
    answers[trait] = user_answer
    return answers


# Creates a record for a completed game, storing the animal name, the total number of questions asked, and whether the guess was correct.

def save_game_result(game_history, animal, questions_asked, success):
    game_result = {
        "animal": animal,
        "questions_asked": questions_asked,
        "success": success
    }

    game_history.append(game_result) # Appends the result to the game history for later use on the Stats page.
    return game_history

