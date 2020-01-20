import casepdfparser.parser as parser
import casepdfparser.reader as reader

from cases.utils import ListLoader as loader


def load_pages(pages):
    all_cases = parser.process_pages(reader.read_pages_from_file(pages))

    loader.load_list(all_cases)


def load_pdf(pdf_file_name):
    load_pages(reader.read_pages_from_filename(pdf_file_name))


def main():
    load_pdf('junk/evictions.pdf')


if __name__ == "__main__":
    main()
