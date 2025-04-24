
## Running Sample MCP
Contains echo tool & calculator tool
```
uvx --from git+https://github.com/ritzvik/samplemcp.git@main samplemcp
```

## Running AI workbench MCP
Contains functions from [Adrien's MCP server for Cloudera AI workbench](https://github.com/adfr/MCP_cloudera)

To run as CLI
```
CLOUDERA_ML_HOST=dummy CLOUDERA_ML_API_KEY=dummy uvx --from git+https://github.com/ritzvik/samplemcp.git@main workbenchmcp
```

### Clade Desktop Config:

```
{
  "mcpServers": {
    "cloudera-ml-mcp-server": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/ritzvik/samplemcp.git@main", "workbenchmcp"
      ],
      "env": {
        "CLOUDERA_ML_HOST": "https://ml-xxxx.cloudera.site",
        "CLOUDERA_ML_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Running Hive Table MCP
Contains tools for querying Hive tables through Cloudera ML data connections

To run as CLI
```
CONNECTION_NAME=your-connection USERNAME=your-username PASSWORD=your-password uvx --from git+https://github.com/ritzvik/samplemcp.git@main hivetablemcp
```

### Claude Desktop Config:

```
{
  "mcpServers": {
    "hive table mcp server": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/ritzvik/samplemcp.git@main", "hivetablemcp"
      ],
      "env": {
        "CONNECTION_NAME": "your-hive-connection-name",
        "USERNAME": "your-username",
        "PASSWORD": "your-password"
      }
    }
  }
}
```