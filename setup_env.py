#!/usr/bin/env python3
"""
Setup script to configure environment variables for the MCP server
"""
import os
import getpass

def setup_environment():
    """Setup environment variables for database connection"""

    print("🔧 MCP Server Environment Setup")
    print("=" * 40)

    # Check if .env file exists
    env_file = ".env"
    env_exists = os.path.exists(env_file)

    if env_exists:
        print(f"✅ Found existing {env_file} file")
        choice = input("Do you want to update it? (y/n): ").lower().strip()
        if choice != 'y':
            print("Setup cancelled.")
            return
    else:
        print(f"📝 Creating new {env_file} file")

    # Get database password securely
    print("\n🔐 Database Configuration:")
    print("Please enter your PostgreSQL database password")
    print("(This will be stored in .env file - make sure it's in .gitignore)")

    while True:
        password = getpass.getpass("DB_PASSWORD: ")
        if password.strip():
            break
        print("Password cannot be empty. Please try again.")

    # Create .env content
    env_content = f"""# Database Configuration for MCP Server
DB_PASSWORD={password}

# Database connection details (external connection)
DB_HOST=northamerica-northeast1-001.proxy.kinsta.app
DB_PORT=30888
DB_NAME=spiritual-orange-blackbird
DB_USER=marmoset

# Server configuration
PORT=8080
"""

    # Write to .env file
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)

        print(f"✅ Environment variables saved to {env_file}")

        # Update .gitignore to exclude .env
        gitignore_file = ".gitignore"
        if os.path.exists(gitignore_file):
            with open(gitignore_file, 'r') as f:
                gitignore_content = f.read()

            if '.env' not in gitignore_content:
                with open(gitignore_file, 'a') as f:
                    f.write('\n# Environment variables\n.env\n')
                print("✅ Added .env to .gitignore")

        print("\n🚀 Next steps:")
        print("1. Test database connection: venv/bin/python test_database.py")
        print("2. Start MCP server: venv/bin/python server.py")
        print("3. Test in Cursor with: 'Add Python as a coding language'")

        return True

    except Exception as e:
        print(f"❌ Error creating {env_file}: {str(e)}")
        return False

def show_alternative_methods():
    """Show alternative methods to set environment variables"""

    print("\n🔄 Alternative Methods:")
    print("=" * 40)

    print("1. Command Line (temporary):")
    print("   export DB_PASSWORD='your_password'")
    print("   venv/bin/python server.py")

    print("\n2. Shell Profile (permanent):")
    print("   echo 'export DB_PASSWORD=\"your_password\"' >> ~/.zshrc")
    print("   source ~/.zshrc")

    print("\n3. Docker/Deployment:")
    print("   Set as environment variable in your deployment platform")

    print("\n⚠️  Security Note:")
    print("   Never commit passwords to version control!")
    print("   Always use .env files or secure environment variable management")

if __name__ == "__main__":
    success = setup_environment()

    if not success:
        show_alternative_methods()

    print("\n📚 Environment Variable Locations:")
    print("✅ .env file (recommended for development)")
    print("✅ Shell environment (export command)")
    print("✅ Shell profile (~/.zshrc, ~/.bashrc)")
    print("❌ pyvenv.cfg (NOT for passwords!)")
    print("❌ Source code (NEVER!)")
