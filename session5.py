import os

from langchain.agents.middleware import before_model
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent, AgentState
from langgraph.runtime import Runtime
from typing import Any
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver

llm = ChatOpenAI(
    temperature=0.6,
    model="glm-4.7",
    openai_api_key="ad5c47ea564a4f618268919f127bb33a.EJmr2BQ23o6P2dg8",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

@tool
def add(a: int, b: int) -> int:
    """计算两个数字的差"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """计算两个数字的乘积"""
    return a * b

@before_model
def trim_message(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """keep only the last few messages to fit context window"""
    messages = state["messages"]
    if len(messages) < 3:
        return None

    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {"messages": [
        RemoveMessage(id=REMOVE_ALL_MESSAGES),
        *new_messages
    ]}

# 4. 工具列表
tools = [add, multiply]

agent = create_agent(llm, tools, middleware=[trim_message], checkpointer=InMemorySaver())

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
agent.invoke({"messages": "now do the same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

final_response["messages"][-1].pretty_print()

# if __name__ == "__main__":
#     print("=" * 50)
#     print("LangChain Agent Demo - 使用智谱 GLM-4")
#     print("=" * 50)
#
#     # 测试问题
#     question = "用 add 工具计算 3+5，再用 multiply 工具把结果乘以 2"
#
#     print(f"\n问题: {question}\n")
#
#     # 调用 agent
#     result = agent.invoke({"messages": [{"role": "user", "content": question}]})
#
#     # 打印完整的消息历史，查看 tool 调用过程
#     print("\n" + "=" * 50)
#     print("消息历史（可以看到 Tool 调用）:")
#     print("=" * 50)
#
#     for i, msg in enumerate(result["messages"]):
#         msg_type = type(msg).__name__
#         print(f"\n[{i + 1}] {msg_type}:")
#
#         if msg_type == "HumanMessage":
#             print(f"    用户: {msg.content}")
#         elif msg_type == "AIMessage":
#             if msg.tool_calls:
#                 print(f"    🤖 AI 决定调用工具:")
#                 for tc in msg.tool_calls:
#                     print(f"       → {tc['name']}({tc['args']})")
#             if msg.content:
#                 print(f"    🤖 AI: {msg.content[:100]}...")
#         elif msg_type == "ToolMessage":
#             print(f"    🔧 工具 [{msg.name}] 返回: {msg.content}")
#
#     print("\n" + "=" * 50)
#     print(f"最终答案: {result['messages'][-1].content}")