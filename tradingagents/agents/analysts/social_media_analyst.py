from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json

def create_social_media_analyst(llm, toolkit):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        # 工具链全部禁用
        # if toolkit.config["online_tools"]:
        #     tools = [toolkit.get_stock_news_openai]
        # else:
        #     tools = [toolkit.get_reddit_stock_info]

        system_message = (
            "You are a social media and company specific news researcher/analyst tasked with analyzing social media posts, recent company news, and public sentiment for a specific company over the past week. "
            "You will be given a company's name. Your objective is to write a comprehensive long report detailing your analysis, insights, and implications for traders and investors on this company's current state after looking at social media and what people are saying about that company, analyzing sentiment data of what people feel each day about the company, and looking at recent company news. "
            "Try to look at all sources possible from social media to sentiment to news. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."
            " Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."
            f"\nFor your reference, the current date is {current_date}. The current company we want to analyze is {ticker}."
        )

        # 只用普通 prompt，不传 tools
        prompt = [
            {"role": "system", "content": system_message},
            *state["messages"]
        ]

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
            "sentiment_report": report,
        }

    return social_media_analyst_node
