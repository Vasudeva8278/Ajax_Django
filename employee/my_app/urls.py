from django.urls import path
from . import views
from .views import CreateEmployeeView, GetEmployeeView,UpdateEmployeeView,DeleteView

urlpatterns = [
    path('employees/', views.listEmployees, name='list_employees'), 
    path('employee/create/', views.createEmployee, name='create_employee'), 
    path('employee/update/<int:employeeId>/', views.updateEmployee, name='update_employee'),  
    path('employee/delete/<int:employeeId>/', views.deleteEmployee, name='delete_employee'), 
     path('reg/create/', CreateEmployeeView.as_view(), name='create_employee'), 
    path('employee/<int:pk>/', GetEmployeeView.as_view(), name='get_employee'),
    path('employee/<int:pk>/update/', UpdateEmployeeView.as_view(), name='update_employee'),
    path("delete/<int:id",DeleteView.as_view(),name='delete'),

]
