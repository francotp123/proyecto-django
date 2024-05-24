from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def mainpage(request):
    return HttpResponse('Hello world!')