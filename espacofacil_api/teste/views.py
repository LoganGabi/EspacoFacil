from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets,status
from rest_framework.response import Response

from teste.models import Teste
from teste.serializers import TesteSerializer


class teste(viewsets.ModelViewSet):
    queryset = Teste.objects.all()
    serializer_class = TesteSerializer


    #  NA URLS.PY OS METODOS SAO CRIADOS AUTOMATICAMENTE, MAS SE FOR NECESSARIO FAZER UM CRUD MAIS COMPLEXO,
    # PODE-SE SOBRECREVER O METODO

    def create(self, request, *args, **kwargs):
        data = request.data  # Pega os dados enviados no POST
        if len(data.get('nomeTeste')) > 10:
            return Response({"error": "O nomeTeste deve ser menor que 10 caracteres"}, status=status.HTTP_400_BAD_REQUEST)

        # Se passar pela validação, segue com o fluxo normal
        return super().create(request, *args, **kwargs)

    
