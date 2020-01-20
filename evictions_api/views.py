from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from casepdfparser import loader
from cases.models import Case, Party
from cases.utils import FakeLoader
from evictions_api.serializers import CaseSerializer, PartySerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


class PdfUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, filename, format=None):
        file_obj = request.FILES['file']
        loader.load_pages(file_obj)

        return Response(status=201)


class GenerateTestDataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        fakeloader = FakeLoader()

        generated = fakeloader.generate_mock_cases(
            int(request.POST.get('num')))

        return Response(status=201, data=[CaseSerializer(case).data for case in generated])
