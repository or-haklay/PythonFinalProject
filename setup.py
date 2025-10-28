#!/usr/bin/env python
"""
Setup script for the Blog Application
This script helps set up the Django backend and React frontend
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        print(f"Successfully ran: {command}")
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def setup_backend():
    """Set up the Django backend"""
    print("Setting up Django backend...")
    
    # Check if virtual environment exists
    venv_path = ".venv"
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        if not run_command("python -m venv .venv"):
            return False
    
    # Determine activation script based on OS
    if platform.system() == "Windows":
        activate_script = ".venv\\Scripts\\activate"
        pip_command = ".venv\\Scripts\\pip"
        python_command = ".venv\\Scripts\\python"
    else:
        activate_script = "source .venv/bin/activate"
        pip_command = ".venv/bin/pip"
        python_command = ".venv/bin/python"
    
    # Install requirements
    print("Installing Python dependencies...")
    if not run_command(f"{pip_command} install -r requirements.txt"):
        return False
    
    # Run migrations
    print("Running database migrations...")
    if not run_command(f"{python_command} manage.py makemigrations"):
        return False
    
    if not run_command(f"{python_command} manage.py migrate"):
        return False
    
    # Setup initial data
    print("Setting up initial data...")
    if not run_command(f"{python_command} manage.py setup_initial_data"):
        return False
    
    print("Django backend setup complete!")
    return True

def setup_frontend():
    """Set up the React frontend"""
    print("Setting up React frontend...")
    
    client_dir = "client"
    if not os.path.exists(client_dir):
        print("Client directory not found!")
        return False
    
    # Install npm dependencies
    print("Installing Node.js dependencies...")
    if not run_command("npm install", cwd=client_dir):
        return False
    
    print("React frontend setup complete!")
    return True

def main():
    """Main setup function"""
    print("Blog Application Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("Error: manage.py not found. Please run this script from the Django project root directory.")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("Frontend setup failed!")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    print("\nTo start the application:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Start React client: cd client && npm start")
    print("\nThe application will be available at:")
    print("- Backend API: http://127.0.0.1:8000/")
    print("- Frontend: http://localhost:3000/")
    print("\nSample users:")
    print("- Admin: admin / admin123")
    print("- Editor: editor / editor123")
    print("- User: user / user123")

if __name__ == "__main__":
    main()


