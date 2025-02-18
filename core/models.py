from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from guardian.shortcuts import assign
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from .validators import *
# Create your models here.

# Model para visitantes
class Visitor(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True, validators=[validate_cpf]) # CPF é a chave primária
    rg = models.CharField(max_length=9, unique=True, validators=[validate_rg]) # RG é único
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, validators=[validate_phone])
    photo = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # Campo para armazenar a foto do visitante em um tamanho menor
    profile_picture = ImageSpecField(source='photo',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})


    def __str__(self):
        return self.name


# Model para setores
class Branch(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Model para unidades
class Department(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Customizando o gerenciador de usuários
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


# Customizando os campos de usuário para adicionar os campos de nivel de acesso
class CustomUser(AbstractUser):

    administrador = models.BooleanField(default=False) # Campo para verificar se o usuário é administrador
    atendente = models.BooleanField(default=False) # Campo para verificar se o usuário é atendente
    funcionario = models.BooleanField(default=False) # Campo para verificar se o usuário é funcionário
    email = models.EmailField(unique=True) # Campo de e-mail
    phone = models.CharField(max_length=20, null=False, blank=False, validators=[validate_phone])
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomUserManager()

    # Adicionando permissões para os usuários
    class Meta:
        permissions = [
            ('admin_permission', 'admin can view add and change branches,departments and users'),
            ('attendant_permission', 'attendant can view add and change visitors and visits'),
            ('employee_permission', 'employee can view add and change visits'),
        ]
    
    def __str__(self):
        return self.username
    
# Função para atribuir permissões aos usuários
# Como funciona o receiver:
# O receiver é um decorador que registra uma função para ser executada quando um sinal é enviado.
# O sinal é uma mensagem que envia informações sobre ações que ocorrem no Django.
# O sinal post_save é enviado sempre que um modelo é salvo.
# Neste caso, a função assign_user_permissions é chamada sempre que um CustomUser é salvo.
@receiver(post_save, sender=CustomUser)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.administrador: # Se o usuário for administrador
            group, _ = Group.objects.get_or_create(name="Administradores") # Cria o grupo de administradores
            assign('core.admin_permission', group) # Adiciona permissões para o grupo de administradores
            instance.groups.add(group) # Adiciona o usuário ao grupo de administradores
        
        if instance.atendente: # Se o usuário for atendente
            group, _ = Group.objects.get_or_create(name="Atendentes") # Cria o grupo de atendentes
            # Adicionando permissões para o grupo de atendentes
            assign('core.attendant_permission', group)
            instance.groups.add(group) # Adiciona o usuário ao grupo de atendentes
        
        if instance.funcionario: # Se o usuário for funcionário
            group, _ = Group.objects.get_or_create(name="Funcionários") # Cria o grupo de funcionários
            assign('core.employee_permission', group) # Adiciona permissões para o grupo de funcionários
            instance.groups.add(group) # Adiciona o usuário ao grupo de funcionários


# Model para visitas    
class Visits(models.Model):
    status = models.CharField(max_length=20, default='Agendada') # Status da visita
    visitor = models.ForeignKey('Visitor', on_delete=models.CASCADE) # Visitante
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True) # Usuário que registrou a visita
    department = models.ForeignKey('Department', on_delete=models.CASCADE) # Setor
    date = models.DateTimeField() # Data da visita

    def __str__(self):
        return self.visitor.name
    


    

