from base import Compiler
from ollama import chat
import re


def extract_code_blocks(text):
    # 匹配完整的多行代码块（包括语言标识符和内容）
    pattern = r'```(?:\w*\n)(.*?)(?=\n```)'
    return re.findall(pattern, text, re.DOTALL)

def remove_think_tags(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

def find_importance(info) -> str:
    pattern = r"```(?:[^\n]*\n)(.*?)(?=```)"
    keywords = ["一般", "重要", "无关"]
    code_blocks = re.findall(pattern, info, re.DOTALL)
    found_keywords = set()

    for block in code_blocks:
        for keyword in keywords:
            if keyword in block:
                found_keywords.add(keyword)

    return list(found_keywords)


class LLMCompiler(Compiler):
    def __init__(self, config=None):
        super().__init__(config)

    def html_to_markdown(self, info: str) -> str:
        return chat(
            model="qwen3",
            messages=[
                {
                    "role": "system",
                    "content": "你现在需要将下面输入的html文档进行结构清洗，提取其主要内容，给出针对其内容的一个总结。格式要求，必须将总结放置在单独的多行代码语法中，且不要在这个多行代码语法的范围内中放置其他内容。",
                },
                {
                    "role": "user",
                    "content": info,
                },
            ],
        ).message.content

    def compile_info(self, source_description, title, url):
        prompt = """你是一个专业的简报编辑助手，下面提供了我的个人信息，现在你需要帮我判断所抓取到的新闻信息是否是我所关心的信息，并将他们分为三个重要等级，分别是`重要`、`一般`、`无关`。
格式要求，必须将你判断得到的重要等级结果放置在单独的多行代码语法中，且不要在这个多行代码语法的范围内中放置其他内容。"""
        response: str = chat(
            model="qwen3",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {"role": "user", "content": self.config["personal_info"]},
                {
                    "role": "user",
                    "content": f"新闻消息来源：{source_description}，新闻标题：{title}",
                },
            ],
        ).message.content
        importance = find_importance(response)[0]
        # print(response)
        # TODO: ensure only one importance
        if importance == "无关":
            return ("", "无关")
        print(importance)
        html_parsed = self.html_to_markdown(self.get_info(url))
        print(html_parsed)
        detail_info = remove_think_tags(html_parsed)
        print(detail_info)
        prompt_summary = """你是一个专业的简报编辑助手，下面提供了我的个人信息，请你根据提供的信息，总结不超过300字的新闻内容。
格式要求，必须将新闻内容放置在单独的多行代码语法中，且不要在这个多行代码语法的范围内中放置其他内容。"""
        response: str = chat(
            model="qwen3",
            messages=[
                {
                    "role": "system",
                    "content": prompt_summary,
                },
                {"role": "user", "content": self.config["personal_info"]},
                {
                    "role": "user",
                    "content": f"对我的重要程度：{importance}, 新闻消息来源：{source_description}，新闻标题：{title}，新闻内容：{detail_info}",
                },
            ],
        ).message.content
        # print(response)
        summary = extract_code_blocks(response)[0]
        print(summary)
        return (summary, importance)

    def compile_list(self, info_list):
        r = ""
        for info in info_list:
            r += "\n".join(info)
        return r

