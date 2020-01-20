"""evictions_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework import serializers, viewsets, routers

from cases.models import Address, Party, Case, Attorney, Event
from evictions_api.views import CaseViewSet, PartyViewSet, PdfUploadView, GenerateTestDataView
from evictions_api.serializers import AddressSerializer, AttorneySerializer, PartySerializer, EventSerializer, CaseSerializer


router = routers.DefaultRouter()
router.register(r'cases', CaseViewSet)
router.register(r'parties', PartyViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/upload/(?P<filename>[^/]+)$', PdfUploadView.as_view()),
    url(r'^api/generate',
        GenerateTestDataView.as_view()),
    path('admin/', admin.site.urls),
]
