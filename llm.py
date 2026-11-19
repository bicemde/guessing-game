import os
import re
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("LLM_API_KEY")
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=api_key
)

def ask(prompt): # llm is gonna ask questions if there are stil more than one animal
    try:
        response = client.chat.completions.create(model="Ornith-1.5-35B-A3B", max_tokens=1000, temperature = 0.2, messages=[{"role": "user", "content": prompt}])
        content = response.choices[0].message.content
        if content is None:
            print("LLM returned empty content. finish_reason:", response.choices[0].finish_reason)
            return None
        return content.strip()
    except Exception as e:
        print("LLM error:", e)
        return None
    

def make_question(candidates, asked):
    prompt = f"""
Animal guessing game. Candidates {", ".join(candidates)}.
Questions already asked_: {asked or "none"}.
Write "one" yes/no question that splits these candidates into two groups..
Reply with only the question.
"""
    return ask(prompt) or "Does it live in water?"

def filter_candidates(candidates,question,answer):
    prompt = f"""
Animal guessing game. Candidates {", ".join(candidates)}.
Question: {question}
The player answered: {"YES" if answer else "NO"}.
List only tha candidates that are still possible, separated by commas.
Reply with only tha names.
"""
    text = ask(prompt)
    if text is None:
        return candidates
    text = text.lower()
    left = [c for c in candidates if c.lower() in text]
    return left or candidates 