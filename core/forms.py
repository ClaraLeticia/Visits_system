from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Branch, Department, Visitor, Visits
from django.utils import timezone
from datetime import timedelta

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'description']
    
    def save(self, commit=True, branch=None):  
        branch = Branch.objects.update_or_create(
            id=branch, 
            defaults={
                'name': self.cleaned_data['name'],
                'description': self.cleaned_data['description']
            }
        )[0]
        return branch

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'branch', 'description']

    def save(self, commit=True, department=None):
        department = Department.objects.update_or_create(
            id=department,
            defaults={
                'name': self.cleaned_data['name'],
                'branch': self.cleaned_data['branch'],
                'description': self.cleaned_data['description']
            }
        )
        return department


class VisitsForm(forms.ModelForm):

    class Meta:
        model = Visits
        fields = ['department', 'user']

    def save(self, commit=True):
        visit = super().save(commit=False)
        visit.date = timezone.now() + timedelta(weeks=1, hours=-3)
        visit.user = self.cleaned_data.get('user')  # Lidar com o campo opcional
        if commit:
            visit.save()
        return visit


class VisitorForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11)
    rg = forms.CharField(max_length=9)
    phone = forms.CharField(max_length=20)
    photo = forms.ImageField()

    class Meta:
        model = Visitor
        fields = ['name', 'cpf', 'rg', 'phone', 'photo']


    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    administrador = forms.BooleanField(required=False)
    atendente = forms.BooleanField(required=False)
    funcionario = forms.BooleanField(required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False, empty_label="Selecione uma unidade")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="Selecione um setor")
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'administrador', 'atendente', 'funcionario', 'branch', 'department', 'first_name', 'last_name', 'phone']


    def clean(self):
        cleaned_data = super().clean()
        atendente = cleaned_data.get("atendente")
        funcionario = cleaned_data.get("funcionario")
        branch = cleaned_data.get("branch")
        department = cleaned_data.get("department")

        # Se for atendente ou funcionário, a unidade e setor são obrigatórios
        if (atendente) and not branch:
            self.add_error("branch", "Unidade é obrigatória para Atendentes.")
        if (funcionario) and not department and not branch:
            self.add_error("department", "Unidade e Setor é obrigatório para Funcionários.")

        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'administrador', 'atendente', 'funcionario', 'branch', 'department', 'first_name', 'last_name', 'phone']
        