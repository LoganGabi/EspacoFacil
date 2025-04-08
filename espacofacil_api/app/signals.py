from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import UserType  # certifique-se que o import é do seu model certo

@receiver(post_migrate)
def criar_tipos_usuario(sender, **kwargs):
    tipos = ['Administrador', 'Usuario']
    for tipo in tipos:
        UserType.objects.get_or_create(type=tipo)