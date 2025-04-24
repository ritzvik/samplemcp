from typing import Annotated, Literal
from pydantic import Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Sample-MCP")


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"


@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"


@mcp.tool()
def calculator_tool(
    a: Annotated[float, Field(description="first number")],
    b: Annotated[float, Field(description="second number")],
    operator: Annotated[Literal["+", "-", "*", "/"], Field(description="operator")],
) -> str:
    """
    Calculator tool which can do basic addition, subtraction, multiplication, and division.
    Division by 0 is not allowed.
    """
    res = None
    if operator == "+":
        res = a + b
    elif operator == "-":
        res = a - b
    elif operator == "*":
        res = a * b
    elif operator == "/":
        res = float(a / b)
    else:
        raise ValueError("Invalid operator")
    return str(res)


def main():
    print("Starting MCP server...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
