# src/llm.py

import os
from openai import OpenAI

class LLM:
    def __init__(self):
        self.client = OpenAI()

    def generate_daily_report(self, markdown_content, dry_run=False):
        prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
        if dry_run:
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(prompt)
            return "DRY RUN"

        print("Before call GPT")
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
                {"role": "system", "content": "你是一个帮助总结 GitHub 内容 的 AI。"
                                              "你的摘要应当简洁明了，突出关键点，并抓住问题的本质，包括任何重要的评论。"
                                              "请确保识别出主要请求、支持的评论以及提出的任何问题，使用中文来回复"}
            ]
        )
        print("After call GPT")
        print(response)
        return response.choices[0].message.content
