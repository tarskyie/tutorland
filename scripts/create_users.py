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

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'AdminPass123!')
        print('Superuser `admin` created (password: AdminPass123!)')
    else:
        print('Superuser `admin` already exists')

def create_test_users():
    if not User.objects.filter(username='alice').exists():
        User.objects.create_user('alice', 'alice@example.com', 'StudentPass123!', role='student')
        print('Student user `alice` created (password: StudentPass123!)')
    else:
        print('Student user `alice` already exists')

    if not User.objects.filter(username='bob').exists():
        User.objects.create_user('bob', 'bob@example.com', 'TutorPass123!', role='tutor')
        print('Tutor user `bob` created (password: TutorPass123!)')
    else:
        print('Tutor user `bob` already exists')

if __name__ == '__main__':
    create_superuser()
    create_test_users()
