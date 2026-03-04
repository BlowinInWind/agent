from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

llm = ChatOpenAI(
    model="zhipuai/glm-5",           # 替换为你的模型名称，如 "qwen2.5", "deepseek-chat" 等
    openai_api_key="sk-vH7IxF0dcLUAy0HunorBGVpcLT7hY5esJQX2MQWYuiJbno66",     # 替换为你的 API Key，无需验证可填 "EMPTY"
    openai_api_base="http://model.mify.ai.srv/v1/",  # 替换为你的服务地址
    temperature=0.7,
)

llm_anthropic = ChatAnthropic(
    model="ppio/pa/claude-sonnet-4-6",           # 替换为你的模型名称，如 "qwen2.5", "deepseek-chat" 等
    openai_api_key="sk-vH7IxF0dcLUAy0HunorBGVpcLT7hY5esJQX2MQWYuiJbno66",     # 替换为你的 API Key，无需验证可填 "EMPTY"
    openai_api_base="http://model.mify.ai.srv/anthropic",  # 替换为你的服务地址
    temperature=0.7,
)

ZHIPU_API_KEY = "ad5c47ea564a4f618268919f127bb33a.EJmr2BQ23o6P2dg8"
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

zp_llm = ChatOpenAI(
    temperature=0,
    model="glm-5",
    openai_api_key=ZHIPU_API_KEY,
    openai_api_base=ZHIPU_BASE_URL,
)