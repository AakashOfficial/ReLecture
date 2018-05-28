#!/usr/bin/env python

"""
Converts PDF text content (though not images containing text) to plain text, html, xml or "tags".
"""
import sys
import logging
import six
import pdfminer.settings

pdfminer.settings.STRICT = False
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO, BytesIO
import re
import csv


def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0  # is for all
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    string = retstr.getvalue()
    retstr.close()
    # out = open(path[:-4]+".html", 'w')
    # out.write(string)
    return str(string)


if __name__ == '__main__':
    str = convert_pdf_to_html("Lec01_note.pdf")
    print(str)
