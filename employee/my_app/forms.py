from django import forms
from .models import UserProfile, WorkExperience, Qualification, Project

class Profile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'age', 'gender', 'phone_no', 'hno', 'street', 'city', 'state']

class Experience(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'from_date', 'to_date', 'address']

class Qualifications(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['qualification_name', 'percentage']

class Projects(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'photo']
