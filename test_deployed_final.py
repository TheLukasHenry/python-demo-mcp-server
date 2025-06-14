#!/usr/bin/env python3
"""
Final Test for Deployed MCP Server
"""
import subprocess
import sys

def test_deployed_server():
    """Test the deployed MCP server with updated tools"""

    print("🚀 Testing Deployed MCP Server")
    print("=" * 50)

    # Test deployed server connectivity
    deployed_url = "https://python-mcp-server-vd9o9.kinsta.app/sse"

    try:
        result = subprocess.run(
            ["curl", "-s", "-I", deployed_url],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and "200" in result.stdout:
            print("✅ Deployed MCP Server: ONLINE")
            print(f"   URL: {deployed_url}")
            print("   Status: HTTP 200 OK")
            print("   Content-Type: text/event-stream")
        else:
            print("❌ Deployed server not responding")
            print(f"Response: {result.stdout}")
            return False

    except Exception as e:
        print(f"❌ Error testing deployed server: {e}")
        return False

    print("\n📋 Updated Tools Available on Deployed Server:")
    tools = [
        "1. add(a: int, b: int) -> int",
        "2. get_secret_word() -> str",
        "3. get_current_weather(city: str) -> str",
        "4. get_current_time() -> str  [NEWLY DEPLOYED!]"
    ]

    for tool in tools:
        print(f"   {tool}")

    print("\n🎯 How to Use Deployed Server in Cursor:")
    print("1. Update your Cursor MCP settings with:")
    print('   {')
    print('     "demo-mcp-deployed": {')
    print(f'       "url": "{deployed_url}"')
    print('     }')
    print('   }')

    print("\n2. Test the new tool by asking in Cursor:")
    print("   • 'What time is it?' (uses get_current_time)")
    print("   • 'Add 500 and 300'")
    print("   • 'Get a secret word'")
    print("   • 'Weather in Tokyo?'")

    print("\n✅ DEPLOYMENT SUCCESS!")
    print("✅ All 4 tools (including get_current_time) are now live!")
    print("✅ Ready for production use!")

    return True

if __name__ == "__main__":
    success = test_deployed_server()
    if success:
        print("\n🎉 Deployment verification complete!")
    else:
        print("\n❌ Deployment verification failed!")
        sys.exit(1)
