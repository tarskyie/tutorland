import sys
from pathlib import Path
import os

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newcubebackend.settings')

import django
django.setup()

from newcubebackend.accounts.serializers import UserCreateSerializer

data = {
    'username': 'robert2',
    'email': 'robert2@example.com',
    'password': 'TutorPass123!',
    're_password': 'TutorPass123!',
    'role': 'tutor',
}

serializer = UserCreateSerializer(data=data)
if not serializer.is_valid():
    print('Serializer invalid:', serializer.errors)
else:
    user = serializer.save()
    print('Created user:', user.username, 'role=', user.role)
