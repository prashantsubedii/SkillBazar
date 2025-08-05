#!/usr/bin/env python3
"""
Simple script to run the SkillBazar Django development server
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("Error: manage.py not found. Please run this script from the SkillBazar project root.")
        sys.exit(1)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Virtual environment not detected. Consider activating your virtual environment.")
    
    # Check if requirements are installed
    try:
        import django
        print(f"Django {django.get_version()} detected.")
    except ImportError:
        print("Error: Django not found. Please install requirements:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Run migrations if needed
    print("Running migrations...")
    subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
    
    # Create superuser if none exists
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print("\nNo superuser found. Creating one...")
            subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
    except Exception as e:
        print(f"Warning: Could not check/create superuser: {e}")
    
    # Populate demo data if needed
    try:
        from gigs.models import Gig
        if not Gig.objects.exists():
            print("No gigs found. Populating demo data...")
            subprocess.run([sys.executable, 'manage.py', 'populate_demo_data'], check=True)
    except Exception as e:
        print(f"Warning: Could not populate demo data: {e}")
    
    # Start the development server
    print("\nStarting SkillBazar development server...")
    print("Access the site at: http://localhost:8000")
    print("Admin panel at: http://localhost:8000/admin")
    print("Press Ctrl+C to stop the server.")
    
    subprocess.run([sys.executable, 'manage.py', 'runserver'])

if __name__ == '__main__':
    main() 