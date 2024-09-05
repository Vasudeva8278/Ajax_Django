from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UserProfile, WorkExperience, Qualification, Project
from .forms import Profile, Experience, Qualifications, Projects
import json
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

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



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def deleteEmployee(request, employeeId):
    try:
        employee = get_object_or_404(UserProfile, id=employeeId)  # Fetch the employee to delete
        employee.delete()  # Delete the employee
        return JsonResponse({'message': 'Employee deleted successfully!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)







from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserProfileSerializer,WorkExperienceSerializer,QualificationSerializer,ProjectSerializer


class CreateEmployeeView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            profile_serializer = UserProfileSerializer(data=data)
            if profile_serializer.is_valid():
                employee = profile_serializer.save()

                # Process additional fields if provided
                for experience in data.get('work_experience', []):
                    experience_serializer = WorkExperienceSerializer(data=experience)
                    if experience_serializer.is_valid():
                        experience_serializer.save(user_profile=employee)

                for qualification in data.get('qualifications', []):
                    qualification_serializer = QualificationSerializer(data=qualification)
                    if qualification_serializer.is_valid():
                        qualification_serializer.save(user_profile=employee)

                for project in data.get('projects', []):
                    project_serializer = ProjectSerializer(data=project)
                    if project_serializer.is_valid():
                        project_serializer.save(user_profile=employee)

                return Response({'message': 'Employee created successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetEmployeeView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            employee_id = kwargs.get('pk')  # Get the employee ID from URL parameters
            if not employee_id:
                return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                employee = UserProfile.objects.get(id=employee_id)  # Fetch the employee
            except UserProfile.DoesNotExist:
                return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserProfileSerializer(employee)  # Serialize the employee data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




class UpdateEmployeeView(APIView):
    def put(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')
        if not employee_id:
            return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employee = UserProfile.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update logic as per your original implementation
        # Make sure you're using `partial=True` in the serializer if you're updating only parts of the data
        profile_serializer = UserProfileSerializer(employee, data=request.data, partial=True)
        
        if profile_serializer.is_valid():
            profile_serializer.save()
            # Continue handling the work_experience, qualifications, and projects
            # Logic already looks correct for these parts
        else:
            return Response({'error': profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Employee updated successfully!'}, status=status.HTTP_200_OK)

        


class EmployeeDeleteView(DeleteView):
    model = UserProfile
    success_url = reverse_lazy('employee_list')  # Redirect URL after successful deletion

    def delete(self, request, *args, **kwargs):
        try:
            # Call the parent delete method
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({"message": "Employee deleted successfully."}, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "Employee not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)