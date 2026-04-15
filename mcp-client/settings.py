import logging
import os

from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()

PORT = os.getenv("PORT", "8003")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8002/mcp")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:e2b")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

mcp_client = Client(MCP_SERVER_URL)
