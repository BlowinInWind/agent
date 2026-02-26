from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from config.llm import llm
from tools.tool import tools

# 创建内存检查点（保存对话历史）
memory = MemorySaver()

# 创建带记忆的agent
agent = create_agent(llm, tools=tools, checkpointer=memory)

# 对话配置（使用 thread_id 标识对话）
config = {"configurable": {"thread_id": "conversation-1"}}

# 第一轮
result1 = agent.invoke(
    {"messages": [{"role": "user", "content": "北京天气怎么样？"}]},
    config
)
print("第一轮:", result1["messages"][-1].content)

# 第二轮（Agent 记得上文）
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "那上海呢？"}]},
    config
)
print("第二轮:", result2["messages"][-1].content)

# 第三轮
result3 = agent.invoke(
    {"messages": [{"role": "user", "content": "哪个城市更冷？"}]},
    config
)
print("第三轮:", result3["messages"][-1].content)
