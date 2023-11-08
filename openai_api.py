import json
import openai


class OpenAIHelper:
    api_key: str
    model: str

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    async def chat_with_openai(self, messages: list):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                # Controls randomness: 0.0 (deterministic) to 1.0 (creative).
                temperature=0.5,
                # Maximum output length: Min 1 to model's max tokens limit.
                max_tokens=250,
                # Nucleus sampling: 0.0 (most likely token only) to 1.0 (all tokens).
                top_p=0.5,
                # Discourages repetition: 0.0 (no penalty) to 2.0 (high penalty).
                frequency_penalty=0.0,
                # Encourages new topics: 0.0 (no penalty) to 2.0 (high penalty).
                presence_penalty=0.0
            )
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def create_prompt(self, context, transcript):
        # Create a dictionary with the required structure
        message_structure = {
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": transcript},
            ]
        }
        # Convert the dictionary to a JSON object
        message_json = json.dumps(message_structure)
        return message_json
