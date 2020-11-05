from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def abc(request):
    return HttpResponse('Welcome to AlgoCourse! Fuck')
