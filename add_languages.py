#!/usr/bin/env python3
"""
Script to add Python and Java as coding languages to the database
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def add_coding_languages():
    """Add Python and Java to the coding languages database"""

    print("🐍 Adding Python and Java to Database")
    print("=" * 40)

    # Database configuration
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

    if not DB_PASSWORD:
        print("❌ DB_PASSWORD not configured")
        return False

    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()

        # Languages to add
        languages = [
            {
                "name": "Python",
                "is_static": False,  # Python is dynamically typed
                "creator": "Python Software Foundation"
            },
            {
                "name": "Java",
                "is_static": True,   # Java is statically typed
                "creator": "Oracle Corporation"
            }
        ]

        print("Adding languages:")

        for lang in languages:
            # Insert language
            insert_query = """
                INSERT INTO "codingLanguage" (name, "isStatic", creator)
                VALUES (%s, %s, %s)
                RETURNING id;
            """

            cursor.execute(insert_query, (lang["name"], lang["is_static"], lang["creator"]))
            result = cursor.fetchone()
            language_id = result['id']

            type_str = "Static" if lang["is_static"] else "Dynamic"
            print(f"✅ {lang['name']}: ID {language_id} | {type_str} | Creator: {lang['creator']}")

        # Commit changes
        conn.commit()

        # Show all entries
        print("\n📋 All coding language entries:")
        cursor.execute('SELECT id, name, "isStatic", creator FROM "codingLanguage" ORDER BY id;')
        all_languages = cursor.fetchall()

        for lang in all_languages:
            type_str = "Static" if lang['isStatic'] else "Dynamic"
            print(f"   ID: {lang['id']} | {lang['name']} | Type: {type_str} | Creator: {lang['creator']}")

        cursor.close()
        conn.close()

        print(f"\n✅ Successfully added {len(languages)} coding languages!")
        print(f"✅ Total entries in database: {len(all_languages)}")

        return True

    except psycopg2.Error as e:
        print(f"❌ Database error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_mcp_tools():
    """Show how to test the MCP tools in Cursor"""

    print("\n🎯 Test MCP Tools in Cursor:")
    print("=" * 40)

    print("Now that Python and Java are added, you can test:")
    print("1. 'List all coding languages' - Should show the entries we just added")
    print("2. 'Add a static coding language created by Microsoft' - Add TypeScript")
    print("3. 'Add a dynamic coding language created by system' - Add a generic entry")

    print("\n📊 Expected Results:")
    print("- Python: Dynamic typing, created by Python Software Foundation")
    print("- Java: Static typing, created by Oracle Corporation")
    print("- Plus any additional entries you add via MCP tools")

if __name__ == "__main__":
    success = add_coding_languages()

    if success:
        test_mcp_tools()
        print("\n🎉 Python and Java successfully added to database!")
        print("🚀 Ready to test MCP tools in Cursor!")
    else:
        print("\n❌ Failed to add languages. Check database connection.")
