from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.listEmployees, name='list_employees'), 
    path('employee/create/', views.createEmployee, name='create_employee'), 
    path('employee/update/<int:employeeId>/', views.updateEmployee, name='update_employee'),  
    path('employee/delete/<int:employeeId>/', views.deleteEmployee, name='delete_employee'),  
]
