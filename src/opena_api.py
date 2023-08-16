import os
import openai

from dotenv import load_dotenv
load_dotenv()

class OpenAIApi():
    def __init__(self, model):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.total_cost = 0

    MAX_RETRIES = 3
    def call_api(self, prompt):
        for i in range(self.MAX_RETRIES):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                )
                print(response)
                break
            except Exception as e:
                print("Error: ", str(e))
                if i == self.MAX_RETRIES - 1:
                    raise Exception("Max retries exceeded")
        return self._format_response(response)
    
    def _format_response(self, response):
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        cost = self._cost_tokens(tokens)
        self.total_cost += cost
        return content, cost, tokens
    
    TOKEN_COST = {'gpt-3.5-turbo': 0.002 / 1000}
    def _cost_tokens(self, n_tokens):
        return n_tokens * self.TOKEN_COST[self.model]