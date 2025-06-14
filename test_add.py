import httpx

# The MCP server endpoint
url = "http://localhost:8080/sse"

# MCP request parameters for the 'add' tool
params = {
    "tool": "add",
    "a": 333,
    "b": 443
}

# Send the request as a GET with query parameters
response = httpx.get(url, params=params, timeout=10)

print("Status code:", response.status_code)
print("Response:", response.text)
