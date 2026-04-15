def _greet_data(name: str) -> dict:
    return {"greeting": f"Hello, {name}!", "status": "Greeted"}


def _revenue_data(year: int) -> dict:
    data = [
        {"quarter": "Q1", "revenue": 42000},
        {"quarter": "Q2", "revenue": 51000},
        {"quarter": "Q3", "revenue": 47000},
        {"quarter": "Q4", "revenue": 63000},
    ]
    total = sum(d["revenue"] for d in data)
    return {"year": year, "quarters": data, "total_revenue": total}
