import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Any, Annotated
from pydantic import Field
import cml.data_v1 as cmldata

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP(name="Hive MCP server")


def get_config():
    return {
        "connection_name": os.environ.get("CONNECTION_NAME", ""),
        "username": os.environ.get("USERNAME", ""),
        "password": os.environ.get("PASSWORD", ""),
    }


@mcp.tool()
def hive_table_return_top_3_rows(
    table: Annotated[str, Field(description="Fully qualified table name (e.g. default.customer)")],
) -> Any:
    """
    Main tool code logic. Anything returned from this method is returned
    from the tool back to the calling agent.
    """
    config = get_config()
    CONNECTION_NAME = config["connection_name"]
    USERNAME = config["username"]
    PASSWORD = config["password"]

    sql_query1 = f"DESCRIBE {table}"

    sql_query2 = f"SELECT * FROM {table} limit 3"

    conn = cmldata.get_connection(CONNECTION_NAME, {"USERNAME": USERNAME, "PASSWORD": PASSWORD})

    try:
        dataframe1 = conn.get_pandas_dataframe(sql_query1)
        ret1 = dataframe1.to_dict(orient="records")  # structured output

        dataframe2 = conn.get_pandas_dataframe(sql_query2)
        ret2 = dataframe2.to_dict(orient="records")  # structured output

        ret = ret1 + ret2
        return ret
    finally:
        conn.close()


@mcp.tool()
def hive_or_impala_execute_readonly_sql_query(
    query: Annotated[str, Field(description="SQL query to execute")],
) -> str:
    """
    This tool executes a SQL query and returns the result as a dictionary.
    This tool is used for read-only queries. Do not use the tool for write/insert/update/delete queries.
    """
    config = get_config()
    CONNECTION_NAME = config["connection_name"]
    USERNAME = config["username"]
    PASSWORD = config["password"]

    conn = cmldata.get_connection(CONNECTION_NAME, {"USERNAME": USERNAME, "PASSWORD": PASSWORD})
    try:
        dataframe = conn.get_pandas_dataframe(query)
        print("dataframe returned: ", dataframe)
        dataframe_dict: dict = dataframe.to_dict(orient="records")
        return str(dataframe_dict)
    finally:
        conn.close()


@mcp.tool()
def hive_or_impala_execute_write_sql_query(
    query: Annotated[str, Field(description="SQL query to execute")],
) -> Any:
    """
    This tool executes a SQL query.
    This tool is used for write/insert/update/delete operations.
    """
    config = get_config()
    CONNECTION_NAME = config["connection_name"]
    USERNAME = config["username"]
    PASSWORD = config["password"]

    conn = cmldata.get_connection(CONNECTION_NAME, {"USERNAME": USERNAME, "PASSWORD": PASSWORD})
    cursor = conn.get_cursor()
    try:
        cursor.execute(query)
        return "Query executed successfully"
    except Exception as e:
        return f"Error executing query: {str(e)}"
    finally:
        cursor.close()
        conn.close()


def main():
    # Check if configuration is complete
    config = get_config()
    missing = [k for k, v in config.items() if not v]

    if missing:
        print(f"Error: Missing configuration: {', '.join(missing)}")
        print("Please set the following environment variables:")
        print("  CONNECTION_NAME - Your Cloudera ML connection name")
        print("  USERNAME - Your Cloudera ML username")
        print("  PASSWORD - Your Cloudera ML password")
        exit(1)

    # Initialize and run the server
    print(f"Starting Hive Table MCP Server with connection name: {config['connection_name']}")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
