from django.contrib import admin
from .models import UserProfile, WorkExperience, Qualification, Project

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'gender', 'phone_no', 'hno', 'street', 'city', 'state')
    search_fields = ('name', 'email')
    list_filter = ('gender', 'city')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'from_date', 'to_date', 'address', 'user_profile')
    search_fields = ('company_name', 'address')
    list_filter = ('user_profile',)

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('qualification_name', 'percentage', 'user_profile')
    search_fields = ('qualification_name',)
    list_filter = ('user_profile',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user_profile')
    search_fields = ('title', 'description')
    list_filter = ('user_profile',)
