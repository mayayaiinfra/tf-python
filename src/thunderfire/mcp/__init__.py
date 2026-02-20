"""
THUNDERFIRE MCP Server

Usage:
    # Run as CLI:
    thunderfire-mcp --api-key tf_live_...

    # Or import:
    from thunderfire.mcp.server import main
    main()
"""

from .server import main

__all__ = ["main"]
