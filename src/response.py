from openai import OpenAI
import os
from dotenv import load_dotenv

def response(all_messages):
    load_dotenv()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    completion = client.chat.completions.create(
        #   extra_headers={
        #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
        #   },
        extra_body={},
        model="mistralai/mistral-7b-instruct:free",
        messages = all_messages 
    )

    return completion.choices[0].message.content