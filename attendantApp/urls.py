from django.contrib import admin
from django.urls import path
from attendantApp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static



#Urls do aplicativo core
urlpatterns = [
   path('get-departments/', get_departments, name='get_departments'), # View para retornar os setor
   path('get-visitors/', get_visitors_by_cpf, name='get_visitors'), # View para retornar os visitantes pelo cpf
   path('add-visitors/', add_visitor, name='add_visitor'), # Link para adicionar visitantes
   path('add-visit/', add_visit, name='add_visit'), # Link para adicionar visitas
   path('get-func-user/', get_func_user, name='get_func_user' ), # View para retornar os funcionários de um setor
   path('', attendant_dashboard, name='atendente'),
]
