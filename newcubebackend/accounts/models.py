from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STUDENT = 'student'
    TUTOR = 'tutor'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TUTOR, 'Tutor'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    @property
    def is_student(self):
        return self.role == self.STUDENT

    @property
    def is_tutor(self):
        return self.role == self.TUTOR


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='student_profile')
    grade_level = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"StudentProfile({self.user.username})"


class TutorProfile(models.Model):
    VISIBLE = 'visible'
    HIDDEN = 'hidden'

    VISIBILITY_CHOICES = [
        (VISIBLE, 'Visible'),
        (HIDDEN, 'Hidden'),
    ]

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='tutor_profile')
    subjects = models.ManyToManyField(Subject, blank=True, related_name='tutors')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Hourly rate in currency units")
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default=VISIBLE)

    def __str__(self):
        return f"TutorProfile({self.user.username})"
