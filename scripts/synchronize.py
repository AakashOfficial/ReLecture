import json, RAKE, string
from mp3segment import mp3_length, mp3_segment_all
from pdf2txt import pdf_length, pdf2txt
import nltk
from nltk.corpus import stopwords
# import gensim
from pdfwordsize import get_page_words

# def pre_process_txt(text_file):

def parse_script(json_path):
	with open(json_path) as f:
		data = json.load(f)
	sentence_list = []
	for i in range(len(data)):
		start_time = data[i]['results'][0]['alternatives'][0]['timestamps'][0][1] * 1000
		end_time = data[i]['results'][0]['alternatives'][0]['timestamps'][-1][2] * 1000
		sentence_text = data[i]['results'][0]['alternatives'][0]['transcript']
		sentence_text = sentence_text.replace("%HESITATION", "")
		sentence_list.append([i, int(start_time), int(end_time), sentence_text])
	return sentence_list

def strip_text(text):
	no_punc = ""
	for c in text:
		if c not in string.punctuation:
			no_punc += c
		else:
			no_punc += " "
	final_text = ""
	words = no_punc.split()
	for w in words:
		final_text += w + " "
	return final_text[:-1].lower()

def extract_keywords(text):
	rake = RAKE.Rake(RAKE.SmartStopList())
	return rake.run(text, maxWords=1)

def get_keywords(pdf_text, pdf_words):
	stopwords_set = set(stopwords.words('english'))
	keywords_list = []
	assert len(pdf_text) == len(pdf_words)
	for i in range(len(pdf_text)):
		stripped = strip_text(pdf_text[i][1])
		pdf_text[i][1] = stripped

		keywords = stripped.split()[:4]
		nlp_words = extract_keywords(stripped)
		for w in nlp_words:
			keywords.append(w[0].lower())

		maxfont = 0
		for w in pdf_words[i]:
			if int(w[1]) > maxfont:
				maxfont = int(w[1])
			if w[2] == True:
				keywords.append(w[0])

		for w in pdf_words[i]:
			if int(w[1]) == maxfont:
				keywords.append(w[0])

		keywords_list.append(list(set(keywords).difference(stopwords_set)))
	return keywords_list


def synchronize(rec_file, rec_format, pdf_file):
	json_path = "Lec01.json" # path of conversion of rec_file to text script
	
	sentence_list = parse_script(json_path)
	# [sid, start_time, end_time, text] - e.g. [[0, 10, 4500, "So today.."]...]

	pdf_text = pdf2txt(pdf_file)
	# [slide_no, slide_text] - e.g. [[0, "Today: Lists Tuples Context"], ...]
	pdf_words = get_page_words(pdf_file)
	# [[word, font-size, bold], ...] - e.g. [[["welcome", 80, true], ["to", 20, false], ...], ...]
	print (len(pdf_text))
	print (len(pdf_words))

	time_boundaries = []
	sentence_boundaries = []
	# [start_time, end_time] e.g. [[0, 1000], [1000, 4000]...]

	########### main synchronization ############
	# choose keywords for each slide: keyword from NLP + keyword from first 4 words
	pdf_keywords = get_keywords(pdf_text, pdf_words)

	model = gensim.models.KeyedVectors.load_word2vec_format('./../model/GoogleNews-vectors-negative300.bin', binary=True)  	
	vocab = model.vocab.keys()

	partition = 0
	for i in range(1, len(pdf_keywords)):
		slide = pdf_keywords[i]
		if i == len(pdf_keywords)-1 or partition == len(sentence_list):
			break
		s_set = {}
		for line in sentence_list[partition+1:]:
			idx = line[0]
			s_set[idx] = 0.0
			words_in_sentence = line[3].split()
			for keyword in slide:
				# if keyword in line[3]:
				# 	s_set[idx] += 1
				for word in words_in_sentence:
					if keyword == word:
						s_set[idx] += 1
					elif keyword in vocab:
						if word in vocab:
							similarity = model.similarity(word, keyword)
							if similarity >= 0.8:
								s_set[idx] += similarity/4
			# #print("\n")
			# if len(words_in_sentence) != 0:
			# 	s_set[idx] /= len(words_in_sentence)

				# if keyword in line[3]:
				# 	idx = line[0]
				# 	if idx in s_set:
				# 		s_set[idx] += 1
				# 	else:
				# 		s_set[idx] = 1
		#print (slide[0], " ", slide[2])
		#print (s_set)
		if not s_set:
			partition = partition
		else:
			partition = max(s_set, key=s_set.get)
		sentence_boundaries.append(partition)

	# # print(sentence_boundaries, len(sentence_boundaries))
	x = 1;
	print ("slide " + str(x) + ": " + sentence_list[0][3])
	for i in sentence_boundaries:
		x += 1
		print ("slide " + str(x) + ": " + sentence_list[i][3])


	#############################################

	########### demo synchronization ############	
	# rec_len = mp3_length(rec_file, rec_format)
	# pdf_len = pdf_length(pdf_file)
	# seg_len = rec_len / pdf_len
	# for i in range(pdf_len):
	# 	boundaries.append([i*seg_len, (i+1)*seg_len])
	# #############################################

	# mp3_segment_all(rec_file, rec_format, boundaries, rec_file[:-4])

synchronize("voice.mp3", "mp3", "Lec01_note.pdf")
# print (a[:3])


