"""
THUNDERFIRE MCP Server

Python MCP server wrapping THUNDERFIRE tools.
"""

import os
import sys
import json
import asyncio
import argparse
from typing import Any

from ..client import ThunderFireClient
from ..types import TOOLS

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, Resource, TextContent
except ImportError:
    Server = None


async def run_server(config: dict):
    """Run the MCP server."""
    if Server is None:
        print("Error: MCP package not installed. Install with: pip install thunderfire[mcp]", file=sys.stderr)
        sys.exit(1)

    server = Server("thunderfire")
    client = ThunderFireClient(
        api_url=config["api_url"],
        api_key=config["api_key"],
        timeout=config["timeout"] / 1000
    )

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=t.name,
                description=t.description,
                inputSchema=t.parameters
            )
            for t in TOOLS
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        tool = next((t for t in TOOLS if t.name == name), None)
        if not tool:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        try:
            handler = getattr(client, tool.handler)
            result = await handler(**arguments)
            return [TextContent(type="text", text=json.dumps(result))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]

    @server.list_resources()
    async def list_resources() -> list[Resource]:
        return [
            Resource(
                uri="thunderfire://nodes",
                name="Node List",
                description="Live list of all connected THUNDERFIRE nodes",
                mimeType="application/json"
            ),
            Resource(
                uri="thunderfire://marketplace/catalog",
                name="Marketplace Catalog",
                description="Full TF Store marketplace catalog",
                mimeType="application/json"
            )
        ]

    @server.read_resource()
    async def read_resource(uri: str) -> str:
        if uri == "thunderfire://nodes":
            nodes = await client.node_list()
            return json.dumps(nodes, indent=2)
        elif uri == "thunderfire://marketplace/catalog":
            packages = await client.marketplace_search("")
            return json.dumps(packages, indent=2)
        else:
            raise ValueError(f"Unknown resource: {uri}")

    if config["debug"]:
        print(f"Connecting to {config['api_url']}...", file=sys.stderr)

    valid = await client.validate()
    if not valid:
        print(f"Warning: Cannot connect to TOP API at {config['api_url']}", file=sys.stderr)

    if config["debug"]:
        print(f"Registered {len(TOOLS)} tools", file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="THUNDERFIRE MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  thunderfire-mcp --api-key tf_live_xxx
  THUNDERFIRE_API_KEY=tf_live_xxx thunderfire-mcp
  thunderfire-mcp --api-url https://top.mayayai.com --api-key tf_live_xxx
        """
    )
    parser.add_argument("--api-url",
                        default=os.environ.get("THUNDERFIRE_API_URL", "http://localhost:8080"),
                        help="TOP API URL")
    parser.add_argument("--api-key",
                        default=os.environ.get("THUNDERFIRE_API_KEY", ""),
                        help="TOP API key (required)")
    parser.add_argument("--timeout", type=int,
                        default=int(os.environ.get("THUNDERFIRE_TIMEOUT", "30000")),
                        help="Request timeout in ms")
    parser.add_argument("--debug", action="store_true",
                        default=os.environ.get("THUNDERFIRE_DEBUG", "").lower() == "true",
                        help="Enable debug logging")
    parser.add_argument("--version", action="version", version="thunderfire-mcp 1.0.0")
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.api_key:
        print("Error: THUNDERFIRE_API_KEY required", file=sys.stderr)
        print("Set via --api-key argument or THUNDERFIRE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    config = {
        "api_url": args.api_url,
        "api_key": args.api_key,
        "timeout": args.timeout,
        "debug": args.debug
    }

    try:
        asyncio.run(run_server(config))
    except KeyboardInterrupt:
        if args.debug:
            print("Shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
