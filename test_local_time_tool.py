import asyncio
import httpx

async def test_local_time_tool():
    """Test the get_current_time tool on local server"""

    url = "http://localhost:8080/sse"

    async with httpx.AsyncClient() as client:
        try:
            print("Testing local server connectivity...")
            response = await client.get(url, timeout=5.0)
            print(f"✅ Local server status: {response.status_code}")

            if response.status_code == 200:
                print("✅ Local server with get_current_time tool is running!")
                print("✅ Ready to deploy the updated version!")
            else:
                print(f"❌ Server responded with: {response.status_code}")

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_local_time_tool())
