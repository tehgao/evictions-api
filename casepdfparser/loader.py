import casepdfparser.parser as parser


def load_pdf(pdf_file_name):
    cases_map = parser.process_pdf_file(pdf_file_name)
