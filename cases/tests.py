from django.test import TestCase
from cases.models import Address, Party, Attorney, Case
from cases.utils import FakeLoader


class TestFakeLoader(TestCase):

    def test_address_fake(self):
        fakeloader = FakeLoader()
        fakeloader.generate_mock_address()
        self.assertIsNotNone(Address.objects.all())

    def test_parties_fake(self):
        fakeloader = FakeLoader()
        fakeloader.generate_mock_parties(amount=10)
        self.assertEqual(len(Party.objects.all()), 10)
        for party in Party.objects.all():
            self.assertIsNotNone(party.name)
            self.assertIsNotNone(party.address)

    def test_cases_fake(self):
        fakeloader = FakeLoader()
        fakeloader.generate_mock_cases(12)
        self.assertEqual(len(Case.objects.all()), 12)
        for case in Case.objects.all():
            print(case)
