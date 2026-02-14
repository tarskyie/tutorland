import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newcubebackend.settings')

import django
django.setup()

from djoser.views import UserViewSet

vs = UserViewSet()
vs.action = 'create'
print('get_serializer_class ->', vs.get_serializer_class())
