import time
import hashlib
import hmac
import base64
from urllib import parse
from langchain_core.tools import tool
import requests

# 心知天气 API 配置
SENIVERSE_UID = "你的公钥"
SENIVERSE_KEY = "你的私钥"
SENIVERSE_API_URL = "https://api.seniverse.com/v3/weather/now.json"

@tool
def get_weather(city: str) -> str:
    """查询指定城市的实时天气情况，支持中文城市名如北京、上海等"""
    try:
        ts = int(time.time())
        params_str = f"ts={ts}&uid={SENIVERSE_KEY}"

        key = bytes(SENIVERSE_KEY, "utf-8")
        raw = bytes(params_str, "utf-8")
        digester = hmac.new(key, raw, hashlib.sha1).digest()
        sig = parse.quote(base64.b64encode(digester).decode('utf8'))
        url = f"{SENIVERSE_API_URL}?location={parse.quote(city)}&{params_str}&sig={sig}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if 'results' in data:
            result = data['results'][0]
            location = result['location']['name']
            now = result['now']
            return f"{location}：{now['text']}，温度 {now['temperature']}°C"
        else:
            return f"未找到 {city} 的天气信息"
    except Exception as e:
        return f"获取天气失败: {str(e)}"

from datetime import datetime

@tool
def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


from langchain.agents import create_agent
from main import llm
tools = [get_weather, get_current_time]
agent = create_agent(llm, tools)

if __name__ == "__main__":
    question = "现在几点了？北京天气怎么样？"
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)