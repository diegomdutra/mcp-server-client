import logging
import os

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8002))
MCP_SERVER_NAME = os.getenv("MCP_SERVER_NAME", "My MCP Server")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)
