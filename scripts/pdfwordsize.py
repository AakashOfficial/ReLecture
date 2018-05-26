from pdfmine import convert_pdf_to_html

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def get_page_words(pdf_file):

	delete_words = ['"',':',';','!','@','#','$','%','^','&',
	                            '*','(',')','+','-','_','=','{','}','[',']','?',
	                            '/','<','>',',','.','|','`','~','"',"'",'\\','\n']

	contents = convert_pdf_to_html(pdf_file)
	# with open(pdf_file) as f:
	#     for line in f.readlines():
	#         contents += line

	# contents = contents.replace("\n", "")
	# contents = contents.replace("\r", "")
	contents = contents.rstrip()
	pages = contents.split("<a name=")[1:]
	all_pages = []
	for page in pages:
		page_html = BeautifulSoup(page, "html.parser")
		divs = page_html.find_all('div')
		spans = []
		for div in divs:
			spans += div.find_all('span')
		word_list = []
		for span in spans:
			text = span.text.lower()
			for dw in delete_words:
				text.replace(dw, "")
			words = text.split()
			style = span['style']
			bold = ",Bold" in style
			size = style[style.find("font-size:")+10:-2]
			for word in words:
				if "\\" in word:
					idx = word.find("\\")
					word = word.replace(word[idx:idx+15], "")
				if word != "":
					word_list.append([word, size, bold])
		all_pages.append(word_list)

	return all_pages

print (get_page_words("Lec01_note.pdf")[3])