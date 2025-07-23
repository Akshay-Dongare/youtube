from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import ToolNode

client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["mcp/math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp/",
            "transport": "streamable_http",
        },
    }
)

@tool
def sing_a_song() -> str:
  """Use this tool to sing a song for the user"""
  creatures_in_heaven = """I don't think I realize
  Just how much I miss you sometimes
  We were young and so in love
  We were just creatures in heaven
  I don't think I realize
  Just how much I miss you sometimes
  For a moment, we were just
  We were just creatures in heaven"""
  return creatures_in_heaven

@tool
def tell_a_joke() -> str:
  """Use this tool to tell a joke to the user"""
  joke = """How did the picture end up in prison?
  It was framed."""
  return joke

normal_tools = [sing_a_song, tell_a_joke]

def create_tool_node():
    mcp_tools = await client.get_tools()
    all_tools = list(mcp_tools) + normal_tools
    return ToolNode(
        tools=all_tools,
        name="Tools",
    )
