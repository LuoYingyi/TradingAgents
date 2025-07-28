from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create a custom config
#config = DEFAULT_CONFIG.copy()
#config["llm_provider"] = "google"  # Use a different model
#config["backend_url"] = "https://generativelanguage.googleapis.com/v1"  # Use a different backend
#config["deep_think_llm"] = "gemini-2.0-flash"  # Use a different model
#config["quick_think_llm"] = "gemini-2.0-flash"  # Use a different model
#config["max_debate_rounds"] = 1  # Increase debate rounds
#config["online_tools"] = True  # Increase debate rounds

# Initialize with custom config
#ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
#_, decision = ta.propagate("NVDA", "2024-05-10")
#print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns


config = DEFAULT_CONFIG.copy()
config["quick_think_llm"] = "llama3.1:8b"
config["deep_think_llm"] = "deepseek-r1:32b"
config["online_tools"] = False  # 完全离线
config["ollama_api_base"] = "http://localhost:11434"  # 如果框架允许自定义 API 地址

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("AAPL", "2024-06-01")
print(decision)
