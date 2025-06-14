#!/usr/bin/env python3
"""
Verification script for MCP server tools
"""
import asyncio
import httpx

async def verify_mcp_server():
    """Verify the MCP server is running and show expected tools"""

    print("🔍 MCP Server Verification")
    print("=" * 40)

    # Test local server
    local_url = "http://localhost:8080/sse"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(local_url, timeout=5.0)
            if response.status_code == 200:
                print("✅ Local MCP Server: RUNNING")
                print(f"   URL: {local_url}")
                print(f"   Content-Type: {response.headers.get('content-type')}")
            else:
                print(f"❌ Local server error: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Local server connection failed: {e}")
            return

    print("\n📋 Available Tools:")
    tools = [
        "add(a: int, b: int) -> int",
        "get_secret_word() -> str",
        "get_current_weather(city: str) -> str",
        "get_current_time() -> str  [NEW!]"
    ]

    for i, tool in enumerate(tools, 1):
        print(f"   {i}. {tool}")

    print("\n🎯 How to Test in Cursor:")
    print("1. Make sure 'demo-mcp' is enabled in Cursor MCP settings")
    print("2. In a Cursor chat, try asking:")
    print("   - 'Add 333 and 443'")
    print("   - 'Get a secret word'")
    print("   - 'What time is it?'")
    print("   - 'What's the weather in London?'")

    print("\n✅ Server is ready for testing!")

if __name__ == "__main__":
    asyncio.run(verify_mcp_server())
