from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'product')
Partner = get_model('partner', 'partner')
Category = get_model('catalogue', 'category')
StockRecord = get_model('partner', 'stockrecord')
Language = get_model('catalogue', 'language')


def index(request):
    if not request.user.is_authenticated():
        raise PermissionDenied()

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    ids = StockRecord.objects.values_list('product', flat=True).filter(partner=userPartner)
    productList = Product.objects.filter(pk__in=set(ids))

    template = loader.get_template('editor/index.html')
    context = RequestContext(request, {
        'productList': productList,
    })
    return HttpResponse(template.render(context))


def edit(request, productUpc):
    if not request.user.is_authenticated():
        raise PermissionDenied()

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    product = get_object_or_404(Product, upc=productUpc)

    template = loader.get_template('editor/edit.html')
    context = RequestContext(request, {
        'product': product,
    })
    return HttpResponse(template.render(context))
