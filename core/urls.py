from django.contrib import admin
from django.urls import path
from core.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static



#Urls do aplicativo core
urlpatterns = [
   path('', loginPage, name='login'),
   path('login/', loginPage, name='login'),
   path('get-departments/', get_departments, name='get_departments'),
   path('get-visitors/', get_visitors_by_cpf, name='get_visitors'),
   path('add-visitors/', add_visitor, name='add_visitor'),
   path('add-visit/', add_visit, name='add_visit'),
   path('get-func-user/', get_func_user, name='get_func_user' ),
   path('funcionario/', get_visits_by_func, name='get_visits_by_func'),
   path('confirm-visit/', confirm_visit, name='confirm_visit'),
   path('atendente/', attendant_dashboard, name='atendente'),
   path('logout/', logoutView, name='logout'),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)