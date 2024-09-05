from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UserProfile, WorkExperience, Qualification, Project
from .forms import Profile, Experience, Qualifications, Projects
import json

def listEmployees(request):
    try:
        employees = UserProfile.objects.all()  # Fetch all employee records
        return render(request, 'employee/list.html', {'employees': employees})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Return error if there's any exception

# Create a new employee via AJAX
@require_POST
def createEmployee(request):
    try:
        data = json.loads(request.body)  # Parse JSON data from the request body
        profileForm = Profile(data)  # Bind the data to the Profile form

        if profileForm.is_valid():  # Check if the form data is valid
            employee = profileForm.save()  # Save the employee profile

            # Process additional fields (work experience, qualifications, projects) if provided
            work_experience = data.get('work_experience')
            if work_experience:
                for experience in work_experience:
                    experienceForm = Experience(experience)
                    if experienceForm.is_valid():
                        experience_instance = experienceForm.save(commit=False)
                        experience_instance.user_profile = employee  # Assign employee to experience
                        experience_instance.save()

            qualifications = data.get('qualifications')
            if qualifications:
                for qualification in qualifications:
                    qualificationForm = Qualifications(qualification)
                    if qualificationForm.is_valid():
                        qualification_instance = qualificationForm.save(commit=False)
                        qualification_instance.user_profile = employee  # Assign employee to qualification
                        qualification_instance.save()

            projects = data.get('projects')
            if projects:
                for project in projects:
                    projectForm = Projects(project)
                    if projectForm.is_valid():
                        project_instance = projectForm.save(commit=False)
                        project_instance.user_profile = employee  # Assign employee to project
                        project_instance.save()

            return JsonResponse({'message': 'Employee created successfully!'}, status=200)
        else:
            return JsonResponse({'error': profileForm.errors}, status=400)  # Return form validation errors
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Return error if there's an exception

# Update an existing employee via AJAX
@require_POST
def updateEmployee(request, employeeId):
    try:
        employee = get_object_or_404(UserProfile, id=employeeId)  # Fetch the employee to update
        data = json.loads(request.body)  # Parse JSON data from the request body
        profileForm = Profile(data, instance=employee)  # Bind data to form instance for update

        if profileForm.is_valid():  # Check if form data is valid
            profileForm.save()  # Save updated profile

            # Process work experience, qualifications, and projects as needed (similar to createEmployee)
            # You can add similar logic here for work_experience, qualifications, and projects update

            return JsonResponse({'message': 'Employee updated successfully!'}, status=200)
        else:
            return JsonResponse({'error': profileForm.errors}, status=400)  # Return form validation errors
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Return error if there's an exception

# Delete an employee via AJAX
@require_POST
def deleteEmployee(request, employeeId):
    try:
        employee = get_object_or_404(UserProfile, id=employeeId)  # Fetch the employee to delete
        employee.delete()  # Delete the employee
        return JsonResponse({'message': 'Employee deleted successfully!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Return error if there's an exception
