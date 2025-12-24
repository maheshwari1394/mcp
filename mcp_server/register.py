"""Register this MCP server with Claude Desktop.

Usage:
    python main.py --register
"""

import json
import os
import sys
from pathlib import Path
import platform
import logging

# ------------------------------------------------------------------------------
# Determine config location (Claude Desktop)
# ------------------------------------------------------------------------------
def _claude_config_path() -> Path:
    """Return the path to Claude Desktop's configuration file."""
    home = Path.home()
    if platform.system() == "Windows":
        return home / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    elif platform.system() == "Darwin":
        return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        # For Linux or unknown OS
        return home / ".config" / "Claude" / "claude_desktop_config.json"


def _load_config() -> dict:
    """Load the Claude Desktop config JSON (if it exists)."""
    path = _claude_config_path()
    if not path.exists():
        logging.warning(f"⚠️ Config not found: {path}")
        return {"mcpServers": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        logging.error(f"❌ Failed to parse {path}: {e}")
        return {"mcpServers": {}}


def _save_config(data: dict) -> None:
    """Save the modified Claude config back to disk."""
    path = _claude_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    logging.info(f"✅ Updated config at {path}")


# ------------------------------------------------------------------------------
# Registration logic
# ------------------------------------------------------------------------------
def _register_in_claude(
    server_name: str = "HR Leave Balancer Assistant (v5)",
    main_script: str = "main.py",
):
    """Register or update this MCP server entry in Claude Desktop."""

    # Determine full paths
    project_root = Path(__file__).resolve().parent.parent
    python_exe = Path(sys.executable)
    server_script = project_root / main_script

    # Ensure files exist
    if not python_exe.exists():
        raise FileNotFoundError(f"Python executable not found: {python_exe}")
    if not server_script.exists():
        raise FileNotFoundError(f"Main script not found: {server_script}")

    config = _load_config()
    mcp_servers = config.setdefault("mcpServers", {})

    mcp_servers[server_name] = {
        "command": [
            str(python_exe),
            str(server_script),
        ],
        "env": {},
    }

    _save_config(config)
    print(f"✅ Successfully registered MCP server: {server_name}")
    print(f"🗂️  Config path: {_claude_config_path()}")
    print(f"🐍 Python: {python_exe}")
    print(f"📜 Script: {server_script}")


if __name__ == "__main__":
    _register_in_claude()
