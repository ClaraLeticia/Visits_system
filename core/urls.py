from django.contrib import admin
from django.urls import path
from core.views import *


#Urls do aplicativo core
urlpatterns = [
   path('', loginPage, name='login'),
   path('register/', registerPage, name='register'),
   path('login/', loginPage, name='login'),
   path('get-departments/', get_departments, name='get_departments'),
   path('get-visitors/', get_visitors_by_cpf, name='get_visitors'),
   path('add-visitors/', add_visitor, name='add_visitor'),
   path('add-visit/', add_visit, name='add_visit'),
   path('get-func-user/', get_func_user, name='get_func_user' ),
   path('func/get-visits/', get_visits_by_func, name='get_visits_by_func'),
   path('confirm-visit/', confirm_visit, name='confirm_visit'),
   path('add-branch/', add_branch, name='add_branch'),
   path('add-department/', add_department, name='add_department'),
   path('list-branches/', list_branches, name='list_branches'),
]