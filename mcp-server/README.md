# MCP Server

An [MCP](https://modelcontextprotocol.io/) server built with [FastMCP](https://gofastmcp.com/) that exposes data tools and visual [PrefabUI](https://prefab-ui.com/) app tools, plus custom HTTP endpoints for rendering visual tools as embeddable HTML.

## Tech Stack

- **Python 3.13+**
- **FastMCP** — MCP protocol server (with apps support)
- **PrefabUI** — Visual component rendering
- **Starlette** — Custom HTTP routes
- **python-dotenv** — Environment variable management

## Project Structure

```
mcp-server/
├── main.py            # Entry point
├── settings.py        # Environment config (loads .env)
├── app/               # FastMCP app factory
├── helpers/           # Shared data helpers and visual builders
│   ├── data.py        # Data generation functions
│   └── visuals.py     # PrefabUI visual builders
├── tools/             # MCP tools
│   ├── data.py        # Data tools (greet, revenue_chart)
│   └── visuals.py     # App/visual tools (greet_visual, revenue_chart_visual)
├── routes/            # Custom HTTP routes
│   └── render.py      # GET /render, GET /render/{tool_name}
├── .env               # Environment variables (not committed)
└── pyproject.toml     # Project metadata and dependencies
```

## Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) (package manager)

## Getting Started

1. **Clone the repository** and navigate to the project folder:
   ```bash
   cd mcp-server
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment variables** — create a `.env` file in the project root:
   ```env
   PORT=8002
   MCP_SERVER_NAME=My MCP Server
   LOG_LEVEL=DEBUG
   ```

4. **Run the server:**
   ```bash
   uv run python main.py
   ```

   The MCP server will be available at `http://localhost:8002`.

## MCP Tools

| Tool                   | Type   | Description                                  |
|------------------------|--------|----------------------------------------------|
| `greet`                | Data   | Returns a structured greeting message        |
| `revenue_chart`        | Data   | Returns annual revenue data by quarter       |
| `greet_visual`         | Visual | Renders a greeting card with PrefabUI        |
| `revenue_chart_visual` | Visual | Renders a bar chart with PrefabUI            |

## HTTP Endpoints

| Method | Endpoint               | Description                         |
|--------|------------------------|-------------------------------------|
| GET    | `/render`              | List available visual tools         |
| GET    | `/render/{tool_name}`  | Render a visual tool as HTML        |

## Environment Variables

| Variable          | Default            | Description              |
|-------------------|--------------------|--------------------------|
| `PORT`            | `8002`             | Server port              |
| `MCP_SERVER_NAME` | `My MCP Server`    | MCP server display name  |
| `LOG_LEVEL`       | `DEBUG`            | Python logging level     |