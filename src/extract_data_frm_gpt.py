import openai
import os
import json
import tiktoken
import time

class data_mine():
    def __init__(self, api_key, test):
        self.api_key = api_key
        self.frmt = 'csv'
        self.model = "gpt-3.5-turbo"
        self.path = 'data/'
        self.max_tokens=2000
        self.test = test

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


    def domain_high(self):
        self.prompt = f"What are the {self.domain} topics in {self.frmt} format"
        self.name = 'domain_high' 
        return self.generate_response()



    def generate_response(self):
        if self.test:
            self.prompt = 'print hello'
            self.name = 'test'
            max_tokens = 2
        try:
            input(self.prompt)
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
        except Exception as e:
            self.resp = f"Error: {str(e)}"
        self.save_responce()

        return self.resp


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
            'max_tocken': self.max_tokens
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

    api_key = os.environ["OPENAI_API_KEY"] 
    cntnt = data_mine(api_key, test=False)
    cntnt.teacher()
    cntnt.domain_high()

