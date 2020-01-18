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

from cases.models import *


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Address
        fields = '__all__'


class AttorneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attorney
        fields = ('name', )


class PartySerializer(serializers.ModelSerializer):
    attorney_set = AttorneySerializer(many=True)
    address = AddressSerializer

    class Meta:
        model = Party
        fields = ('name', 'address', 'attorney_set')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):
    plaintiffs = PartySerializer(many=True)
    defendants = PartySerializer(many=True)
    additional_parties = PartySerializer(many=True)

    events = EventSerializer

    class Meta:
        model = Case
        fields = '__all__'
        depth = 4


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


router = routers.DefaultRouter()
router.register(r'cases', CaseViewSet)
router.register(r'parties', PartyViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
