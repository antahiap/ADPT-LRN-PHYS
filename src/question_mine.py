import json
import time
import re

from opena_api import OpenAIApi

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATAFOLDER = "data/"
FORMAT = "csv"
MODEL = "gpt-3.5-turbo"

class QuestionMine():
    def __init__(self, domain):
        self.api = OpenAIApi(MODEL)
        self.main_domain = domain

    def gen_questions(self):
        domains = self._get_domains()
        for domain in domains:
            prompt = f"Write 5 questions about {domain} considering {self.main_domain} in {FORMAT} format. Do not add any explanation."
            self._generate_response(domain, prompt)
        print("Total cost: ", self.api.total_cost, '$')

    def _get_domains(self):
        domains = []
        with open(f"{DATAFOLDER}datascience-topics.json", "r") as f:
            topics = json.load(f)
            for topic in topics:
                domains.append(topic["domain"])
        return domains

    def _generate_response(self, domain, prompt):
        start_time = time.time()
        content, cost, tokens = self.api.call_api(prompt)
        prompt_time = time.time() - start_time

        questions = self._parse_answer(content)
        self._save_response(domain, prompt, content, questions, prompt_time, cost, tokens)

    def _parse_answer(self, answer):
        items = answer.title().replace("_", " ").replace("\n", ",").split(",")
        items = [item for item in items if any(c.isalpha() for c in item)]
        items = [re.sub(r"^(\d+\.\s*|-*\s*)", "", item.strip()) for item in items]
        return items

    def _save_response(
        self, domain, prompt, content, questions, prompt_time, cost, tokens
    ):
        save_path = f"{DATAFOLDER}datascience-questions.json"
        prmpt = {
            "Q": prompt,
            "A": content,
            "questions": questions,
            "time": prompt_time,
            "tocken": tokens,
            "model": MODEL,
            "cost": cost,
            "domain": domain,
        }
        j_prmt = json.dumps(prmpt, indent=2)
        with open(save_path, "a") as f:
            f.write(j_prmt + ",")

if __name__ == "__main__":
    q_mine = QuestionMine("Data Science")
    q_mine.gen_questions()