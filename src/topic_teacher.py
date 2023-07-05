from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.5,
)

class TopicTeacher():
    def __init__(self, topic):
        self.chain = ConversationChain(llm=llm, verbose=True, memory=ConversationBufferMemory())
        self.topic = topic

    def send_message(self, message):
        return self.chain.run(message)
    
    def get_course(self):
        return self.chain.run(
            f"Explain {self.topic} in markdown format to a 10 year old. Only include facts known to be true. Be clear, simple and concise."
        )
    
    def get_exercise(self):
        return self.chain.run(
            f"Give me 1 very hard exercise that you didnt give me yet to assess my knowledge on {self.topic}"
        )
    
    def correct_exercise(self, exercise, answer):
        return self.chain.run(
            f"""Here's the exercise: 
            {exercise}

            Here's my answer:
            {answer}
            
            Grade me out of 5 and correct my mistakes. Dont give explanation if I'm correct."""
        )