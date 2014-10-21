import uuid as libuuid
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
#from django.contrib.auth.models import User
from django.template import RequestContext, loader
from django import forms
from django.template.defaultfilters import slugify
from oscar.core.loading import get_class, get_model
from forms import *

User = get_model('user', 'User')
Product = get_model('catalogue', 'product')
Partner = get_model('partner', 'partner')
Category = get_model('catalogue', 'category')
StockRecord = get_model('partner', 'stockrecord')
Language = get_model('catalogue', 'language')
Tag = get_model('catalogue', 'Tags')
EmbeddedMedia = get_model('catalogue', 'EmbeddedMedia')


def index(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    template = loader.get_template('panel/index.html')

    return render(request, 'panel/index.html')


def stats(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    template = loader.get_template('panel/index.html')

    return render(request, 'panel/index.html')


def help(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    template = loader.get_template('panel/index.html')

    return render(request, 'panel/index.html')


def products(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    ids = StockRecord.objects.values_list('product', flat=True).filter(partner=userPartner)
    productList = Product.objects.filter(pk__in=set(ids))

    template = loader.get_template('panel/products/index.html')
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
            new_item.save()

            # Save icon
            if cd["iconUrl"] is not None:
                #Download icon if one is specified
                new_item.iconUrl = cd["iconUrl"]
                new_item.saveIcon()

            # Save embedded media
            # Remove possible whitespaces
            embedString = cd['embedMedia']
            embedString = embedString.replace(" ", "")
            embedList = embedString.split(',')

            for media in embedList:
                embedEntry = EmbeddedMedia.create()
                embedEntry.url = media
                embedEntry.product = new_item
                embedEntry.save()

            # Save tags
            # Remove possible whitespaces
            tagsString = cd['tags']
            tagsString = tagsString.replace(" ", "")
            tagsList = tagsString.split(',')

            for tag in tagsList:
                #check if the tag is already in db, if not create it
                if Tag.objects.filter(name=tag).exists():
                    t = Tag.objects.get(name=tag)
                    t.hasTags.add(new_item)
                else:
                    tagEntry = Tag.create()
                    tagEntry.name = tag
                    tagEntry.save()
                    tagEntry.hasTags.add(new_item)

            # Slugify uuid
            uuid = cd['uuid']
            uuid = slugify(uuid)

            # Create new instances in Stock Records
            # TODO AWFUL BUG FIX
            if cd['price'] == 0:
                price = 0.01
            else:
                price = cd['price']

            f = StockRecord(product=new_item, partner=userPartner, price_excl_tax=price, price_retail=price, partner_sku=uuid, num_in_stock=1)
            f.save()

            return HttpResponseRedirect('/panel/products')
        else:
            errors = f.errors
            return render(request, 'panel/products/new.html', {'form': f, 'errors': errors})
    else:
        form = NewForm()
        return render(request, 'panel/products/new.html', {'form': form})


def edit(request, productUpc):
    if not request.user.is_authenticated():
        raise PermissionDenied()

    user = User.objects.get(username=request.user.username)
    try:
        userPartner = Partner.objects.get(users=user)
    except Partner.DoesNotExist:
        raise PermissionDenied()

    product = get_object_or_404(Product, upc=productUpc)

    stock = StockRecord.objects.get(product=product)
    price = stock.price_retail
    embedList = EmbeddedMedia.objects.filter(product=product)
    tagsList = Tag.objects.filter(hasTags=product)

    tagArray = []
    embedArray = []

    for tag in tagsList:
        tagArray.append(tag.name)

    for embed in embedList:
        embedArray.append(embed.url)

    tagString = ','.join(tagArray)
    embedString = ','.join(embedArray)


    if request.method == 'POST':
        form = EditForm(request.POST, instance=product, initial={"price": price, "embedMedia": embedString, "tags": tagString})

        if form.is_valid():
            cd = form.cleaned_data
            form.save()

            # Save icon
            if cd["iconUrl"] is not None:
                #Download icon if one is specified
                product.iconUrl = cd["iconUrl"]
                product.saveIcon()

            # Delete all products embedded media instances
            e = EmbeddedMedia.objects.filter(product=product)
            for ee in e:
                ee.delete()

            # Save embedded media
            embedString = cd['embedMedia']
            # Remove possible whitespaces
            embedString = embedString.replace(" ", "")
            embedList = embedString.split(',')

            for media in embedList:
                embedEntry = EmbeddedMedia.create()
                embedEntry.url = media
                embedEntry.product = product
                embedEntry.save()

            # Delete all products tag instances # TODO
            t = Tag.objects.filter(hasTags=product)
            for tt in t:
                tt.hasTags.remove(product)

            # Save tags
            tagsString = cd['tags']
            # Remove possible whitespaces
            tagsString = tagsString.replace(" ", "")
            tagsList = tagsString.split(',')

            for tag in tagsList:
                #check if the tag is already in db, if not create it
                if Tag.objects.filter(name=tag).exists():
                    t = Tag.objects.get(name=tag)
                    t.hasTags.add(product)
                else:
                    tagEntry = Tag.create()
                    tagEntry.name = tag
                    tagEntry.save()
                    tagEntry.hasTags.add(product)

            # Create new instances in Stock Records
            f = StockRecord.objects.get(product=product)

            # TODO AWFUL BUG FIX
            if cd['price'] == 0:
                price = 0.01
            else:
                price = cd['price']

            f.price_retail = price
            f.price_excl_tax = price
            f.save()

            return HttpResponseRedirect('/panel/products')
        else:
            errors = form.errors
            form = EditForm(instance=product, initial={"price": price, "embedMedia": embedString, "tags": tagString})
            return render(request, 'panel/products/edit.html', {'form': form, 'product': product, 'errors': errors})
    else:
        form = EditForm(instance=product, initial={"price": price, "embedMedia": embedString, "tags": tagString})
        return render(request, 'panel/products/edit.html', {'form': form, 'product': product})

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