from django.test import TestCase
import casepdfparser.loader as loader
import os
from django.conf import settings
from cases.models import Case
# Create your tests here.


class LoaderTest(TestCase):

    def test_loader(self):
        test_list = [{'code': '2019 CVG 020274',
                      'defendants': [{'address': ['3788 E 52ND STREET',
                                                  'CLEVELAND',
                                                  'OH',
                                                  '44105'],
                                      'name': 'COONA, AUTUMN'}],
                      'events': [{'event_type': 'ATTY FIRST CAUSE HEARING',
                                  'date': '01/21/2020',
                                  'is_pro_se': False,
                                  'time': '09:00'}],
                      'file_date': '12/30/2019',
                      'plaintiffs': [{'address': ['5555 CLEVELAND AVE',
                                                  'GW1W42',
                                                  'COLUMBUS',
                                                  'OH',
                                                  '43231'],
                                      'attorney': 'CASTERLINE ESQ, CHRISTOPHER S',
                                      'name': 'THE HUNTINGTON NATIONAL BANK'}]}]

        loader.load_list(test_list)
        self.assertEqual(len(Case.objects.all()), 1)

    def test_loader_pdf(self):
        pdf_location = os.path.join(settings.BASE_DIR, 'junk/evictions.pdf')
        loader.load_pdf(pdf_location)

        self.assertEqual(len(Case.objects.all()), 94)
