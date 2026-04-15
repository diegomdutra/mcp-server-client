from fastmcp import FastMCP

from settings import MCP_SERVER_NAME

mcp = FastMCP(MCP_SERVER_NAME)


def create_mcp() -> FastMCP:
    """Build and configure the FastMCP application."""
    import tools.data  # noqa: F401
    import tools.visuals  # noqa: F401
    import routes.render  # noqa: F401

    return mcp
