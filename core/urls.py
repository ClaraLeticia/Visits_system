from django.contrib import admin
from django.urls import path
from core.views import registerPage, loginPage


#Urls do aplicativo core
urlpatterns = [
   path('register/', registerPage, name='register'),
   path('login/', loginPage, name='login'),
]