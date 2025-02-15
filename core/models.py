from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from guardian.shortcuts import assign_perm, assign, remove_perm
# Create your models here.

class Visitor(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    rg = models.CharField(max_length=9, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    '''
    img = models.ImageField(upload_to='visitors', null=False, blank=False)
    img_thumbnail = ImageSpecField(source='img',
                                   processors=[ResizeToFill(100, 50)],
                                   format='JPEG',
                                   options={'quality': 60})
    '''


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
    choices = (
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    )

    administrador = models.BooleanField(default=False)
    atendente = models.BooleanField(default=False)
    funcionario = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=False, blank=False)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=choices, default='Ativo')

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
@receiver(post_save, sender=CustomUser)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.administrador:
            group, _ = Group.objects.get_or_create(name="Administradores")
            assign('core.add_branch', group)
            instance.groups.add(group)
        
        if instance.atendente:
            group, _ = Group.objects.get_or_create(name="Atendentes")
            # Adicionando permissões para o grupo de atendentes
            permissions = ['core.add_visitor', 'core.view_visitor', 'core.delete_visitor', 'core.change_visitor', 'core.add_visits',]
            for perm in permissions:
                assign(perm, group)
            instance.groups.add(group)
        
        if instance.funcionario:
            group, _ = Group.objects.get_or_create(name="Funcionários")
            assign('core.change_confirm_visits_employee', group)
            instance.groups.add(group)

    
class Visits(models.Model):
    status = models.CharField(max_length=20, default='Agendada')
    visitor = models.ForeignKey('Visitor', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.visitor.name
    
    class Meta:
        permissions = [
            ('change_confirm_visits_employee', 'employee can change the status of visits'),
        ]

    

