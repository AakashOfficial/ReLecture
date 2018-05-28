import PyPDF2
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# example : pdf2txt('UML.pdf', '1.json', '2.csv')
# pdf2txt('UML.pdf', '1.json', '2.csv')

def pdf2txt(pdf):
    path = os.path.join(os.path.join(BASE_DIR, 'static'), 'convert_pdf')

    # read pdf
    pdfFileObj = open(pdf, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # print("slide number: {}".format(pdfReader.numPages))

    output = []
    count = 0
    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        text = pageObj.extractText()
        text = text.rstrip().replace("\n", " ")
        output.append([count, text])
        count += 1
        # save as json file
        # json_val = json.dumps(slide_by_number)
        # f = open(output_json, "w")
        # f.write(json_val)
        # f.close()

        # save as csv file
        w = csv.writer(open(os.path.join(path, 'pdf_text.csv'), "w"))
    for val in output:
        w.writerow([val[0], '"' + val[1] + '"'])

    return output


# save as list
# w = csv.writer(open(output_csv, "w"))


def get_contents(pdf):
    xx = pdfrw.PdfReader(pdf)
    print(len(str(xx.pages[0]['/Parent'])))
    print(len(str(xx.pages[0]['/Parent']['/Kids'][0])))
