from django.db.models.signals import post_migrate
from django.dispatch import receiver
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
    if not User.objects.filter(email='usuario@padrao.com').exists():
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