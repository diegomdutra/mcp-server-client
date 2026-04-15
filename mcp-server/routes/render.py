import json as _json

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from app.factory import mcp
from helpers.visuals import VISUAL_BUILDERS


@mcp.custom_route("/render/{tool_name}", methods=["GET"])
async def render_tool(request: Request) -> HTMLResponse:
    tool_name = request.path_params["tool_name"]
    builder = VISUAL_BUILDERS.get(tool_name)
    if not builder:
        available = ", ".join(VISUAL_BUILDERS.keys())
        return HTMLResponse(
            f"<h1>Unknown visual tool: {tool_name}</h1><p>Available: {available}</p>",
            status_code=404,
        )
    try:
        args_raw = request.query_params.get("args", "{}")
        parsed = _json.loads(args_raw)
        app_result = builder(**parsed)
        return HTMLResponse(app_result.html(renderer_mode="cdn"))
    except Exception as exc:
        return HTMLResponse(f"<h1>Error</h1><pre>{exc}</pre>", status_code=500)


@mcp.custom_route("/render", methods=["GET"])
async def list_visual_tools(request: Request) -> JSONResponse:
    """List available visual tools."""
    return JSONResponse([
        {"name": name, "parameters": list(builder.__code__.co_varnames[:builder.__code__.co_argcount])}
        for name, builder in VISUAL_BUILDERS.items()
    ])
