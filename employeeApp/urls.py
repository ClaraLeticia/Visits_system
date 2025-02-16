from django.urls import path
from employeeApp.views import *

urlpatterns = [
    path('', employee_dashboard, name='employee_dashboard'),
    path('confirm-visit/<int:pk>', confirm_visit, name='add_visit'),

]