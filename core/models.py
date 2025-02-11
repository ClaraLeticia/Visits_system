from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=False, blank=False)
    
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
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    
@receiver(post_save, sender=CustomUser)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.administrador:
            group, _ = Group.objects.get_or_create(name="Administradores")
            permission = Permission.objects.get(codename="add_branch")
            group.permissions.add(permission)
            instance.groups.add(group)
        
        if instance.atendente:
            group, _ = Group.objects.get_or_create(name="Atendentes")
            permission = Permission.objects.get(codename="add_department")
            group.permissions.add(permission)
            instance.groups.add(group)
        
        if instance.funcionario:
            group, _ = Group.objects.get_or_create(name="Funcionários")
            permission = Permission.objects.get(codename="  view_department")
            group.permissions.add(permission)
            instance.groups.add(group)

