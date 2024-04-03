# =========================================
import json
from openai import OpenAI
from pathlib import Path
import os

# =========================================
BASE_DIR = Path(__file__).resolve().parent.parent


def chat(obj: OpenAI, model: str, context: str, text: str) -> str:
    completion = obj.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": context,
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
            api_key = json_data["key"]
            work_dir = json_data["source_dir"]
            context = json_data["context"]
            model = json_data["model"]

            client = OpenAI(api_key=api_key)
            for node in os.listdir(work_dir):
                if node[:2] != "__":
                    with open(
                        os.path.join(work_dir, node),
                        "r",
                    ) as file:
                        response = chat(
                            obj=client,
                            model=model,
                            context=context,
                            text=file.read(),
                        )
                        with open(
                            os.path.join(BASE_DIR, "gpt_3~5", "tmpfiles", node), "w"
                        ) as tmp:
                            response_lines = response.split("```")[1].split("\n")
                            tmp.write("\n".join(response_lines[1:]))
    except Exception as e:
        print(e)
