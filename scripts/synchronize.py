from mp3segment import mp3_length, mp3_segment_all
from pdf2txt import pdf_length
import json
from pprint import pprint

# def pre_process_txt(text_file):

def parse_script(json_path):
	with open(json_path) as f:
		data = json.load(f)
	sentence_list = []
	for i in range(len(data)):
		start_time = data[i]['results'][0]['alternatives'][0]['timestamps'][0][1] * 1000
		end_time = data[i]['results'][0]['alternatives'][0]['timestamps'][-1][2] * 1000
		sentence_text = data[i]['results'][0]['alternatives'][0]['transcript']
		sentence_list.append([i, int(start_time), int(end_time), sentence_text])
	return sentence_list


def synchronize(rec_file, rec_format, pdf_file):
	json_path = "Lec01.json" # path of conversion of rec_file to text script
	
	sentence_list = parse_script(json_path)
	# [sid, start_time, end_time, text] - e.g. [[0, 10, 4500, "So today.."]...]

	pdf_text = pdf2txt(pdf_file)
	# [slide_no, slide_text] - e.g. [[0, "Today: Lists Tuples Context"]...]

	boundaries = []
	# [start_time, end_time] e.g. [[0, 1000], [1000, 4000]...]

	########### main synchronization ############
	# choose keywords for each slide


	#############################################

	########### demo synchronization ############	
	rec_len = mp3_length(rec_file, rec_format)
	pdf_len = pdf_length(pdf_file)
	seg_len = rec_len / pdf_len
	for i in range(pdf_len):
		boundaries.append([i*seg_len, (i+1)*seg_len])
	#############################################

	mp3_segment_all(rec_file, rec_format, boundaries, rec_file[:-4])

# synchronize("voice.mp3", "mp3", "UML.pdf")
# a = parse_script("test_json.json")
# for i in range (3):
# 	print (a[i])