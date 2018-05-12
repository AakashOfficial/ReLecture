import PyPDF2
import json
import csv


def pdf2txt(pdf):
    # read pdf
    pdfFileObj = open(pdf, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    print("slide number: {}".format(pdfReader.numPages))
  
    output = []
    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        text = pageObj.extractText()
        text = text.rstrip().replace("\n", " ")
        output.append([i, text])

    # save as json file
    # json_val = json.dumps(slide_by_number)
    # f = open(output_json, "w")
    # f.write(json_val)
    # f.close()

    # save as csv file

    # save as list
    #w = csv.writer(open(output_csv, "w"))
    return output


def pdf_length(pdf):
    reader = PyPDF2.PdfFileReader(open(pdf, 'rb'))
    return reader.getNumPages()

# print(pdf2txt("Lec01_note.pdf"))