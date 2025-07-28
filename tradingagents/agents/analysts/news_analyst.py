from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json

def create_news_analyst(llm, toolkit):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        # 工具链全部禁用
        # if toolkit.config["online_tools"]:
        #     tools = [toolkit.get_global_news_openai, toolkit.get_google_news]
        # else:
        #     tools = [
        #         toolkit.get_finnhub_news,
        #         toolkit.get_reddit_news,
        #         toolkit.get_google_news,
        #     ]

        # 提示词里直接写清需求
        system_message = (
            "You are a news researcher tasked with analyzing recent news and trends over the past week. "
            "Please write a comprehensive report of the current state of the world that is relevant for trading and macroeconomics. "
            "Look at news from EODHD, and finnhub to be comprehensive. "
            "Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."
            " Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."
            f"\nFor your reference, the current date is {current_date}. We are looking at the company {ticker}."
        )

        # prompt 构造（不用 tools、只有系统和历史消息）
        prompt = [
            {"role": "system", "content": system_message},
            *state["messages"]
        ]

        # 只用文本 LLM 推理
        result = llm.invoke(prompt)

        report = ""
        if hasattr(result, "content"):
            report = result.content
        elif isinstance(result, str):
            report = result
        else:
            report = str(result)

        return {
            "messages": [result],
            "news_report": report,
        }

    return news_analyst_node
