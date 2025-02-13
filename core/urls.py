from django.contrib import admin
from django.urls import path
from core.views import registerPage, loginPage, get_departments, get_visitors_by_cpf, add_visitor, add_visit, get_func_user, get_visits_by_func


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

]