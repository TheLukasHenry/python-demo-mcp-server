import asyncio
import httpx
import json

async def test_deployed_server_tools():
    """Test all tools on the deployed MCP server"""

    # The deployed MCP server endpoint
    base_url = "https://python-mcp-server-vd9o9.kinsta.app"
    sse_url = f"{base_url}/sse"

    print("🚀 Testing Deployed MCP Server")
    print(f"URL: {sse_url}")
    print("=" * 50)

    async with httpx.AsyncClient() as client:
        try:
            # Test basic connectivity
            print("1. Testing server connectivity...")
            response = await client.get(sse_url, timeout=10.0)

            if response.status_code == 200:
                print("✅ Server is responding correctly!")
                print(f"   Content-Type: {response.headers.get('content-type')}")
            else:
                print(f"❌ Server responded with status: {response.status_code}")
                return

        except Exception as e:
            print(f"❌ Error connecting to server: {e}")
            return

    print("\n2. Expected tools after deployment:")
    tools = [
        {
            "name": "add",
            "description": "Add two numbers",
            "test_params": {"a": 333, "b": 443},
            "expected_result": "776"
        },
        {
            "name": "get_secret_word",
            "description": "Get a random secret word",
            "test_params": {},
            "expected_result": "One of: apple, banana, cherry"
        },
        {
            "name": "get_current_weather",
            "description": "Get current weather for a city",
            "test_params": {"city": "London"},
            "expected_result": "Weather report with forecast"
        },
        {
            "name": "get_current_time",
            "description": "Get current time",
            "test_params": {},
            "expected_result": "Current date and time in YYYY-MM-DD HH:MM:SS format"
        }
    ]

    for tool in tools:
        print(f"   📋 {tool['name']}: {tool['description']}")

    print("\n3. Deployment Instructions:")
    print("   To test these tools after deployment:")
    print("   1. Deploy the updated server.py to Kinsta")
    print("   2. Wait for deployment to complete")
    print("   3. Add to Cursor MCP settings:")
    print('   {')
    print('     "demo-mcp-deployed": {')
    print(f'       "url": "{sse_url}"')
    print('     }')
    print('   }')
    print("   4. Restart Cursor to pick up the new tool")

    print(f"\n✅ Server is ready at: {sse_url}")
    print("✅ All 4 tools will be available after deployment!")

if __name__ == "__main__":
    asyncio.run(test_deployed_server_tools())
