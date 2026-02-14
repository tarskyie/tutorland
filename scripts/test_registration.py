import sys
from pathlib import Path
import os

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newcubebackend.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()

client = Client()

payload = {
    'username': 'robert',
    'email': 'robert@example.com',
    'password': 'TutorPass123!',
    're_password': 'TutorPass123!',
    'role': 'tutor',
}

resp = client.post('/auth/users/', data=json.dumps(payload), content_type='application/json')
print('Status:', resp.status_code)
try:
    print('Response JSON:', resp.json())
except Exception:
    print('Response text:', resp.content.decode())

u = None
try:
    u = User.objects.get(username='robert')
    print('Stored role for robert:', u.role)
except User.DoesNotExist:
    print('User not created in DB')
