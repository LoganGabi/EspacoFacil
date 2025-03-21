from django.db import models

# Create your models here.
from django.db import models

class Teste(models.Model):
    nomeTeste = models.CharField(max_length=100)