from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.



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

    objects = CustomUserManager()

    def __str__(self):
        return self.username
