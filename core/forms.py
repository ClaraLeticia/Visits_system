from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# Customizando o formulário de criação de usuário para adicionar os campos de perfil
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'administrador', 'atendente', 'funcionario')
