from langchain_community.chat_models import ChatOpenAI
from langchain.agents import create_agent
from typing import Literal, Any
from pydantic import BaseModel, Field
from langchain.tools import tool, ToolRuntime


llm = ChatOpenAI(
    temperature=0.6,
    model="glm-4.7",
    openai_api_key="ad5c47ea564a4f618268919f127bb33a.EJmr2BQ23o6P2dg8",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

class Context(BaseModel):
    authority: Literal["admin", "user"]

class CalcInfo(BaseModel):
    """Calculation information"""
    output: int = Field(description="the calculation result")

@tool
def math_add(runtime: ToolRuntime[Context, Any], a: int, b: int) -> int:
    """Add two numbers together."""
    authority = runtime.context.authority
    # 只有admin用户可以访问加法工具
    if authority != "admin":
        raise PermissionError("User does not have permission to add numbers")
    return a + b

agent = create_agent(llm, tool=[math_add], system_prompt="You are a helpful assistant", response_format=CalcInfo)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "请计算 8234783 + 94123832 = ?"}]},
    config={"configurable": {"thread_id": "1"}},
    context=Context(authority="admin"))