#!/usr/bin/env python
"""
Automate superuser creation for admin2@test.com
"""
import os
import sys
from pathlib import Path
import django

# Ensure project root is on PYTHONPATH so settings can be imported
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newcubebackend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin2_superuser():
    email = 'tafunum@example.com'
    password = 'Password123'
    username = 'newadmin'
    
    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(username, email, password)
        print(f'✓ Superuser "{email}" created successfully')
        print(f'  Username: {username}')
        print(f'  Password: {password}')
    else:
        print(f'✗ Superuser with email "{email}" already exists')

if __name__ == '__main__':
    create_admin2_superuser()
