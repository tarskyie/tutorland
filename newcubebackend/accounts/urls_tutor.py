from django.urls import path
from .views import TutorProfileView, IsTutorView, TutorListView

urlpatterns = [
    path('', TutorProfileView.as_view(), name='tutor-profile'),
    path('is-tutor/', IsTutorView.as_view(), name='is-tutor'),
    path('list/', TutorListView.as_view(), name='tutor-list'),
]
