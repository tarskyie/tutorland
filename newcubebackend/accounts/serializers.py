from djoser.serializers import (
    UserSerializer as DjoserUserSerializer,
    UserCreateSerializer as DjoserUserCreateSerializer,
    UserCreatePasswordRetypeSerializer as DjoserUserCreatePasswordRetypeSerializer,
)
from .models import User
from .models import StudentProfile, TutorProfile, Subject
from rest_framework import serializers

class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Debug: print incoming validated_data to verify 'role' presence
        try:
            print('UserCreateSerializer.create() validated_data:', validated_data)
        except Exception:
            pass

        role = validated_data.pop('role', User.STUDENT)
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        user.role = role
        if password:
            user.set_password(password)
        user.save()
        return user


class UserCreatePasswordRetypeSerializer(DjoserUserCreatePasswordRetypeSerializer):
    class Meta(DjoserUserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')

    def create(self, validated_data):
        role = validated_data.pop('role', User.STUDENT)
        user = super().create(validated_data)
        user.role = role
        user.save()
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, required=False)

    class Meta:
        model = StudentProfile
        fields = ('first_name', 'last_name', 'grade_level')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if 'first_name' in user_data:
            instance.user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            instance.user.last_name = user_data['last_name']
        instance.grade_level = validated_data.get('grade_level', instance.grade_level)
        instance.user.save()
        instance.save()
        return instance


class TutorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, required=False)
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = TutorProfile
        fields = ('first_name', 'last_name', 'subjects', 'hourly_rate', 'visibility')

    def get_subjects(self, instance):
        return [s.name for s in instance.subjects.all()]

    def to_internal_value(self, data):
        # Extract subjects before parent processing
        subjects_data = data.pop('subjects', None)
        
        ret = super().to_internal_value(data)
        
        # Pass subjects through to validated_data
        if subjects_data is not None:
            ret['subjects'] = subjects_data
        
        return ret

    def create_or_update_subjects(self, instance, subjects_list):
        instance.subjects.clear()
        for name in subjects_list:
            subj, _ = Subject.objects.get_or_create(name=name)
            instance.subjects.add(subj)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if 'first_name' in user_data:
            instance.user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            instance.user.last_name = user_data['last_name']
        
        subjects = validated_data.pop('subjects', None)
        if subjects is not None:
            self.create_or_update_subjects(instance, subjects)
        
        # Update hourly_rate and visibility if provided
        if 'hourly_rate' in validated_data:
            instance.hourly_rate = validated_data['hourly_rate']
        if 'visibility' in validated_data:
            instance.visibility = validated_data['visibility']
        
        instance.user.save()
        instance.save()
        return instance


class TutorListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = TutorProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'subjects', 'hourly_rate')

    def get_subjects(self, instance):
        return [s.name for s in instance.subjects.all()]
