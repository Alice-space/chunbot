import logging
from typing import Sequence
from bs4 import BeautifulSoup
from ollama import ChatResponse, Message, chat  # type: ignore
import requests
import re

from type import ImportanceType, News

logger = logging.getLogger(__name__)


def get_info(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.getText()


def extract_code_blocks(text: str) -> str:
    pattern = r"```(?:\w*\n)(.*?)(?=\n```)"
    match = re.findall(pattern, text, re.DOTALL)
    if not match:
        logging.error("No code blocks found in the input text")
        raise ValueError("Cannot find code blocks!")
    if len(match) > 1:
        logging.error(f"Found {len(match)} code blocks in the input text")

    return match[0]


def remove_think_tags(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


def find_importance(info: str) -> ImportanceType:
    pattern = r"```(?:[^\n]*\n)(.*?)(?=```)"
    keywords: list[ImportanceType] = ["一般", "重要", "无关"]
    code_blocks = re.findall(pattern, info, re.DOTALL)
    logger.debug(f"Analyzing info for importance: {info[:100]}...")

    found_keywords: list[ImportanceType] = []
    for block in code_blocks:
        for keyword in keywords:
            if keyword in block:
                found_keywords.append(keyword)

    if len(found_keywords) > 1:
        logger.error(f"Found multiple importance keywords: {found_keywords}")

    if found_keywords:
        logger.info(f"Using importance keyword: {found_keywords[0]}")
        return found_keywords[0]

    logger.error("No importance keyword found, defaulting to '一般'")
    return "一般"


def html_to_markdown(info: str) -> str:
    logger.debug(f"Converting HTML to markdown: {info[:100]}...")
    msg: Sequence[Message] = [
        Message(
            role="system",
            content="你现在需要将下面输入的html文档进行结构清洗，提取其主要内容，给出针对其内容的一个总结。格式要求，必须将总结放置在单独的多行代码语法中，且不要在这个多行代码语法的范围内中放置其他内容。",
        ),
        Message(role="user", content=info),
    ]
    response: ChatResponse = chat(
        model="qwen3",
        messages=msg,
    )

    if response.message.content:
        return response.message.content
    else:
        logger.error("Empty response content received from chat model")
        raise ValueError("Empty response content received from chat model")


def format_item(item: News) -> str:
    return f"- [{item['title']}]({item['url']}) ({item['source']}){f": {item['summary']}" if item['summary'] else ""}"
