from django import forms
from django.contrib.auth.forms import UserCreationForm
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
        )
        return branch

class DepartmentForm(forms.Form):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="Selecione uma unidade")

    class Meta:
        model = Department
        fields = ['name', 'branch', 'description']


class VisitsForm(forms.ModelForm):
    '''
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Selecione um setor")
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), empty_label="Selecione um funcionário", required=False)
    '''

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


class VisitorForm(forms.Form):
    name = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11)
    rg = forms.CharField(max_length=9)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = Visitor
        fields = ['name', 'cpf', 'rg', 'phone']

    def save(self, commit=True):
        visitor, created = Visitor.objects.update_or_create(
            cpf=self.cleaned_data['cpf'],
            defaults={
                'name': self.cleaned_data['name'],
                'rg': self.cleaned_data['rg'],
                'phone': self.cleaned_data['phone']
            }
        )
        return visitor

    

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
        fields = ['username', 'email', 'password1', 'password2', 'administrador', 'atendente', 'funcionario', 'branch', 'department', 'first_name', 'last_name']


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
