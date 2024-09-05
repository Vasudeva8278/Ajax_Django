# serializers.py
from rest_framework import serializers
from .models import UserProfile, WorkExperience, Qualification, Project

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    work_experience = WorkExperienceSerializer(many=True, read_only=True)
    qualifications = QualificationSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
