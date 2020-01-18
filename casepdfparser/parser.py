from pdfmajor.interpreter import PDFInterpreter, LTTextBlock
import re
import pprint

pages = []


def partitioned_list(part_list, partitions):
    return [part_list[i:j]
            for i, j in zip([0] + partitions, partitions + [None])]


def get_addresses(section_list):
    split_points = [min(idx + 1, len(section_list)) for (idx, str) in enumerate(section_list)
                    if re.search(r'([\w ]+), ([A-Z]{2}) ([0-9]{5}(-[0-9]{4})?)', str)]
    return partitioned_list(section_list, split_points)[:-1]


def process_parties(plaintiff_list):
    plaintiffs = []
    for p in plaintiff_list:
        plaintiff = list(p)
        plaintiff_name = plaintiff.pop(0)
        finds = [(idx, line) for (idx, line) in enumerate(
            plaintiff) if re.search(r'[\w ]+ ESQ, [\w ]+', line)]
        if len(finds) > 0:
            plaintiff_addr = plaintiff
            plaintiff_addr.pop(finds[0][0])
            plaintiffs.append(
                {'name': plaintiff_name, 'address': plaintiff_addr, 'attorney': finds[0][1]})
        else:
            plaintiffs.append(
                {'name': plaintiff_name, 'address': plaintiff})

    return plaintiffs


def process_defendants(defendant_list):
    defendants = []
    for d in defendant_list:
        defendant = list(d)
        defendant_name = defendant.pop(0)
        defendants.append({'name': defendant_name, 'address': defendant})

    return defendants


def process_events(event_list):
    if (len(event_list) - 1) % 3 != 0:
        raise ValueError

    events = []

    every_third = [
        3 * x + 1 for x in range(int((len(event_list) - 1) / 3))]
    event_triples = [(event_list[i:j]) for (i, j) in
                     zip(every_third, every_third[1:] + [None])]
    for (case_type, date, time) in event_triples:
        event = {
            "case_type": case_type,
            "date": date,
            "time": time,
            "is_pro_se": bool(re.search('PRO SE', case_type))
        }

        events.append(event)

    return events


def process_cases(cases_list):
    processed_cases = []
    cases = cases_list[1:]
    for case in cases:
        case_dict = {}
        split_indices = list(map(case.index, ['PLAINTIFF(s):', 'DEFENDANT(s):',
                                              'Additional Party(s):', 'File Date:', 'Time']))
        sections = partitioned_list(case, split_indices)
        case_dict['code'] = re.match(
            '^20[0-9]{2} CVG [0-9]{6}', case[0]).group(0)

        case_dict['plaintiffs'] = process_parties(
            get_addresses(sections[1][1:]))

        case_dict['defendants'] = process_parties(
            get_addresses(sections[2][1:]))

        case_dict['file_date'] = [elt for elt in sections[4]
                                  if re.match(r'\d{2}\/\d{2}\/\d{4}', elt)][0]

        case_dict['events'] = process_events(sections[5])
        processed_cases.append(case_dict)

    return processed_cases


def process_all_lines(all_lines):
    start_indices = [idx for (idx, line) in enumerate(all_lines)
                     if re.search('^20[0-9]{2} CVG [0-9]{6}', line)]

    return process_cases(partitioned_list(all_lines, start_indices))


def process_pdf_file(file_name):
    for page in PDFInterpreter(file_name):
        page_lines = []
        for item in page:
            if isinstance(item, LTTextBlock):
                item_text = ''.join(
                    c.get_text() for c in item)
                if not re.search('^Attorney\\(s\\)$', item_text):
                    page_lines.append(item_text)
        end_of_header = [idx for (idx, line) in enumerate(page_lines)
                         if re.search('Case Status: All', line)]

        pages.append(page_lines[end_of_header[0] + 1:])

    return process_all_lines([line for page in pages for line in page][:-1])


def main():
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(process_pdf_file('../junk/evictions.pdf'))


if __name__ == "__main__":
    main()
