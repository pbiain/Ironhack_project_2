# %%
# Single-cell test: Load key and ask OpenAI to say hello
import os
from dotenv import load_dotenv
import openai

def config_llm():

    # Load environment variables
    load_dotenv()
    # Assign API key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print("API Key loaded:", openai.api_key.startswith("sk-"))  # True if key is valid
    # Simple helper function for chat
    test_prompt = "tell me a joke."
    def call_openai(prompt=test_prompt, model="gpt-4.1-nano", temperature=0):
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    # Test prompt
    test_prompt = "Say hello."
    response = call_openai(test_prompt)
    print("API Test Result:")
    print(response)


