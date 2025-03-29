from django.db import models
from rest_framework import serializers

from teste.models import Teste

class TesteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teste
        fields = '__all__'

