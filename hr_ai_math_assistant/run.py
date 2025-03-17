#!/usr/bin/env python3
import os
import sys
import subprocess
import pkg_resources
import platform

def check_python_version():
    """Check if Python version is 3.7 or higher."""
    required_version = (3, 7)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current Python version: {current_version[0]}.{current_version[1]}")
        sys.exit(1)

def check_dependencies():
    """Check if all required packages are installed."""
    with open('requirements.txt') as f:
        required_packages = [line.strip() for line in f if line.strip()]

    missing_packages = []
    
    for package in required_packages:
        try:
            pkg_resources.require(package)
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
    
    return missing_packages

def check_env_file():
    """Check if .env file exists and contains OPENAI_API_KEY."""
    if not os.path.exists('.env'):
        print("Warning: .env file not found.")
        create_env = input("Would you like to create it now? (y/n): ")
        if create_env.lower() == 'y':
            api_key = input("Please enter your OpenAI API key: ")
            with open('.env', 'w') as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
        else:
            print("Please create .env file with OPENAI_API_KEY before running the application.")
            sys.exit(1)

def install_dependencies(missing_packages):
    """Install missing dependencies."""
    print("Installing missing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies.")
        sys.exit(1)

def main():
    """Main function to run the application."""
    print("🤖 Starting AI Personal Assistant setup...")
    
    # Check Python version
    print("\nChecking Python version...")
    check_python_version()
    print("✅ Python version check passed")
    
    # Check dependencies
    print("\nChecking dependencies...")
    missing_packages = check_dependencies()
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        install = input("Would you like to install them now? (y/n): ")
        if install.lower() == 'y':
            install_dependencies(missing_packages)
        else:
            print("Please install required packages before running the application.")
            sys.exit(1)
    print("✅ All dependencies are installed")
    
    # Check .env file
    print("\nChecking environment configuration...")
    check_env_file()
    print("✅ Environment configuration check passed")
    
    # Start the application
    print("\n🚀 Starting the application...")
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
