from django.db import models
from rest_framework import serializers

class TesteSerializer(models.Model):
    nomeTeste = models.CharField(max_length=100)
