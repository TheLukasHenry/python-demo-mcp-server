#!/usr/bin/env python3
"""
Simple MCP Server Status Check
"""
import subprocess
import sys

def check_server_status():
    """Check if the MCP server is running"""

    print("🔍 MCP Server Status Check")
    print("=" * 40)

    try:
        # Use curl to test the server
        result = subprocess.run(
            ["curl", "-s", "-I", "http://localhost:8080/sse"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and "200 OK" in result.stdout:
            print("✅ Local MCP Server: RUNNING")
            print("   URL: http://localhost:8080/sse")
            print("   Status: HTTP 200 OK")
        else:
            print("❌ Server not responding")
            return False

    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

    print("\n📋 Available Tools (Updated):")
    tools = [
        "1. add(a: int, b: int) -> int",
        "2. get_secret_word() -> str",
        "3. get_current_weather(city: str) -> str",
        "4. get_current_time() -> str  [NEW TOOL!]"
    ]

    for tool in tools:
        print(f"   {tool}")

    print("\n🎯 Test in Cursor:")
    print("Since you've enabled 'demo-mcp' in Cursor settings, try:")
    print("   • 'What time is it?' (tests the new get_current_time tool)")
    print("   • 'Add 100 and 200'")
    print("   • 'Get me a secret word'")
    print("   • 'What's the weather in Paris?'")

    print("\n✅ Server is ready! The new get_current_time tool should work!")
    return True

if __name__ == "__main__":
    check_server_status()
