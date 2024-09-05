from django.urls import path
from . import views
from .views import CreateEmployeeView, GetEmployeeView,UpdateEmployeeView,EmployeeDeleteView
urlpatterns = [
    path('employees/', views.listEmployees, name='list_employees'), 
    path('reg/create/', CreateEmployeeView.as_view(), name='create_employee'), 
    path('employee/<int:pk>/', GetEmployeeView.as_view(), name='get_employee'),
    path('employee/<int:pk>/update/', UpdateEmployeeView.as_view(), name='update_employee'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='delete_employee'),
]

