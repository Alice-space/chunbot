from typing import Sequence
from compile.base import Compiler, CompilerConfig
from ollama import ChatResponse, Message, chat  # type: ignore
import logging

from compile.helper import (
    extract_code_blocks,
    find_importance,
    format_item,
    get_info,
    html_to_markdown,
    remove_think_tags,
)
from type import ImportanceType, News


logger = logging.getLogger(__name__)


class LLMCompilerConfig(CompilerConfig):
    personal_info: str


class LLMCompiler(Compiler):
    def __init__(self, config: LLMCompilerConfig):
        self.config = config
        logger.info("Initializing LLMCompiler")

    def compile_info(self, news: News) -> News:
        if not news["success"]:
            return news

        logger.info(f"Compiling info: {news['title']} from {news['source']}")

        # Get Importance
        messages: Sequence[Message] = [
            Message(
                role="system",
                content="""你是一个专业的简报编辑助手，下面提供了我的个人信息，现在你需要帮我判断所抓取到的新闻信息是否是我所关心的信息，并将他们分为三个重要等级，分别是`重要`、`一般`、`无关`。
格式要求，必须将你判断得到的重要等级结果放置在单独的多行代码语法中，且不要在这个多行代码语法的范围内中放置其他内容，注意，重要等级必须严格遵循`重要`、`一般`、`无关`的格式，不要添加诸如`重要等级`之类的前缀。""",
            ),
            Message(role="user", content=self.config["personal_info"]),  # type: ignore
            Message(
                role="user",
                content=f"新闻消息来源：{news['source']}，新闻标题：{news['title']}",
            ),
        ]
        try:
            response: ChatResponse = chat(
                model="qwen3",
                messages=messages,
            )
            if not response.message.content:
                news["success"] = False
                news["error_msg"] = "重要级判断失败"
                news["importance"] = "未分配"
                logger.error(f"No Importance detected: {news['title']}")
                return news
            else:
                # print(response.message.content)
                importance = find_importance(response.message.content)
                news["importance"] = importance
                if importance == "无关":
                    logger.debug(f"Marked as irrelevant: {news['title']}")
                    return news
        except Exception as e:
            news["success"] = False
            news["error_msg"] = "重要级判断错误"
            logger.error(f"Importance error: {news['title']} {str(e)}")
            return news

        logger.debug(
            f"Processing news with importance {news['importance']}: {news['title']}"
        )

        # get detail

        try:
            if not news["url"]:
                news["success"] = False
                news["error_msg"] = "没有URL"
                logger.error(f"No URL detected: {news['title']}")
                return news
            detail_info = remove_think_tags(html_to_markdown(get_info(news["url"])))
            # print(detail_info)
        except Exception as e:
            news["success"] = False
            news["error_msg"] = "解析详情错误"
            logger.error(f"Parse detail info error: {news['title']}, {str(e)}")
            return news

        # get summary
        logger.debug(
            f"Processing news with importance {news['importance']}: {news['title']} \n detail: {detail_info[:100]}"
        )
        summary_msg: Sequence[Message] = [
            Message(
                role="system",
                content="""你是一个专业的简报编辑助手，下面提供了我的个人信息，请你根据提供的信息，总结不超过100字的新闻内容。
格式要求，必须将新闻内容放置在单独的多行代码语法中，且不要在这个多行代码语法的范围内中放置其他内容。""",
            ),
            Message(role="user", content=self.config["personal_info"]),  # type: ignore
            Message(
                role="user",
                content=f"对我的重要程度：{news['importance']}, 新闻消息来源：{news['source']}，新闻标题：{news['title']}，新闻内容：{detail_info}",
            ),
        ]
        try:
            summary_response: ChatResponse = chat(model="qwen3", messages=summary_msg)
            if not summary_response.message.content:
                news["success"] = False
                news["error_msg"] = "获取总结错误"
                logger.error(f"Parse summary info error: {news['title']}")
                return news
            # print(summary_response.message.content)
            summary = extract_code_blocks(summary_response.message.content)
            news["summary"] = summary
        except Exception as e:
            news["success"] = False
            news["error_msg"] = "获取总结错误"
            logger.error(f"Summary error: {news['title']}")
            return news

        logger.info(f"process ok: {news['title']}")
        logger.debug(f"process ok detail: {news}")
        return news

    def compile_list(self, news: list[News]) -> str:
        logger.info(f"Compiling list of {len(news)} items")

        # Calculate success ratio
        total_news = len(news)
        successful_news = sum(1 for item in news if item["success"])
        success_ratio = successful_news / total_news if total_news > 0 else 0

        # Collect failed news details
        failed_news = [
            f"- 来源: {item['source']}, 标题: {item['title']}"
            for item in news
            if not item["success"]
        ]

        # group by importance
        importance_groups: dict[ImportanceType, list[News]] = {}
        for single_news in news:
            if not single_news["success"]:
                continue
            importance = single_news["importance"]
            if importance not in importance_groups:
                importance_groups[importance] = []
            importance_groups[importance].append(single_news)

        # fill in
        important = "\n".join(
            format_item(item) for item in importance_groups.get("重要", [])
        )
        normal = "\n".join(
            format_item(item) for item in importance_groups.get("一般", [])
        )
        irrelevant = "\n".join(
            format_item(item) for item in importance_groups.get("无关", [])
        )

        report = f"""# 今日简报

## 统计
成功比例: {success_ratio:.1%} ({successful_news}/{total_news})
失败条目: 
{"\n".join(failed_news) if failed_news else "无"}

## 重要
{important}

## 一般
{normal}

## 无关
{irrelevant}
"""

        return report
