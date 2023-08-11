import openai
import os
import json
import tiktoken
import time

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

class DataMine():
    def __init__(self, test):
        self.frmt = 'csv'
        self.model = "gpt-3.5-turbo"
        self.path = 'data/'
        self.max_tokens=2000
        self.test = test
        self.prompt_time=0

    def student(self, age, intrst):
        self.age = age
        self.intrst = intrst

    def teacher(
            self,
            domain='physics', 
            depth=4,
            n_problem=5,
            ranking= range(0,6)):
        
        self.domain = domain
        self.depth = depth
        self.n_problem = n_problem
        self.ranking = ranking

    def gpt_depndencies(self, domains):
        for di, domain in enumerate(domains):
            self.prompt = f"What are the {domain} topics in {self.frmt} format"
            self.name = f'{domain}-{di}' 
            self.generate_response()
            if not self.topics == []:
                return self.gpt_depndencies(self.topics)
            else:
                return 'done'

    def generate_response(self):
        if self.test:
            self.prompt = 'print hello'
            self.name = 'test'
            max_tokens = 2
        try:
            input(self.prompt)
            input(openai.api_key)
            start_time = time.time()
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                      {"role": "user", 
                       "content": self.prompt
                       },
                  ],
                max_tokens = self.max_tokens,
                
            )
            self.prompt_time = time.time() - start_time

            self.resp = response.choices[0].message.content#.strip()
            self.topics = []
        except Exception as e:
            self.resp = f"Error: {str(e)}"
            self.topics = []
        self.save_responce()

        # return self.topics

    def save_responce(self):
        save_path = f'{self.path}{self.name}.json'
        cost, tocken = self.cost_tokens(f'{self.prompt}, {self.resp}')
        prmpt = {
            'Q' : self.prompt,
            'A' : self.resp,
            'time': self.prompt_time,
            'tocken': tocken,
            'model' : self.model,
            'cost': cost, 
            'max_tocken': self.max_tokens,
            'domain': self.topics
        }
        j_prmt = json.dumps(prmpt, indent=2)
        with open(save_path, 'a') as f:
            f.write(j_prmt)

    def cost_tokens(self, text):
        TOKEN_COST = {'gpt-3.5-turbo': 0.002 / 1000}

        encoding = tiktoken.encoding_for_model(self.model)
        tokens = encoding.encode(text)
        ntokens = len(tokens)
        cost = ntokens * TOKEN_COST[self.model]
        return (cost, ntokens)


if __name__ == '__main__':

    openai.api_key = os.getenv("OPENAI_API_KEY")
    cntnt = DataMine(test=False)
    cntnt.teacher(domain='data science')
    cntnt.gpt_depndencies(['data science'])

