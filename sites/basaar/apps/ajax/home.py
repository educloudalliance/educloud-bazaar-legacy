from django.shortcuts import render
from django_ajax.decorators import ajax

from random import randint

@ajax
def loadItems(request):
	#c = 5 + 3
    return render(request, 'ajax/items.html')
