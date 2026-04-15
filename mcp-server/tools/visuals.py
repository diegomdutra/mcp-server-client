from prefab_ui.app import PrefabApp

from app.factory import mcp
from helpers.visuals import build_greet_visual, build_revenue_chart_visual


@mcp.tool(app=True)
def greet_visual(name: str) -> PrefabApp:
    """Greet someone with a visual card."""
    return build_greet_visual(name)


@mcp.tool(app=True)
def revenue_chart_visual(year: int) -> PrefabApp:
    """Show annual revenue as an interactive bar chart."""
    return build_revenue_chart_visual(year)
