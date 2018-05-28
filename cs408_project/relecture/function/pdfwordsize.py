from .pdfmine import convert_pdf_to_html

from bs4 import BeautifulSoup


def get_page_words(pdf_file):
    delete_words = ['"', ':', ';', '!', '@', '#', '$', '%', '^', '&', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '*', '(', ')', '+', '-', '_', '=', '{', '}', '[', ']', '?',
                    '/', '<', '>', ',', '.', '|', '`', '~', '"', "'", '\\']

    contents = convert_pdf_to_html(pdf_file)
    # with open(pdf_file) as f:
    #     for line in f.readlines():
    #         contents += line

    contents = contents.replace("\n", "")
    contents = contents.replace("\r", "")
    # contents = contents.rstrip()
    pages = contents.split("<a name=")[1:]
    all_pages = []
    for i in range(len(pages)):
        page_html = BeautifulSoup(pages[i], "html.parser")
        divs = page_html.find_all('div')
        spans = []
        for div in divs:
            spans += div.find_all('span')
        word_list = []
        for span in spans:
            text = span.text.lower()
            text = text.replace("\\n", " ")
            text = text.replace("\\r", " ")
            fin = False
            while not fin:
                if text.find("\\xe") >= 0:
                    idx = text.find("\\xe")
                    text = text.replace(text[idx:idx + 12], "")
                else:
                    fin = True
            for dw in delete_words:
                text = text.replace(dw, " ")
            words = text.split()
            style = span['style']
            bold = ",Bold" in style
            size = style[style.find("font-size:") + 10:-2]
            for word in words:
                if len(word) == 1:
                    continue
                if word != "":
                    word_list.append([word, size, bold])

        all_pages.append(word_list)

    return all_pages

# print (get_page_words("Lec01_note.pdf")[3])
