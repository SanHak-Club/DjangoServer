from django.shortcuts import render
from .models import Cad
from django.http import JsonResponse
from django.http import HttpResponse

def get_similar_cad(request):
    data = Cad.objects.all()
    print(data[0])

    result = [data[0]]
    
# Create your views here.