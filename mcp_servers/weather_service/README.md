# weather_service MCP server

A MCP server project, following the tutorial at https://modelcontextprotocol.io/quickstart/server

For Linux, the required condif to use the server is:

```
{
    "mcpServers": {
        "weather": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
                "run",
                "weather.py"
            ]
        }
    }
}
```