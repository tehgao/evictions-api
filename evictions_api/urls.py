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
from rest_polymorphic.serializers import PolymorphicSerializer

from cases.models import *


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Address
        fields = '__all__'


class AttorneySerializer(serializers.ModelSerializer):
    address = AddressSerializer

    class Meta:
        model = Attorney
        fields = ('first_name', 'middle_initial', 'last_name')


class PartySerializer(serializers.ModelSerializer):
    attorney_set = AttorneySerializer(many=True)
    address = AddressSerializer

    class Meta:
        model = Party
        fields = ('address', 'attorney_set')


class PersonSerializer(serializers.ModelSerializer):
    address = AddressSerializer
    attorney_set = AttorneySerializer(many=True)

    class Meta:
        model = Person
        fields = ('first_name', 'middle_initial',
                  'last_name', 'address', 'attorney_set')


class CompanySerializer(serializers.ModelSerializer):
    address = AddressSerializer
    attorney_set = AttorneySerializer(many=True)

    class Meta:
        model = Company
        fields = ('name', 'address', 'attorney_set')


class PartyPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Party: PartySerializer,
        Person: PersonSerializer,
        Attorney: PersonSerializer,
        Company: CompanySerializer,
    }


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):
    plaintiffs = PartyPolymorphicSerializer(many=True)
    defendants = PartyPolymorphicSerializer(many=True)
    additional_parties = PartyPolymorphicSerializer(many=True)

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
    serializer_class = PartyPolymorphicSerializer


router = routers.DefaultRouter()
router.register(r'cases', CaseViewSet)
router.register(r'parties', PartyViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
