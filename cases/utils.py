import math
import random
from datetime import date, datetime

import pytz
from faker import Faker
from django.utils.timezone import make_aware

from cases.models import Address, Attorney, Case, Event, Party


class ListLoader:

    def load_list(raw_list):
        for case in raw_list:
            plaintiffs = []
            for plaintiff in case.get('plaintiffs'):
                address_raw = plaintiff.get('address')
                address = None
                if len(address_raw) == 5:
                    address = Address(street_address=address_raw[0],
                                      street_address_2=address_raw[1],
                                      city=address_raw[2],
                                      state=address_raw[3],
                                      zip=address_raw[4])
                else:
                    address = Address(street_address=address_raw[0],
                                      city=address_raw[1],
                                      state=address_raw[2],
                                      zip=address_raw[3])
                address.save()
                plaintiff_obj = Party(name=plaintiff.get(
                    'name'), address=address)
                plaintiff_obj.save()
                if plaintiff.get('attorney'):
                    attorney = Attorney(name=plaintiff.get(
                        'attorney'), associated_party_id=plaintiff_obj.id)
                    attorney.save()
                plaintiffs.append(plaintiff_obj)

            defendants = []
            for defendant in case.get('defendants'):
                address_raw = defendant.get('address')
                address = None
                if len(address_raw) == 5:
                    address = Address(street_address=address_raw[0],
                                      street_address_2=address_raw[1],
                                      city=address_raw[2],
                                      state=address_raw[3],
                                      zip=address_raw[4])
                else:
                    address = Address(street_address=address_raw[0],
                                      city=address_raw[1],
                                      state=address_raw[2],
                                      zip=address_raw[3])
                address.save()
                defendant_obj = Party(name=defendant.get(
                    'name'), address=address)
                defendant_obj.save()
                if defendant.get('attorney'):
                    attorney = Attorney(name=defendant.get(
                        'attorney'), associated_party_id=defendant_obj.id)
                    attorney.save()
                defendants.append(defendant_obj)

            code = case.get('code')

            file_date = datetime.strptime(case.get('file_date'), '%m/%d/%Y')

            case_obj = Case(case_number=code, file_date=file_date)
            case_obj.save()

            case_obj.plaintiffs.set(plaintiffs)
            case_obj.defendants.set(defendants)

            for event in case.get('events'):
                event_obj = Event.objects.create_event(event_type=event.get('event_type'),
                                                       date=event.get('date'),
                                                       time=event.get('time'),
                                                       is_pro_se=event.get(
                    'is_pro_se'),
                    assoc_case_id=case_obj.id)
                event_obj.save()


class FakeLoader:

    def generate_mock_address(self, with_secondary=False):
        faker = Faker()
        if with_secondary:
            address = Address(street_address=faker.street_address(),
                              street_address_2=faker.secondary_address(),
                              city=faker.city(),
                              state=faker.state_abbr(),
                              zip=faker.zipcode())
        else:
            address = Address(street_address=faker.street_address(),
                              city=faker.city(),
                              state=faker.state_abbr(),
                              zip=faker.zipcode())
        address.save()
        return address

    def generate_mock_parties(self, amount, attorneys=False):
        parties = []
        for i in range(amount):
            faker = Faker()
            party = Party(name=faker.name(),
                          address=self.generate_mock_address())
            party.save()

            if attorneys:
                attorney = Attorney(name=faker.name() + " Esq.",
                                    associated_party_id=party.id)
                attorney.save()

            parties.append(party)

        return parties

    def generate_mock_cases(self, amount):
        faker = Faker()
        mock_plaintiffs = self.generate_mock_parties(
            int(math.ceil(amount / 4)))

        cases = []
        for i in range(amount):
            year = str(date.today().year)
            num = str(random.randint(100000, 999999))
            case_number = year + " CVG " + num
            case = Case(case_number=case_number,
                        file_date=faker.date_this_month(after_today=False))
            case.save()

            case.plaintiffs.set([random.choice(mock_plaintiffs)])
            case.defendants.set(self.generate_mock_parties(1))

            generate_fc = random.choice([True, False])
            generate_sc = generate_fc and random.choice([True, False])

            if(generate_fc):
                fc = Event(event_type='FC',
                           is_pro_se=random.choice([True, False]),
                           date_time=make_aware(
                               faker.date_time_between_dates(case.file_date,
                                                             date.today())
                           ),
                           assoc_case=case)
                fc.save()
            if(generate_sc):
                sc = Event(event_type='SC',
                           is_pro_se=random.choice([True, False]),
                           date_time=make_aware(
                               faker.date_time_between_dates(case.file_date,
                                                             date.today())
                           ),
                           assoc_case=case)
                sc.save()

            cases.append(case)

        return cases
