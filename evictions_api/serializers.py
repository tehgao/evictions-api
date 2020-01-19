from rest_framework import serializers
from cases.models import Address, Party, Case, Attorney, Event


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Address
        fields = ('street_address', 'street_address_2', 'city', 'state', 'zip')


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
        depth = 3


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):
    plaintiffs = PartySerializer(many=True)
    defendants = PartySerializer(many=True)
    additional_parties = PartySerializer(many=True)

    event_set = EventSerializer(many=True)

    class Meta:
        model = Case
        fields = '__all__'
        depth = 3
