from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
#from django.contrib.auth.models import User
from django.template import RequestContext, loader
from oscar.core.loading import get_class, get_model
from forms import *

User = get_model('user', 'User')
Product = get_model('catalogue', 'product')
Partner = get_model('partner', 'partner')
Category = get_model('catalogue', 'category')
StockRecord = get_model('partner', 'stockrecord')
Language = get_model('catalogue', 'language')


def index(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    ids = StockRecord.objects.values_list('product', flat=True).filter(partner=userPartner)
    productList = Product.objects.filter(pk__in=set(ids))

    template = loader.get_template('panel/index.html')
    context = RequestContext(request, {
        'productList': productList,
    })
    return HttpResponse(template.render(context))


def new(request):
    if not request.user.is_authenticated():
        raise PermissionDenied()

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    if request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            save_edited_database()
            return HttpResponseRedirect('/panel')
    else:
        form = NewForm()
        return render(request, 'panel/new.html', {'form': form})


def edit(request, productUpc):
    if not request.user.is_authenticated():
        raise PermissionDenied()

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    product = get_object_or_404(Product, upc=productUpc)

    if request.method == 'POST':
        form = EditForm(request.POST, instance=product)
        if form.is_valid():
            cd = form.cleaned_data
            save_edited_database()
            return HttpResponseRedirect('/panel')
    else:
        form = EditForm(instance=product)
        return render(request, 'panel/edit.html', {'form': form, 'product': product})

def save_new_database():
    pass

def save_edited_database():
    pass