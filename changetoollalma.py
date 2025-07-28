from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
resp = client.chat.completions.create(
    model="qwen3:30b",
    messages=[{"role": "user", "content": "Hello, who are you?"}]
)
print(resp.choices[0].message.content)
