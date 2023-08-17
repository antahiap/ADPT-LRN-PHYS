import json
import sys
from openai_api import OpenAIApi

def get_questions():
    """Get questions from the json file"""
    questions = {}
    with open("data/datascience-questions.json", "r") as f:
        json_questions = json.load(f)
        for json_question in json_questions:
            questions[json_question["domain"]] = json_question["questions"]
    return questions

api = OpenAIApi("gpt-3.5-turbo")
def evaluate_answer(question, answer):
    prompt = f"Grade the answer from 1 to 10 to that question: \nQ: {question}\nA: {answer}\n"
    content, _, _ = api.call_api(prompt)
    return content