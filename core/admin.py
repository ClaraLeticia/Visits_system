from django.contrib import admin
from .models import CustomUser

# Register your models here.

# Customizando a exibição dos usuários no painel de administração
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'administrador', 'atendente', 'funcionario']


# Registrando o modelo CustomUser no painel de administração
admin.site.register(CustomUser, CustomUserAdmin)