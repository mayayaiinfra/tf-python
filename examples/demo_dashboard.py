#!/usr/bin/env python3
"""
THUNDERFIRE Demo Dashboard

A simple terminal dashboard demonstrating the THUNDERFIRE Python SDK.
Shows node health, THETA status, and marketplace search.

Usage:
    export THUNDERFIRE_API_URL=http://localhost:8080
    export THUNDERFIRE_API_KEY=tf_test_demo
    python demo_dashboard.py
"""

import asyncio
import os
import sys
from datetime import datetime

# Add parent directory to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from thunderfire import ThunderFireClient
except ImportError:
    print("Install thunderfire: pip install thunderfire")
    sys.exit(1)


def print_header(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    """Print a simple ASCII table."""
    widths = [max(len(h), max(len(str(r[i])) for r in rows) if rows else 0)
              for i, h in enumerate(headers)]

    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    sep_line = "-+-".join("-" * w for w in widths)

    print(header_line)
    print(sep_line)
    for row in rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(row, widths)))


class DemoDashboard:
    """Terminal dashboard for THUNDERFIRE monitoring."""

    def __init__(self, api_url: str = None, api_key: str = None):
        self.api_url = api_url or os.getenv("THUNDERFIRE_API_URL", "http://localhost:8080")
        self.api_key = api_key or os.getenv("THUNDERFIRE_API_KEY", "tf_test_demo")
        self.client = None

    async def connect(self) -> bool:
        """Initialize the client connection."""
        print(f"Connecting to {self.api_url}...")
        self.client = ThunderFireClient(
            api_url=self.api_url,
            api_key=self.api_key
        )
        # Test connection
        try:
            await self.client.status()
            print("Connected!")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    async def show_nodes(self) -> None:
        """Display all nodes with health status."""
        print_header("Node Fleet Status")

        try:
            nodes = await self.client.node_list()
            if not nodes:
                print("No nodes found.")
                return

            rows = []
            for node in nodes:
                status_icon = {
                    "online": "●",
                    "offline": "○",
                    "degraded": "◐",
                }.get(node.get("status", ""), "?")

                rows.append([
                    node.get("id", "?"),
                    node.get("name", "Unnamed"),
                    node.get("tier", "?"),
                    f"{status_icon} {node.get('status', '?')}",
                    str(node.get("health", "?")) + "%",
                ])

            print_table(["ID", "Name", "Tier", "Status", "Health"], rows)
        except Exception as e:
            print(f"Error fetching nodes: {e}")

    async def show_theta_status(self, node_id: str = None) -> None:
        """Display THETA decision engine status."""
        print_header("THETA Decision Engine")

        if not node_id:
            # Get first node
            try:
                nodes = await self.client.node_list()
                if nodes:
                    node_id = nodes[0].get("id")
            except Exception:
                pass

        if not node_id:
            print("No node available for THETA status.")
            return

        try:
            theta = await self.client.theta_status(node_id)

            print(f"Node: {node_id}")
            print(f"Stage: {theta.get('stage', '?')}")
            print(f"Cycle Count: {theta.get('cycle_count', '?')}")
            print(f"Current Goal: {theta.get('current_goal', 'None')}")
            print(f"Efficiency: {theta.get('efficiency', 0):.2%}")

            # THETA stage diagram
            stages = ["G", "V0", "V1", "C", "Ap", "Obe", "Ae", "Oe", "Δ", "Ac", "Ti", "η"]
            current = theta.get("stage", "")
            diagram = " → ".join(
                f"[{s}]" if s == current else s
                for s in stages
            )
            print(f"\nPipeline: {diagram}")
        except Exception as e:
            print(f"Error fetching THETA status: {e}")

    async def show_marketplace(self, query: str = "") -> None:
        """Search and display marketplace packages."""
        print_header(f"TF Store Marketplace{' - Search: ' + query if query else ''}")

        try:
            packages = await self.client.marketplace_search(query)
            if not packages:
                print("No packages found.")
                return

            rows = []
            for pkg in packages[:10]:  # Show top 10
                rows.append([
                    pkg.get("name", "?"),
                    pkg.get("version", "?"),
                    pkg.get("tier_min", "?"),
                    "✓" if pkg.get("installed") else "",
                    pkg.get("description", "")[:40],
                ])

            print_table(["Name", "Version", "Min Tier", "Installed", "Description"], rows)
        except Exception as e:
            print(f"Error searching marketplace: {e}")

    async def show_chitral(self, node_id: str = None) -> None:
        """Display CHITRAL health breakdown."""
        print_header("CHITRAL Health Status")

        if not node_id:
            try:
                nodes = await self.client.node_list()
                if nodes:
                    node_id = nodes[0].get("id")
            except Exception:
                pass

        if not node_id:
            print("No node available.")
            return

        try:
            chitral = await self.client.chitral_status(node_id)

            print(f"Node: {node_id}")
            print(f"Format: {chitral.get('format', '?')}")
            print(f"Size: {chitral.get('size', '?')} bytes")
            print()

            fields = chitral.get("fields", {})
            for key, value in fields.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"Error fetching CHITRAL status: {e}")

    async def run_demo(self) -> None:
        """Run the full demo dashboard."""
        print("\n" + "="*60)
        print("  THUNDERFIRE Demo Dashboard")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        if not await self.connect():
            print("\nDemo requires a running THUNDERFIRE TOP server.")
            print("Start with: top --serve --port 8080")
            return

        await self.show_nodes()
        await self.show_theta_status()
        await self.show_marketplace("navigation")
        await self.show_chitral()

        print_header("Demo Complete")
        print("For more examples, see:")
        print("  - examples/langchain_agent.py")
        print("  - examples/crewai_crew.py")
        print("  - examples/autogen_chat.py")


async def main():
    """Main entry point."""
    dashboard = DemoDashboard()
    await dashboard.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
