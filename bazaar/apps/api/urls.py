from django.conf.urls import patterns, url
from django.conf.urls import url, patterns, include
from rest_framework import viewsets
from django.contrib import admin
from rest_framework import viewsets, routers
from django.contrib.auth.models import User, Group
from oscar.core.loading import get_class, get_model
from apps.api import views


class UserViewSet(viewsets.ModelViewSet):
    model = User

class GroupViewSet(viewsets.ModelViewSet):
    model = Group


router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'subjects',  views.SubjectList)
router.register(r'producttypes', views.ProductTypeList)
router.register(r'productformats', views.ProductFormatList)

urlpatterns = patterns('',
    # ex: /
    #url (r'^users/$', views.UserViewSet.as_view()),
    url(r'^', include(router.urls)),
    url(r'^cms/', views.CMSView.as_view()),
    url(r'^lms/library/$', views.PurchasedProductsView.as_view()),
    url(r'^lms/content/(?P<uuid>.*)/$', views.ProductMetadataView.as_view()),

    #url(r'^cms/', views.CMSView.as_view()),

)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)
