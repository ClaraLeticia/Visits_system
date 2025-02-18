from django.urls import path
from employeeApp.views import *

urlpatterns = [
    path('', employee_dashboard, name='employee_dashboard'), # Dashboard do funcionário
    path('confirm-visit/<int:pk>', confirm_visit, name='add_visit'), # Confirmação da visita

]