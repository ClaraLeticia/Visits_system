from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CustomUser, Branch , Department, Visitor, Visits
from guardian.admin import  GuardedModelAdmin

# Register your models here.

user = get_user_model()



admin.site.register(Visits)

# Customizando a exibição dos usuários no painel de administração
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'administrador', 'atendente', 'funcionario']

class CustomBranchAdmin(admin.ModelAdmin):
    list_display = ['name']


class CustomDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

# Registrando o modelo CustomUser no painel de administração
admin.site.register(user, CustomUserAdmin)

# Registrando os modelos Branch e Department no painel de administração
admin.site.register(Branch, CustomBranchAdmin)
admin.site.register(Department, CustomDepartmentAdmin)

admin.site.register(Visitor)
