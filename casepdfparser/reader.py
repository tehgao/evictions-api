from pdfmajor.parser.PDFPage import PDFPage
from pdfmajor.interpreter import PageInterpreter, PDFInterpreter


def read_pages_from_file(pdf_file_obj):
    pdf_pages = []
    font_cache = {}
    pages = PDFPage.get_pages(pdf_file_obj)
    for page_num, page in enumerate(pages):
        pdf_pages.append(PageInterpreter(page, page_num, font_cache))

    return pdf_pages


def read_pages_from_filename(pdf_file_name):
    return PDFInterpreter(pdf_file_name)
