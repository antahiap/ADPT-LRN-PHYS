import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=api_key, temperature=0)


tools = load_tools(['google-serper', 'wikipedia'], llm=llm)
print(tools[0].name, tools[0].description)

# Create the agent
agent = initialize_agent(
    tools,
    llm, 
    agent='zero-shot-react-description',
    verbose=True)

# Call the tools
# item = agent.run("Berlin")
# print(item)