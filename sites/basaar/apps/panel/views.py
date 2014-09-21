import uuid as libuuid
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
        f = NewForm(request.POST)
        if f.is_valid():
            cd = f.cleaned_data
            new_item = f.instance
            new_item.upc = createUPC()
            #f.save()
            new_item.save()

            # Create new instances in Stock Records
            f = StockRecord(product=new_item, partner=userPartner, price_excl_tax=cd['price'], price_retail=cd['price'], partner_sku=cd['uuid'], num_in_stock=1)
            f.save()

            return HttpResponseRedirect('/panel')
        else:
            errors = f.errors
            return render(request, 'panel/new.html', {'form': f, 'errors': errors})
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
            form.save()
            return HttpResponseRedirect('/panel')
        else:
            errors = form.errors
            form = EditForm(instance=product)
            return render(request, 'panel/edit.html', {'form': form, 'product': product, 'errors': errors})
    else:
        form = EditForm(instance=product)
        return render(request, 'panel/edit.html', {'form': form, 'product': product})

 #Create unique UPC for material
def createUPC():
    UPC = str(libuuid.uuid4())
    UPC = UPC.replace("-", "")
    UPC = UPC[0:10]

    while Product.objects.filter(upc=UPC).exists():
        UPC = str(libuuid.uuid4())
        UPC = UPC.replace("-", "")
        UPC = UPC[0:15]

    return UPC