import PyPDF2
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def pdf2txt(pdf, output_json, output_csv):
	path = os.path.join(BASE_DIR, 'convert_pdf')

	#read pdf
	pdfFileObj = open(pdf,'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	print ("slide number: {}".format(pdfReader.numPages))
	slide_by_number = {}
	for i in range(pdfReader.numPages):
		pageObj = pdfReader.getPage(i)
		slide_by_number[i] = pageObj.extractText()

	#save as json file
	json_val=json.dumps(slide_by_number)
	f = open(os.path.join(path, output_json), "w")
	f.write(json_val)
	f.close()

	#save as csv file
	w = csv.writer(open(os.path.join(path, output_csv), "w"))
	for key, val in slide_by_number.items():
		w.writerow([key, val])

	return True

#example : pdf2txt('UML.pdf', '1.json', '2.csv')
# pdf2txt('UML.pdf', '1.json', '2.csv')