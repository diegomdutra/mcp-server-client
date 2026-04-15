from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text, Badge, Row
from prefab_ui.components.charts import BarChart, ChartSeries

from helpers.data import _greet_data, _revenue_data


def build_greet_visual(name: str) -> PrefabApp:
    info = _greet_data(name)
    with Column(gap=4, css_class="p-6") as view:
        Heading(info["greeting"])
        with Row(gap=2, align="center"):
            Text("Status")
            Badge(info["status"], variant="success")
    return PrefabApp(view=view)


def build_revenue_chart_visual(year: int) -> PrefabApp:
    info = _revenue_data(int(year))
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"{info['year']} Revenue")
        BarChart(
            data=info["quarters"],
            series=[ChartSeries(data_key="revenue", label="Revenue")],
            x_axis="quarter",
        )
    return PrefabApp(view=view)


VISUAL_BUILDERS = {
    "greet_visual": build_greet_visual,
    "revenue_chart_visual": build_revenue_chart_visual,
}
