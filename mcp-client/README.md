# MCP Client

A bridge API that connects a frontend application to an [MCP](https://modelcontextprotocol.io/) server and [Ollama](https://ollama.com/) for AI-powered tool calling. It exposes a REST API via FastAPI, enabling natural-language chat with automatic MCP tool execution.

## Tech Stack

- **Python 3.13+**
- **FastAPI** — REST API framework
- **Uvicorn** — ASGI server
- **FastMCP** — MCP protocol client
- **Ollama** — Local LLM inference with tool calling
- **HTTPX** — Async HTTP client
- **python-dotenv** — Environment variable management

## Project Structure

```
mcp-client/
├── main.py            # Entry point
├── settings.py        # Environment config (loads .env)
├── app/               # FastAPI app factory
├── routes/            # API route handlers
│   ├── chat.py        # POST /api/mcp/chat
│   └── tools.py       # GET/POST /api/mcp/tools, render proxy
├── schemas/           # Pydantic request models
├── helpers/           # Serialization and tool utilities
├── .env               # Environment variables (not committed)
└── pyproject.toml     # Project metadata and dependencies
```

## Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) (package manager)
- [Ollama](https://ollama.com/) running locally with a model pulled
- MCP server running (default: `http://localhost:8002/mcp`)

## Getting Started

1. **Clone the repository** and navigate to the project folder:
   ```bash
   cd mcp-client
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment variables** — create a `.env` file in the project root:
   ```env
   MCP_SERVER_URL=http://localhost:8002/mcp
   OLLAMA_MODEL=gemma4:e2b
   LOG_LEVEL=DEBUG
   ```

4. **Run the server:**
   ```bash
   uv run python main.py
   ```

   The API will be available at `http://localhost:8003`.

## API Endpoints

| Method | Endpoint                    | Description                              |
|--------|-----------------------------|------------------------------------------|
| GET    | `/api/mcp/tools`            | List available MCP tools                 |
| POST   | `/api/mcp/tools/call`       | Call a specific MCP tool                 |
| GET    | `/api/mcp/render/{tool}`    | Proxy visual HTML render from MCP server |
| POST   | `/api/mcp/chat`             | Chat with Ollama using MCP tool calling  |

## Environment Variables

| Variable         | Default                        | Description                  |
|------------------|--------------------------------|------------------------------|
| `MCP_SERVER_URL` | `http://localhost:8002/mcp`    | MCP server endpoint          |
| `OLLAMA_MODEL`   | `gemma4:e2b`                   | Ollama model for chat        |
| `LOG_LEVEL`      | `DEBUG`                        | Python logging level         |