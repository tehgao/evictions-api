import casepdfparser.parser as parser
import casepdfparser.reader as reader
from cases.models import Address, Party, Attorney, Case, Event
from datetime import datetime, date
import pytz


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


def load_pages(pages):
    all_cases = parser.process_pages(reader.read_pages_from_file(pages))

    load_list(all_cases)


def load_pdf(pdf_file_name):
    load_pages(reader.read_pages_from_filename(pdf_file_name))


def main():
    load_pdf('junk/evictions.pdf')


if __name__ == "__main__":
    main()
