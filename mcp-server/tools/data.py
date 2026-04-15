from app.factory import mcp
from helpers.data import _greet_data, _revenue_data


@mcp.tool()
def greet(name: str) -> dict:
    """Greet someone and return structured data with the greeting message."""
    return _greet_data(name)


@mcp.tool()
def revenue_chart(year: int) -> dict:
    """Return annual revenue data broken down by quarter."""
    return _revenue_data(year)
