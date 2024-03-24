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
    "code or imports. Just send back the code snippet only."
)
WORK_DIR = (
    "/home/sengupta/PycharmProjects/medical-backend/backend/"
    + "app_cdn/"
    + "pkg_models/"
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
        # max_tokens=50,
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    try:
        with open(os.path.join(BASE_DIR, "secret", "keys.json"), "r") as fp:
            json_data = json.loads(fp.read())
            client = OpenAI(api_key=json_data["key"])
            for node in os.listdir(WORK_DIR):
                if node[:2] != "__":
                    print(node)
                    with open(
                        os.path.join(WORK_DIR, node),
                        "r",
                    ) as file:
                        response = chat(
                            obj=client,
                            text=file.read(),
                        )
                        with open(
                            os.path.join(BASE_DIR, "gpt_3~5", "tmpfiles", node), "w"
                        ) as tmp:
                            response_lines = response.split("```")[1].split("\n")
                            tmp.write("\n".join(response_lines[1:]))
    except Exception as e:
        print(e)
