from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="ppio/pa/claude-sonnet-4-6",           # 替换为你的模型名称，如 "qwen2.5", "deepseek-chat" 等
    openai_api_key="sk-vH7IxF0dcLUAy0HunorBGVpcLT7hY5esJQX2MQWYuiJbno66",     # 替换为你的 API Key，无需验证可填 "EMPTY"
    openai_api_base="http://model.mify.ai.srv/anthropic",  # 替换为你的服务地址
    temperature=0.7,
)
