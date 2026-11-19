import json
from questions import QUESTIONS

# The animal.json file was created with Chatgpt.

def load_animals():
    with open("animals.json", "r", encoding="utf-8") as f:
        animals_data = json.load(f)
        return animals_data["animals"]


def filter_animals(animals, trait, value):
    filtered_animals = []
    for animal in animals:
        if trait in animal["traits"]:
            correct_value = animal["traits"][trait]

        else:
            correct_value = animal[trait]

        if isinstance(correct_value, list):
            for val in correct_value:
                if val == value:
                    filtered_animals.append(animal)
                    break

        elif correct_value == value:
            filtered_animals.append(animal)

    return filtered_animals
                       


answers = {}

def filter_answers(animals, answers):
    possible_animals = animals
    for trait, value in answers.items():
        possible_animals = filter_animals(possible_animals, trait, value)
    return possible_animals




def call_current_question(question_index):
    question_keys = list(QUESTIONS.keys())

    if question_index < len(question_keys):
        trait = question_keys[question_index]

        return {
            "trait": trait,
            "question": QUESTIONS[trait]
        }

    return None


def save_answer(answers, trait, user_answer):
    answers[trait] = user_answer
    return answers


