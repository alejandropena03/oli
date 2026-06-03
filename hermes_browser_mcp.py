#!/Users/alejandropena/.hermes/hermes-agent/venv/bin/python3
"""
MCP Server that exposes Hermes Agent's browser automation as MCP tools.
Allows opencode (and other MCP clients) to use Hermes's browser for
web research, navigation, and interaction.

Usage:
    python hermes_browser_mcp.py

Configure in opencode.jsonc:
    "mcp": {
        "hermes-browser": {
            "type": "local",
            "command": ["python3", "/path/to/hermes_browser_mcp.py"]
        }
    }
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path

HERMES_HOME = Path.home() / ".hermes"
HERMES_AGENT = HERMES_HOME / "hermes-agent"
VENV_PYTHON = HERMES_AGENT / "venv" / "bin" / "python3"

os.environ.setdefault("HERMES_HOME", str(HERMES_HOME))

sys.path.insert(0, str(HERMES_AGENT))

from mcp.server.fastmcp import FastMCP

from tools.browser_tool import (
    browser_navigate as _hermes_navigate,
    browser_snapshot as _hermes_snapshot,
    browser_click as _hermes_click,
    browser_type as _hermes_type,
    browser_scroll as _hermes_scroll,
    browser_back as _hermes_back,
    browser_press as _hermes_press,
    browser_get_images as _hermes_get_images,
    browser_vision as _hermes_vision,
)

mcp = FastMCP(
    "hermes-browser",
    instructions="""Browser automation via Hermes Agent.
Supports navigate, click, type, snapshot, scroll, back, press, get_images, and vision.
Use navigate() first to open a page, then interact with elements by their reference IDs
(e.g. @e1, @e2) shown in the snapshot output.""",
)

TASK_ID = "opencode_mcp"


@mcp.tool()
def browser_navigate(url: str) -> str:
    """Navigate to a URL and return the page content as a text snapshot.
    Args:
        url: The full URL to navigate to (include https://).
    """
    result = _hermes_navigate(url, task_id=TASK_ID)
    return result


@mcp.tool()
def browser_snapshot() -> str:
    """Get the current page state as an accessibility tree (text snapshot).
    Shows interactive elements with their reference IDs (e.g. @e1, @e3).
    """
    result = _hermes_snapshot(task_id=TASK_ID)
    return result


@mcp.tool()
def browser_click(ref: str) -> str:
    """Click an element identified by its reference ID.
    Args:
        ref: Element reference ID (e.g. @e1, @e3) from the snapshot.
    """
    result = _hermes_click(ref, task_id=TASK_ID)
    return result


@mcp.tool()
def browser_type(ref: str, text: str) -> str:
    """Type text into an input element.
    Args:
        ref: Element reference ID (e.g. @e5) from the snapshot.
        text: The text to type into the element.
    """
    result = _hermes_type(ref, text, task_id=TASK_ID)
    return result


@mcp.tool()
def browser_scroll(direction: str = "down") -> str:
    """Scroll the page in the specified direction.
    Args:
        direction: 'up' or 'down' (default: 'down').
    """
    result = _hermes_scroll(direction, task_id=TASK_ID)
    return result


@mcp.tool()
def browser_back() -> str:
    """Go back to the previous page in browser history."""
    result = _hermes_back(task_id=TASK_ID)
    return result


@mcp.tool()
def browser_press(key: str) -> str:
    """Press a keyboard key.
    Args:
        key: Key to press (e.g. 'Enter', 'Escape', 'Tab', 'ArrowDown').
    """
    result = _hermes_press(key, task_id=TASK_ID)
    return result


@mcp.tool()
def browser_get_images() -> str:
    """Get a summary of all images on the current page with their alt text and sizes.
    Returns JSON with image details.
    """
    result = _hermes_get_images(task_id=TASK_ID)
    return result


@mcp.tool()
def browser_vision(question: str) -> str:
    """Ask a question about the current page using AI vision.
    Takes a screenshot and answers based on what's visible.
    Args:
        question: What to ask about the current page content/visuals.
    """
    result = _hermes_vision(question, task_id=TASK_ID)
    return result


@mcp.tool()
def web_research(query: str) -> str:
    """Perform web research: search, navigate to results, and extract content.
    High-level tool that combines search and browsing into one step.
    Args:
        query: The research question or topic to investigate.
    """
    from tools.website_policy import check_website_access
    check_website_access(query)

    search_result = _hermes_navigate(
        f"https://www.google.com/search?q={__import__('urllib').parse.quote(query)}",
        task_id=TASK_ID
    )
    return search_result


if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run_stdio_async())
