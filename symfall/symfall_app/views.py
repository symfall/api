from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions

# Create your views here.



def index(request):
    return HttpResponse("Hello World!")