from apps.account.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    MASCULINO = 'M'
    FEMININO = 'F'
    OPCOES_DE_SEXO = [
        (MASCULINO, 'Masculino'),
        (FEMININO, 'Feminino'),
    ]
    objects = CustomUserManager() # gerenciador de usuários
    username=None
    """ Campos Obrigatórios - Início"""
    email = models.EmailField(('email address'),unique=True)
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = []

    id_usuario = models.AutoField(primary_key=True)
    no_usuario = models.CharField(max_length=150, blank=False, null=False)
    """ Campos Obrigatórios - FIM"""
    
    """Campos Opcionais - INICIO"""
    dt_nascimento = models.DateField(blank=True,null=True)
    dh_registro = models.DateTimeField(auto_now_add=True)
    dh_alteracao = models.DateTimeField(auto_now=True)
    
    nu_celular = models.CharField(max_length=11, blank=True, null=True, unique=True)
    sexo = models.CharField(max_length=9, choices=OPCOES_DE_SEXO, null=True, blank=True)
    """Campos Opcionais - FIM"""