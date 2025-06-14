import asyncio
import httpx

async def test_deployed_mcp_server():
    """Test the deployed MCP server connectivity"""

    # The deployed MCP server endpoint
    url = "https://python-mcp-server-vd9o9.kinsta.app/sse"

    async with httpx.AsyncClient() as client:
        try:
            print("Testing deployed MCP server connectivity...")
            print(f"URL: {url}")

            # Test basic connectivity
            response = await client.get(url, timeout=10.0)
            print(f"✅ Server connection status: {response.status_code}")

            if response.status_code == 200:
                print("✅ Deployed MCP server is responding correctly!")
                print("✅ Ready to be added to Cursor MCP settings")
            else:
                print(f"⚠️  Server responded with status: {response.status_code}")
                print(f"Response: {response.text[:200]}...")

        except httpx.TimeoutException:
            print("❌ Connection timed out - server might be starting up")
        except httpx.ConnectError:
            print("❌ Could not connect to the server")
        except Exception as e:
            print(f"❌ Error connecting to server: {e}")

if __name__ == "__main__":
    asyncio.run(test_deployed_mcp_server())
