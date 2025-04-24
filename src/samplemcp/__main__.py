import os, json
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


# Get configuration from environment variables
def get_config():
    return {"host": os.environ.get("CLOUDERA_ML_HOST", ""), "api_key": os.environ.get("CLOUDERA_ML_API_KEY", "")}


@mcp.tool()
def list_projects_tool() -> str:
    """
    List all available projects.

    Returns:
        JSON string with all project information
    """
    from samplemcp.workbenchmcp.functions.get_project_id import get_project_id

    config = get_config()
    result = get_project_id(config, {"project_name": "*"})

    # Convert result to string
    return json.dumps(result, indent=2)


def main():
    print("Starting MCP server...")
    mcp.run(transport="stdio")


def testrepo():
    print("Testing.... testing.... testing....")


def workbenchmcp():
    from samplemcp.workbenchmcp.server import main as workbenchmcp_main

    print("Starting Workbench MCP server...")
    workbenchmcp_main()


def hivetablemcp():
    from samplemcp.hivetablemcp.server import main as hivetablemcp_main

    print("Starting Hive Table MCP server...")
    hivetablemcp_main()


if __name__ == "__main__":
    main()
