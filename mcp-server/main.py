import sys

from app import create_mcp
from settings import PORT

mcp = create_mcp()

if __name__ == "__main__":
    try:
        mcp.run(transport="http", port=PORT)
    except KeyboardInterrupt:
        sys.exit(0)