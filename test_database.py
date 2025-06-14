#!/usr/bin/env python3
"""
Test script for database connectivity and MCP tools
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_database_connection():
    """Test database connection with provided credentials"""

    print("🔍 Database Connection Test")
    print("=" * 40)

    # Get database credentials from environment or prompt
    db_password = os.environ.get('DB_PASSWORD')
    if not db_password:
        print("❌ DB_PASSWORD environment variable not set")
        print("Please set it with: export DB_PASSWORD='your_password'")
        return False

    # Database configuration (matching server.py) - Using external connection
    DB_HOST = 'northamerica-northeast1-001.proxy.kinsta.app'
    DB_PORT = '30888'
    DB_NAME = 'spiritual-orange-blackbird'
    DB_USER = 'marmoset'

    print(f"Host: {DB_HOST}")
    print(f"Port: {DB_PORT}")
    print(f"Database: {DB_NAME}")
    print(f"User: {DB_USER}")
    print("Password: [HIDDEN]")

    try:
        print("\n🔌 Attempting connection...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=db_password,
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()

        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connected successfully!")
        print(f"PostgreSQL version: {version['version']}")

        # Check if codingLanguage table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'codingLanguage'
            );
        """)
        table_exists = cursor.fetchone()['exists']

        if table_exists:
            print("✅ codingLanguage table exists")

            # Get table structure
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'codingLanguage'
                ORDER BY ordinal_position;
            """)
            columns = cursor.fetchall()

            print("\n📋 Table structure:")
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                print(f"   {col['column_name']}: {col['data_type']} ({nullable})")

            # Count existing records
            cursor.execute('SELECT COUNT(*) as count FROM "codingLanguage";')
            count = cursor.fetchone()['count']
            print(f"\n📊 Current records: {count}")

        else:
            print("❌ codingLanguage table does not exist")
            print("You may need to create it first")

        cursor.close()
        conn.close()

        print("\n✅ Database test completed successfully!")
        return True

    except psycopg2.Error as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def show_usage_instructions():
    """Show instructions for using the new MCP tools"""

    print("\n🎯 MCP Tools Usage Instructions")
    print("=" * 40)

    print("New tools added to your MCP server:")
    print("1. add_coding_language(language_name, is_static=False, creator='system')")
    print("2. list_coding_languages()")

    print("\n📝 Example usage in Cursor:")
    print("• 'Add Python as a coding language'")
    print("• 'Add Java as a static coding language'")
    print("• 'List all coding languages'")
    print("• 'Add TypeScript created by Microsoft'")

    print("\n🚀 To test locally:")
    print("1. Set database password: export DB_PASSWORD='your_password'")
    print("2. Restart MCP server: venv/bin/python server.py")
    print("3. Test in Cursor with the examples above")

if __name__ == "__main__":
    success = test_database_connection()
    show_usage_instructions()

    if success:
        print("\n🎉 Ready to test the new database MCP tools!")
    else:
        print("\n⚠️  Fix database connection before testing MCP tools")
