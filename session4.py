from langchain_core.tools import tool
from datetime import datetime

@tool
def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def search_attractions(city: str) -> str:
    attractions = {
        "北京": "故宫、长城、颐和园、天坛、南锣鼓巷",
        "上海": "外滩、东方明珠、豫园、南京路、迪士尼",
        "杭州": "西湖、灵隐寺、宋城、西溪湿地、千岛湖",
        "成都": "宽窄巷子、锦里、大熊猫基地、都江堰、青城山",
    }

    return attractions.get(city, f"{city}暂无景点信息")

@tool
def estimate_travel_time(from_city: str,  to_city: str) -> str:
    """估算两个城市之间的交通时间"""
    times = {
        ("北京", "上海"): "高铁约4.5小时，飞机约2小时",
        ("上海", "杭州"): "高铁约1小时，自驾约2小时",
        ("北京", "杭州"): "高铁约5小时，飞机约2小时",
        ("成都", "北京"): "高铁约8小时，飞机约2.5小时",
    }
    key = (from_city, to_city)
    reverse_key = (to_city, from_city)
    return times.get(key) or times.get(reverse_key) or f"{from_city}到{to_city}的交通信息暂无"


# 复杂任务示例
question = """
我想在春节期间从北京去上海玩3天，请帮我：
1. 查看两地天气
2. 推荐上海的景点
3. 估算交通时间
4. 给出一个简单的出行建议
"""

from langchain.agents import create_agent
from main import llm
from session2 import get_weather
tools = [get_weather, get_current_time, search_attractions, estimate_travel_time]# 创建带记忆的agent
agent = create_agent(llm, tools=tools)
result = agent.invoke({"messages": [{"role": "user", "content": question}]})