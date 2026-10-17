from django.shortcuts import render
from django.http import HttpResponse
# Create your views here
def HelloProject(request):
    return HttpResponse ("hellow zee")
    