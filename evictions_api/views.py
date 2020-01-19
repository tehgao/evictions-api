from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import BasePermission, IsAuthenticated
from cases.models import Party, Case
from casepdfparser import loader, reader
from evictions_api.serializers import CaseSerializer, PartySerializer
from django.conf import settings

import tempfile


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
