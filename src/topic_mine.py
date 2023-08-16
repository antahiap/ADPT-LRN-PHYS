import json
import time
import re

from opena_api import OpenAIApi

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATAFOLDER = "data/"
FORMAT = "csv"
MODEL = "gpt-3.5-turbo"


class TopicMine:
    def __init__(self, domain):
        self.api = OpenAIApi(MODEL)
        self.main_domain = domain

    MAX_RECURSION = 1

    def gpt_depndencies(self, domains, recursion=0):
        for domain in domains:
            prompt = f"What are the {domain} topics considering {self.main_domain} in {FORMAT} format. Do not add any explanation."
            topics = self._generate_response(domain, prompt)
            if topics and recursion < self.MAX_RECURSION:
                self.gpt_depndencies(topics, recursion + 1)
        print("Total cost: ", self.api.total_cost, '$')

    def _generate_response(self, domain, prompt):
        start_time = time.time()
        content, cost, tokens = self.api.call_api(prompt)
        prompt_time = time.time() - start_time

        topics = self._parse_answer(content)
        self._save_response(domain, prompt, content, topics, prompt_time, cost, tokens)
        return topics

    def _parse_answer(self, answer):
        items = answer.title().replace("_", " ").replace("\n", ",").split(",")
        items = [item for item in items if any(c.isalpha() for c in item)]
        items = [re.sub(r"^(\d+\.\s*|-*\s*)", "", item.strip()) for item in items]
        return items

    def _save_response(
        self, domain, prompt, content, topics, prompt_time, cost, tokens
    ):
        save_path = f"{DATAFOLDER}datascience-topics.json"
        prmpt = {
            "Q": prompt,
            "A": content,
            "topics": topics,
            "time": prompt_time,
            "tocken": tokens,
            "model": MODEL,
            "cost": cost,
            "domain": domain,
        }
        j_prmt = json.dumps(prmpt, indent=2)
        with open(save_path, "a") as f:
            f.write(j_prmt)
            f.write(",")


if __name__ == "__main__":
    domain = "Data Science"
    cntnt = TopicMine(domain)
    cntnt.gpt_depndencies([domain])
