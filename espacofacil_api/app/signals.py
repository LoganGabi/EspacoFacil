from django.db.models.signals import post_migrate
from django.dispatch import receiver

from app.views import auto_create_schedules

from .models import UserType, User
from django.conf import settings
from django.contrib.auth.hashers import make_password

@receiver(post_migrate)
def criar_tipos_usuario(sender, **kwargs):
    tipos = ['Usuario']
    for tipo in tipos:
        UserType.objects.get_or_create(type=tipo)

@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    if sender.name != 'app':
        return

    # Cria um tipo de usuário padrão se não existir
    user_type, created = UserType.objects.get_or_create(type='Administrador')

    # Verifica se o usuário padrão já existe
    if not User.objects.filter(email='admin@admin.com').exists():
        User.objects.create_user(
            name='admin',
            email='admin@admin.com',
            password='admin',
            phone='0000000000',
            user_type=user_type
        )
        print('Usuário padrão criado.')
    else:
        print('Usuário padrão já existe.')

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


# PELO BEM DO PAÍS, NAO DESCOMENTE
# @receiver(user_logged_in)
# def create_schedules_after_login(sender, request, user, **kwargs):
#     auto_create_schedules(request)
