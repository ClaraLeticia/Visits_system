from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Branch, Department

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    administrador = forms.BooleanField(required=False)
    atendente = forms.BooleanField(required=False)
    funcionario = forms.BooleanField(required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False, empty_label="Selecione uma unidade")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="Selecione um setor")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'administrador', 'atendente', 'funcionario', 'branch', 'department']


    def clean(self):
        cleaned_data = super().clean()
        atendente = cleaned_data.get("atendente")
        funcionario = cleaned_data.get("funcionario")
        branch = cleaned_data.get("branch")
        department = cleaned_data.get("department")

        # Se for atendente ou funcionário, a unidade e setor são obrigatórios
        if (atendente or funcionario) and not branch:
            self.add_error("branch", "Unidade é obrigatória para Atendentes e Funcionários.")
        if (atendente or funcionario) and not department:
            self.add_error("department", "Setor é obrigatório para Atendentes e Funcionários.")

        return cleaned_data
