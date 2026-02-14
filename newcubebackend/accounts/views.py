from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import StudentProfile, TutorProfile, Subject
from .serializers import StudentProfileSerializer, TutorProfileSerializer, TutorListSerializer

User = get_user_model()


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.STUDENT


class IsTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.TUTOR


class StudentProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        serializer = StudentProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TutorProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def get(self, request):
        profile, _ = TutorProfile.objects.get_or_create(user=request.user)
        serializer = TutorProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile, _ = TutorProfile.objects.get_or_create(user=request.user)
        serializer = TutorProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IsTutorView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTutor]

    def get(self, request):
        return Response({'detail': 'You are a tutor!'}, status=status.HTTP_200_OK)


class TutorListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Get list of visible tutors with optional filtering.
        
        Query parameters:
        - min_hourly_rate: Minimum hourly rate (float)
        - max_hourly_rate: Maximum hourly rate (float)
        - subjects: Comma-separated list of subject names to filter by
        
        Example: /api/tutors/list/?min_hourly_rate=10&max_hourly_rate=50&subjects=math,physics
        """
        # Start with visible tutors only
        queryset = TutorProfile.objects.filter(visibility=TutorProfile.VISIBLE)
        
        # Filter by min hourly rate
        min_rate = request.query_params.get('min_hourly_rate')
        if min_rate is not None:
            try:
                queryset = queryset.filter(hourly_rate__gte=float(min_rate))
            except ValueError:
                return Response(
                    {'error': 'min_hourly_rate must be a valid number'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Filter by max hourly rate
        max_rate = request.query_params.get('max_hourly_rate')
        if max_rate is not None:
            try:
                queryset = queryset.filter(hourly_rate__lte=float(max_rate))
            except ValueError:
                return Response(
                    {'error': 'max_hourly_rate must be a valid number'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Filter by subjects (if any subject matches)
        subjects_param = request.query_params.get('subjects')
        if subjects_param:
            subject_names = [s.strip() for s in subjects_param.split(',')]
            queryset = queryset.filter(subjects__name__in=subject_names).distinct()
        
        serializer = TutorListSerializer(queryset, many=True)
        return Response(serializer.data)