from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Branch, Department, Visitor, Visits
from django.utils import timezone
from datetime import timedelta


# Formulário para cadastro de visitantes
class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'description']
    
    # Método para salvar o formulário, se o branch já existir ele atualiza, senão ele cria um novo
    def save(self, commit=True, branch=None):  
        branch = Branch.objects.update_or_create(
            id=branch, 
            defaults={
                'name': self.cleaned_data['name'],
                'description': self.cleaned_data['description']
            }
        )[0]
        return branch
    

# Formulário para cadastro de setores
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'branch', 'description']

    # Método para salvar o formulário, se o department já existir ele atualiza, senão ele cria um novo
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

# Formulário para cadastro de visitantes
class VisitsForm(forms.ModelForm):

    class Meta:
        model = Visits
        fields = ['department', 'user']
    # Método para salvar o formulário
    def save(self, commit=True):
        visit = super().save(commit=False) # Cria o objeto de visitas, mas não salva no banco de dados
        visit.date = timezone.now() + timedelta(weeks=1, hours=-3) # Por padrão, toda visita é agendada para 1 semana após a data de criação
        visit.user = self.cleaned_data.get('user')  # Lidar com o campo opcional
        if commit: # Se commit for verdadeiro, salva a visita
            visit.save()
        return visit


# Formulário para cadastro de visitantes
class VisitorForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11)
    rg = forms.CharField(max_length=9)
    phone = forms.CharField(max_length=20)
    photo = forms.ImageField(required=False)

    class Meta:
        model = Visitor
        fields = ['name', 'cpf', 'rg', 'phone', 'photo']
    # Método para salvar o formulário
    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf')
        rg = cleaned_data.get('rg')
        # Verifica se o visitante já existe
        if cpf and rg:
            try:
                visitor = Visitor.objects.get(cpf=cpf)
                # Substitui a instância do formulário pelo visitante encontrado
                self.instance = visitor
            except Visitor.DoesNotExist:
                pass
        return cleaned_data
    # A função update_or_create não funciona com campos únicos, então foi necessário sobrescrever o método save

    def save(self, commit=True):
        visitor = super().save(commit=False) # Cria o objeto de visitante, mas não salva no banco de dados

        # Atualiza os campos
        visitor.name = self.cleaned_data['name']
        visitor.phone = self.cleaned_data['phone']
        visitor.rg = self.cleaned_data['rg']
        # Se o campo de foto foi preenchido, atualiza a foto
        if 'photo' in self.cleaned_data and self.cleaned_data['photo']:
            visitor.photo = self.cleaned_data['photo']

        if commit:
            visitor.save()
        return visitor


    
# Formulário para cadastro de usuários
class CustomUserCreationForm(UserCreationForm):
    # Customizando as mensagens de erro
    username = forms.CharField( max_length=150, error_messages={
            "unique": _("Este nome de usuário já está em uso."),
            "invalid": _("O nome de usuário pode conter apenas letras, números e @/./+/-/_"),
        })
    
    # Customizando as mensagens de erro
    email = forms.EmailField( error_messages={ "unique": _("Este e-mail já está cadastrado.")})

    # Customizando as mensagens de erro
    password2 = forms.CharField(error_messages={ "password_mismatch": _("As senhas não coincidem.")})

    # Definindo os valores 
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False, empty_label="Selecione uma unidade")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="Selecione um setor")
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'administrador', 'atendente', 'funcionario', 'branch', 'department', 'first_name', 'last_name', 'phone']


    # Método para limpar os campos
    def clean(self):
        cleaned_data = super().clean()
        atendente = cleaned_data.get("atendente")
        funcionario = cleaned_data.get("funcionario")
        branch = cleaned_data.get("branch")
        department = cleaned_data.get("department")

        # Se for atendente a unidade é obrigatório
        if (atendente) and not branch:
            self.add_error("branch", "Unidade é obrigatória para Atendentes.")
        # Se for funcionário unidade e setor são obrigatórios
        if (funcionario) and not department and not branch:
            self.add_error("department", "Unidade e Setor é obrigatório para Funcionários.")

        return cleaned_data


# Formulário para edição de usuários
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'administrador', 'atendente', 'funcionario', 'branch', 'department', 'first_name', 'last_name', 'phone']
        