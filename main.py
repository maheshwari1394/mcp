"""
Entry point for the HR Leave Balancer Assistant MCP Server (v5).
"""

import sys
import argparse
from mcp.server.fastmcp import FastMCP
from mcp_server import core  # sets up logging + JSON-safe stdout
from mcp_server import tools, resources, prompts  # loads MCP definitions


# ---------------------------------------------------------------------
# Initialize the FastMCP instance
# ---------------------------------------------------------------------
mcp = FastMCP("HR Leave Balancer Assistant (v5)")


def main():
    """Main entry point for running or registering the MCP server."""
    parser = argparse.ArgumentParser(description="HR Leave Balancer MCP Server")
    parser.add_argument(
        "--register",
        action="store_true",
        help="Register server in Claude Desktop",
    )
    parser.add_argument(
        "--unregister",
        action="store_true",
        help="Remove server from Claude Desktop",
    )
    args = parser.parse_args()

    # Lazy import to avoid circular dependencies
    from mcp_server.register import _register_in_claude, _claude_config_path

    # Ensure stdout works properly
    sys.stdout = core._sys_stdout_real

    if args.register:
        _register_in_claude()
        print(f"✅ Registered in Claude config: {_claude_config_path()}")
        return

    if args.unregister:
        _unregister_server()
        print("🗑️ Unregistered server from Claude config.")
        return

    # -----------------------------------------------------------------
    # Run the MCP server
    # -----------------------------------------------------------------
    print("🚀 HR Leave Balancer Assistant (v5) is running...")
    mcp.run()  # ✅ Correct method


def _unregister_server(server_name: str = "HR Leave Balancer Assistant (v5)"):
    """Remove the MCP entry from Claude Desktop config."""
    from mcp_server.register import _claude_config_path
    import json

    path = _claude_config_path()
    if not path.exists():
        print(f"⚠️ Config not found: {path}")
        return

    data = json.loads(path.read_text(encoding="utf-8"))
    if "mcpServers" in data and server_name in data["mcpServers"]:
        del data["mcpServers"][server_name]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"✅ Unregistered: {server_name}")
    else:
        print(f"ℹ️ No existing entry found for: {server_name}")


if __name__ == "__main__":
    main()
