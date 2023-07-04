from langchain.chains import ConversationChain
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

class LlmChain():
    def __init__(self, topic):
        self.chain = ConversationChain(llm=llm, memory=ConversationBufferMemory())
        self.topic = topic

    def send_message(self, message):
        return self.chain.run(message)
    
    def get_course(self):
        return self.chain.run(
            f"As a crash test engineer what is {self.topic}"
        )
    
    def get_exercises(self):
        return self.chain.run(
            f"Can you give me 3 exercises to assess my knowledge for {self.topic}"
        )
    
    def correct_exercises(self):
        return self.chain.run(
            f"Give me an exemple of a good answer for the exercises you gave."
        )