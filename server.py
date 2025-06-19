import logging
import os
import random
import sys
from datetime import datetime

import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

name="demo-mcp-server"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(name)

# Get port from environment variable or use 8080 as default
port = int(os.environ.get('PORT', 8080))

# Database configuration - Using external connection
# Updated to match Sevalla's environment variable names
DB_HOST = os.environ.get('DB_HOST', 'northamerica-northeast1-001.proxy.kinsta.app')
DB_PORT = os.environ.get('DB_PORT', '30888')
DB_NAME = os.environ.get('DB_DATABASE', os.environ.get('DB_NAME', 'spiritual-orange-blackbird'))  # Sevalla uses DB_DATABASE
DB_USER = os.environ.get('DB_USERNAME', os.environ.get('DB_USER', 'marmoset'))  # Sevalla uses DB_USERNAME
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')  # Same in both

def get_db_connection():
    """Get database connection"""
    try:
        # Log connection attempt (without password for security)
        logger.info(f"Attempting database connection to {DB_HOST}:{DB_PORT}/{DB_NAME} as {DB_USER}")

        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor,
            connect_timeout=10  # Add connection timeout
        )
        logger.info("Database connection successful")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        logger.error(f"Connection details - Host: {DB_HOST}, Port: {DB_PORT}, Database: {DB_NAME}, User: {DB_USER}")
        raise

# Create server with lifespan
mcp = FastMCP(name, logger=logger, port=port)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    logger.info(f"Tool called: add({a}, {b})")
    return a + b


@mcp.tool()
def get_secret_word() -> str:
    """Get a random secret word"""
    logger.info("Tool called: get_secret_word()")
    return random.choice(["apple", "banana", "cherry"])


@mcp.tool()
def get_current_weather(city: str) -> str:
    """Get current weather for a city"""
    logger.info(f"Tool called: get_current_weather({city})")

    try:
        endpoint = "https://wttr.in"
        response = requests.get(f"{endpoint}/{city}", timeout=10)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return f"Error fetching weather data: {str(e)}"


@mcp.tool()
def get_current_time() -> str:
    """Get current time"""
    logger.info("Tool called: get_current_time()")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@mcp.tool()
def test_database_connection() -> str:
    """Test database connection and return status info"""
    logger.info("Tool called: test_database_connection()")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Test basic connectivity
        cursor.execute('SELECT version();')
        version_result = cursor.fetchone()

        # Test if our table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'codingLanguage'
            );
        """)
        table_exists = cursor.fetchone()['exists']

        cursor.close()
        conn.close()

        result = f"✅ Database Connection: SUCCESS\n"
        result += f"📝 PostgreSQL Version: {version_result['version']}\n"
        result += f"📋 codingLanguage table: {'EXISTS' if table_exists else 'MISSING'}\n"
        result += f"🔗 Connected as: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        return result

    except Exception as e:
        error_msg = f"❌ Database Connection: FAILED\n"
        error_msg += f"🔗 Attempted: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}\n"
        error_msg += f"❌ Error: {str(e)}"
        logger.error(f"Database connection test failed: {str(e)}")
        return error_msg


@mcp.tool()
def add_coding_language(name: str, is_static: bool = False, creator: str = "system") -> str:
    """Add a new coding language to the database

    Args:
        name: Name of the programming language (e.g., 'Python', 'JavaScript')
        is_static: Whether the language is statically typed (default: False)
        creator: Creator/author of the language entry (default: 'system')

    Returns:
        Success message with the created language ID
    """
    logger.info(f"Tool called: add_coding_language({name}, {is_static}, {creator})")

    if not DB_PASSWORD:
        return "Error: Database password not configured. Please set DB_PASSWORD environment variable."

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

                        # Insert new coding language
        insert_query = """
            INSERT INTO "codingLanguage" (name, "isStatic", creator)
            VALUES (%s, %s, %s)
            RETURNING id;
        """

        cursor.execute(insert_query, (name, is_static, creator))
        result = cursor.fetchone()
        language_id = result['id']

        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Successfully added coding language: {name} with ID: {language_id}")
        return f"Successfully added coding language '{name}' with ID: {language_id} (isStatic: {is_static}, creator: {creator})"

    except psycopg2.Error as e:
        logger.error(f"Database error while adding coding language: {str(e)}")
        return f"Error adding coding language: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error while adding coding language: {str(e)}")
        return f"Unexpected error: {str(e)}"


@mcp.tool()
def list_coding_languages() -> str:
    """List all coding languages from the database

    Returns:
        Formatted list of all coding languages with their details
    """
    logger.info("Tool called: list_coding_languages()")

    if not DB_PASSWORD:
        return "Error: Database password not configured. Please set DB_PASSWORD environment variable."

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get all coding languages
        select_query = """
            SELECT id, name, "isStatic", creator
            FROM "codingLanguage"
            ORDER BY id;
        """

        cursor.execute(select_query)
        languages = cursor.fetchall()

        cursor.close()
        conn.close()

        if not languages:
            return "No coding languages found in the database."

        # Format the results
        result = "Coding Languages:\n"
        result += "-" * 50 + "\n"
        for lang in languages:
            static_type = "Static" if lang['isStatic'] else "Dynamic"
            result += f"ID: {lang['id']} | {lang['name']} | Type: {static_type} | Creator: {lang['creator']}\n"

        logger.info(f"Retrieved {len(languages)} coding languages")
        return result

    except psycopg2.Error as e:
        logger.error(f"Database error while listing coding languages: {str(e)}")
        return f"Error retrieving coding languages: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error while listing coding languages: {str(e)}")
        return f"Unexpected error: {str(e)}"

if __name__ == "__main__":
    # Determine transport based on environment
    # If running in a web environment (PORT set), use SSE
    # If running locally/CLI, use stdio
    try:
        if os.environ.get('PORT'):
            logger.info(f"Starting MCP Server with SSE transport on port {port}...")
            mcp.run(transport="sse")
        else:
            logger.info("Starting MCP Server with stdio transport...")
            mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        logger.info("Server terminated")
