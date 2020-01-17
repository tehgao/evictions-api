from pdfmajor.interpreter import PDFInterpreter, LTTextBlock
import re

pages = []


def partitioned_list(part_list, partitions):
    return [part_list[i:j]
            for i, j in zip([0] + partitions, partitions + [None])]


def get_addresses(section_list):
    split_points = [min(idx + 1, len(section_list)) for (idx, str) in enumerate(section_list)
                    if re.search(r'([\w ]+), ([A-Z]{2}) ([0-9]{5}(-[0-9]{4})?)', str)]
    return partitioned_list(section_list, split_points)[:-1]


for page in PDFInterpreter("../junk/evictions.pdf"):
    page_lines = []
    for item in page:
        if isinstance(item, LTTextBlock):
            for text in item:
                item_text = ''.join(
                    c.get_text() for c in item)
                if not re.search('^Attorney\\(s\\)$', item_text):
                    page_lines.append(item_text)
    end_of_header = [idx for (idx, line) in enumerate(page_lines)
                     if re.search('Case Status: All', line)]

    pages.append(page_lines[end_of_header[0] + 1:])

all_lines = [line for page in pages for line in page][:-1]

start_indices = [idx for (idx, line) in enumerate(all_lines)
                 if re.search('^20[0-9]{2} CVG [0-9]{6}', line)]

cases = partitioned_list(all_lines, start_indices)
# print(cases)

# print('\n'.join(['Case {}: {}'.format(idx, case)
#                  for (idx, case) in enumerate(cases)]))

cases = cases[1:]
for case in cases:
    case_dict = {}
    split_indices = list(map(case.index, ['PLAINTIFF(s):', 'DEFENDANT(s):',
                                          'Additional Party(s):', 'File Date:', 'Time']))
    sections = partitioned_list(case, split_indices)
    case_dict['code'] = re.match('^20[0-9]{2} CVG [0-9]{6}', case[0]).group(0)

    # plaintiffs
    plaintiffs = []
    for plaintiff in get_addresses(sections[1][1:]):
        plaintiff_name = plaintiff.pop(0)
        finds = [(idx, line) for (idx, line) in enumerate(
            plaintiff) if re.search(r'[\w ]+ ESQ, [\w ]+', line)]
        if len(finds) > 0:
            plaintiff_addr = plaintiff
            plaintiff_addr.pop(finds[0][0])
            plaintiffs.append(
                {'name': plaintiff_name, 'address': plaintiff_addr, 'attorney': finds[0][1]})
        else:
            plaintiffs.append({'name': plaintiff_name, 'address': plaintiff})

    case_dict['plaintiffs'] = plaintiffs

    # defendants
    case_dict['defendants'] = get_addresses(sections[2][1:])

    print(case_dict)
