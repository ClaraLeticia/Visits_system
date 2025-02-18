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

class Visitor(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True, validators=[validate_cpf])
    rg = models.CharField(max_length=9, unique=True, validators=[validate_rg])
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, validators=[validate_phone])
    photo = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    profile_picture = ImageSpecField(source='photo',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})


    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

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

    administrador = models.BooleanField(default=False)
    atendente = models.BooleanField(default=False)
    funcionario = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=False, blank=False, validators=[validate_phone])
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomUserManager()

    class Meta:
        permissions = [
            ('admin_permission', 'admin can view add and change branches,departments and users'),
            ('attendant_permission', 'attendant can view add and change visitors and visits'),
            ('employee_permission', 'employee can view add and change visits'),
        ]
    
    def __str__(self):
        return self.username
    
@receiver(post_save, sender=CustomUser)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.administrador:
            group, _ = Group.objects.get_or_create(name="Administradores")
            assign('core.admin_permission', group)
            instance.groups.add(group)
        
        if instance.atendente:
            group, _ = Group.objects.get_or_create(name="Atendentes")
            # Adicionando permissões para o grupo de atendentes
            assign('core.attendant_permission', group)
            instance.groups.add(group)
        
        if instance.funcionario:
            group, _ = Group.objects.get_or_create(name="Funcionários")
            assign('core.employee_permission', group)
            instance.groups.add(group)

    
class Visits(models.Model):
    status = models.CharField(max_length=20, default='Agendada')
    visitor = models.ForeignKey('Visitor', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.visitor.name
    


    

