from rest_polymorphic.serializers import PolymorphicSerializer


class PartyPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Person: PersonSerializer,
        Attorney: AttorneySerializer,
        Company: CompanySerializer,
    }
