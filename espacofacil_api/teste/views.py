from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def teste(request):
    return HttpResponse("OLá")