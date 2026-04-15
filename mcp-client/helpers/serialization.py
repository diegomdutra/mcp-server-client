from settings import logger


def serialize_content(content_list) -> list[dict]:
    """Turn fastmcp content objects into JSON-safe dicts."""
    items = []
    for c in content_list:
        logger.debug("Content item type=%s attrs=%s", type(c).__name__, dir(c))
        entry: dict = {"type": getattr(c, "type", "text")}
        if hasattr(c, "text"):
            entry["text"] = c.text
        if hasattr(c, "data"):
            entry["data"] = c.data
        if hasattr(c, "model_dump"):
            try:
                dumped = c.model_dump()
                for k, v in dumped.items():
                    if k not in entry:
                        entry[k] = v
            except Exception:
                pass
        items.append(entry)
    return items
