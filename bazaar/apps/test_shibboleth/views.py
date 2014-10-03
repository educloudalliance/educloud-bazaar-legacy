from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def foo(request):
   return HttpResponse(repr(request.META))
