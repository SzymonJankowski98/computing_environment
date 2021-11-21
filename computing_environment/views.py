from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

def landing(request):
    return render(request, 'landing/index.html')

def sign_in(request):
    return render(request, 'landing/sign_in.html')
