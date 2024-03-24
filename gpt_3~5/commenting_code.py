# =========================================
import json

from openai import OpenAI
from json import loads
from pathlib import Path
import os

# =========================================
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL = "gpt-3.5-turbo"
CONTEXT_PROMPT = (
    "You are a python developer, who is proficient in Django rest framework. You have been given a "
    "task to add code comment and documentation to existing python code without disturbing the core "
    "code or imports."
)


def chat(obj: OpenAI, text: str):
    completion = obj.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": CONTEXT_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    try:
        with open(os.path.join(BASE_DIR, "secret", "keys.json"), "r") as fp:
            json_data = json.loads(fp.read())
            client = OpenAI(api_key=json_data["key"])
            response = chat(
                obj=client,
                text="Compose a poem that explains the concept of recursion in programming.",
            )
            print(response)
    except Exception as e:
        print(e)
