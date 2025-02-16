from django.contrib import admin
from django.urls import path
from adminApp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static



#Urls do aplicativo core
urlpatterns = [
   path('', admin_dashboard, name='admin_dashboard'),
   path('add-users/', add_users, name='add_users'),
   path('update-user/<int:pk>', update_user, name='update_user'),
   path('add-branch/', add_branch, name='add_branch'),
   path('update-branch/<int:pk>', update_branch, name='update_branch'),
   path('add-department/', add_department, name='add_department'),
   path('update-department/<int:pk>', update_department, name='update_department'),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)