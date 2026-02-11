from langchain.agents import create_agent
from main import llm
from tool import tools

agent = create_agent(llm, tools=tools)

result = agent.invoke({
    "messages": [{"role": "user", "content": "计算 3+5，再乘以 2"}]
})
