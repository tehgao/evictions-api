from django.test import TestCase, Client
import os
from django.conf import settings
from django.contrib.auth.models import User
from cases.models import Case

from evictions_api.views import PdfUploadView


class ViewTest(TestCase):

    def test_pdf_upload(self):
        user = User(username='test', password='test')
        user.save()

        pdf_location = os.path.join(
            settings.BASE_DIR, 'test_data/evictions.pdf')
        with open(pdf_location, 'rb') as pdf:
            client = Client()
            client.force_login(user=user)
            payload = {'file': pdf}
            response = client.post(
                '/api/upload/evictions.pdf', payload, format='multipart')

            self.assertEqual(response.status_code, 201)
