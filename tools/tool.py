from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """计算连个数据的和"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """计算连个数据的乘"""
    return a * b

tools = [add, multiply]