from django.contrib import admin
from django.urls import path
from core.views import registerPage, loginPage, get_departments, get_visitors, add_visitor, add_visit, get_func_user


#Urls do aplicativo core
urlpatterns = [
   path('', loginPage, name='login'),
   path('register/', registerPage, name='register'),
   path('login/', loginPage, name='login'),
   path('get-departments/', get_departments, name='get_departments'),
   path('get-visitors/', get_visitors, name='get_visitors'),
   path('add-visitors/', add_visitor, name='add_visitor'),
   path('add-visit/', add_visit, name='add_visit'),
   path('get-func-user/', get_func_user, name='get_func_user' )

]