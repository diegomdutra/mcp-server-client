from settings import mcp_client


async def get_tools_schema() -> list[dict]:
    """List tools from the MCP server as JSON-safe dicts."""
    async with mcp_client:
        tools = await mcp_client.list_tools()
    return [
        {
            "name": t.name,
            "description": t.description or "",
            "parameters": t.inputSchema if hasattr(t, "inputSchema") else {},
        }
        for t in tools
    ]


def tools_to_ollama_format(tools_schema: list[dict]) -> list[dict]:
    """Convert MCP tool schemas into the Ollama function-calling format."""
    ollama_tools = []
    for t in tools_schema:
        params = t.get("parameters", {})
        ollama_tools.append(
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": params,
                },
            }
        )
    return ollama_tools
