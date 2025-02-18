from django.contrib import admin
from django.urls import path
from core.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static



#Urls do aplicativo core
urlpatterns = [
   path('', loginPage, name='login'), # Página de login
   path('login/', loginPage, name='login'), # Página de login
   path('logout/', logoutView, name='logout'), # Realiza o logout
]

urlpatterns += staticfiles_urlpatterns() # Adiciona as urls dos arquivos estáticos

# Adiciona as urls dos arquivos de mídia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)