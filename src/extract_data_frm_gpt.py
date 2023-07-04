import openai
import os



class ChatGPTWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        self.model = "text-davinci-002"  # You can choose the model that suits your requirements

    def generate_response(self, prompt, max_tokens=50):
        try:
            response = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=max_tokens
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    api_key = os.environ["OPENAI_API_KEY"] 
    chatgpt = ChatGPTWrapper(api_key)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        response = chatgpt.generate_response(prompt=user_input)
        print("ChatGPT: ", response)
