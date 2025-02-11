from django.contrib import admin
from django.urls import path
from core.views import registerPage, loginPage, get_departments


#Urls do aplicativo core
urlpatterns = [
   path('register/', registerPage, name='register'),
   path('login/', loginPage, name='login'),
   path('get-departments/', get_departments, name='get_departments')
]