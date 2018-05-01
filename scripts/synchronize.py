from mp3segment import mp3_length, mp3_segment_all
from pdf2txt import pdf_length

def synchronize(rec_file, rec_format, pdf_file):
	rec_len = mp3_length(rec_file, rec_format)
	pdf_len = pdf_length(pdf_file)
	seg_len = rec_len / pdf_len
	boundaries = []
	for i in range(pdf_len):
		boundaries.append([i*seg_len, (i+1)*seg_len])
	mp3_segment_all(rec_file, rec_format, boundaries, rec_file[:-4])

synchronize("voice.mp3", "mp3", "UML.pdf")