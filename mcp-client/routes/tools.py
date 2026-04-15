import traceback

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from settings import logger, mcp_client
from helpers import serialize_content, get_tools_schema
from schemas import ToolCallRequest

router = APIRouter()


@router.get("/tools")
async def list_tools():
    """Return the list of tools exposed by the MCP server."""
    try:
        tools = await get_tools_schema()
        for t in tools:
            t["has_visual"] = t["name"].endswith("_visual")
        return tools
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.post("/tools/call")
async def call_tool(req: ToolCallRequest):
    """Call a single MCP tool by name and return its result."""
    try:
        async with mcp_client:
            result = await mcp_client.call_tool(req.tool_name, req.arguments)
        logger.debug("Raw result type=%s value=%s", type(result), result)
        content = result.content if hasattr(result, "content") else result
        if not isinstance(content, (list, tuple)):
            content = [content]
        return {"tool": req.tool_name, "content": serialize_content(content)}
    except Exception as exc:
        logger.error("call_tool error: %s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/render/{tool_name}")
async def render_tool(tool_name: str, args: str = "{}"):
    """Proxy the PrefabUI HTML render from the MCP server."""
    try:
        url = f"http://localhost:8002/render/{tool_name}"
        async with httpx.AsyncClient() as http:
            resp = await http.get(url, params={"args": args}, timeout=15)
        return HTMLResponse(content=resp.text, status_code=resp.status_code)
    except Exception as exc:
        logger.error("render_tool error: %s", traceback.format_exc())
        raise HTTPException(status_code=502, detail=str(exc))
