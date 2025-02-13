from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Branch, Department, Visitor, Visits
from django.utils import timezone
from datetime import timedelta

class VisitsForm(forms.Form):
    visitor = forms.ModelChoiceField(queryset=Visitor.objects.all(), empty_label="Selecione um visitante")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Selecione um setor")
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), empty_label="Selecione um funcionário", required=False)

    class Meta:
        model = Visits
        fields = ['visitor', 'department']

    def save(self):
        visit = Visits.objects.create(
            visitor=self.cleaned_data['visitor'],
            department=self.cleaned_data['department'],
            date= timezone.now() + timedelta(weeks=1, hours=-3),
            user=self.cleaned_data.get('user') # Lidar com o campo opcional
        )
        return visit


class VisitorForm(forms.Form):
    name = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11)
    rg = forms.CharField(max_length=9)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = Visitor
        fields = ['name', 'cpf', 'rg', 'phone']

    def save(self):
        visitor = Visitor.objects.aupdate_or_create(
            name=self.cleaned_data['name'],
            cpf=self.cleaned_data['cpf'],
            rg=self.cleaned_data['rg'],
            phone=self.cleaned_data['phone']
        )
        return visitor

    

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
        if (atendente) and not branch:
            self.add_error("branch", "Unidade é obrigatória para Atendentes e Funcionários.")
        if (funcionario) and not department and not branch:
            self.add_error("department", "Setor é obrigatório para Atendentes e Funcionários.")

        return cleaned_data
