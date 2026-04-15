import json
import traceback

import ollama
from fastapi import APIRouter, HTTPException

from settings import OLLAMA_MODEL, logger, mcp_client
from helpers import serialize_content, get_tools_schema, tools_to_ollama_format
from schemas import ChatRequest

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest):
    """
    Send a natural-language message to Ollama. The model may choose to call
    one or more MCP tools; if it does, we execute them and return the results
    together with the assistant reply.
    """
    try:
        tools_schema = await get_tools_schema()
        data_tools = [t for t in tools_schema if not t["name"].endswith("_visual")]
        ollama_tools = tools_to_ollama_format(data_tools)

        messages: list[dict] = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant with access to tools. "
                    "When the user asks something that can be answered by a tool, "
                    "you MUST call it using the tool calling mechanism. "
                    "Do not describe the tool or its output — call it directly. "
                    "Always prefer using tools when available."
                ),
            }
        ]
        for h in req.history:
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
        messages.append({"role": "user", "content": req.message})

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=ollama_tools if ollama_tools else None,
        )

        assistant_msg = response.message
        tool_results: list[dict] = []

        if assistant_msg.tool_calls:
            for tc in assistant_msg.tool_calls:
                fn = tc.function
                try:
                    async with mcp_client:
                        result = await mcp_client.call_tool(fn.name, fn.arguments)
                    content = result.content if hasattr(result, "content") else result
                    if not isinstance(content, (list, tuple)):
                        content = [content]
                    visual_name = fn.name if fn.name.endswith("_visual") else f"{fn.name}_visual"
                    render_url = f"/api/mcp/render/{visual_name}?args={json.dumps(fn.arguments)}"
                    tool_results.append(
                        {
                            "tool": fn.name,
                            "arguments": fn.arguments,
                            "content": serialize_content(content),
                            "render_url": render_url,
                        }
                    )
                except Exception as tool_exc:
                    tool_results.append(
                        {
                            "tool": fn.name,
                            "arguments": fn.arguments,
                            "error": str(tool_exc),
                        }
                    )

            messages.append({"role": "assistant", "content": "", "tool_calls": assistant_msg.tool_calls})
            for tr in tool_results:
                content_text = json.dumps(tr.get("content", tr.get("error", "")))
                messages.append({"role": "tool", "content": content_text})

            followup = ollama.chat(model=OLLAMA_MODEL, messages=messages)
            final_text = followup.message.content or ""
        else:
            final_text = assistant_msg.content or ""

        return {
            "reply": final_text,
            "tool_calls": tool_results,
        }
    except Exception as exc:
        logger.error("chat error: %s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(exc))
