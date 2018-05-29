import json, RAKE, string
from mp3segment import mp3_length, mp3_segment_all
from pdf2txt import pdf_length, pdf2txt
import nltk
from nltk.corpus import stopwords
import gensim
from pdfwordsize import get_page_words
from stringsimilarity import get_string_similarity, get_difference, get_text_list
import collections

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
		sentence_text = sentence_text.lstrip().rstrip()
		sentence_list.append([i, int(start_time), int(end_time), sentence_text])
	return sentence_list

def strip_text(text):
	delete_words = ['"',':',';','!','@','#','$','%','^','&','0','1','2','3','4','5','6','7','8','9',
	                            '*','(',')','+','-','_','=','{','}','[',']','?',
	                            '/','<','>',',','.','|','`','~','"',"'",'\\','\n']
	text = text.replace("\n", " ")
	text = text.replace("\r", " ")

	for dw in delete_words:
		text = text.replace(dw, "")
	return text.lower()

def extract_keywords(text):
	rake = RAKE.Rake(RAKE.SmartStopList())
	return rake.run(text, maxWords=1)

def get_keywords(pdf_name, pdf_text, pdf_words):
	stopwords_set = set(stopwords.words('english'))
	keywords_list = []
	assert len(pdf_text) == len(pdf_words)

	similar_index = []
	similarities = get_string_similarity(pdf_name+"_toText.csv")
	# print(similarities)
	for i in range(len(similarities)):
		if similarities[i] > 85:
			similar_index.append(i)
	#similar_index = [2, 4, 5 ...] means slide number 2 and 3, 4 and 5, 5 and 6 ,... are similarhhh

	for i in range(len(pdf_text)):
		stripped = strip_text(pdf_text[i][1])
		pdf_text[i][1] = stripped

		keywords = stripped.split()[:4]
		nlp_words = extract_keywords(stripped)
		for w in nlp_words:
			keywords.append(w[0])

		maxfont = 0
		for w in pdf_words[i]:
			if int(w[1]) > maxfont:
				maxfont = int(w[1])
			if w[2] == True:
				keywords.append(w[0])

		for w in pdf_words[i]:
			if int(w[1]) == maxfont:
				keywords.append(w[0])

		if i>0 and i-1 in similar_index:
			words_in_prev_slide = pdf_text[i-1][1].split()
			words_in_curr_slide = pdf_text[i][1].split()
			extra_words = get_difference(words_in_prev_slide, words_in_curr_slide)
			for word in extra_words:
				keywords.append(word)
				#keywords_list.append(extract_words)

		keywords_list.append(list(set(keywords).difference(stopwords_set)))

	return keywords_list


def synchronize(rec_file, rec_format, pdf_file, json_file):
	print("Starting ...")
	json_path = json_file # path of conversion of rec_file to text script
	rec_len = mp3_length(rec_file, rec_format)
	pdf_len = pdf_length(pdf_file)
	
	sentence_list = parse_script(json_path)
	# [sid, start_time, end_time, text] - e.g. [[0, 10, 4500, "So today.."]...]

	pdf_text = pdf2txt(pdf_file)
	# [slide_no, slide_text] - e.g. [[0, "Today: Lists Tuples Context"], ...]
	pdf_words = get_page_words(pdf_file)
	# [[word, font-size, bold], ...] - e.g. [[["welcome", 80, true], ["to", 20, false], ...], ...]

	time_boundaries = []
	# [start_time, end_time] e.g. [[0, 1000], [1000, 4000]...]
	sentence_boundaries = []
	# [sentence number] e.g. [6, 15, 24, ...]

	########### main synchronization ############
	# choose keywords for each slide: keyword from NLP + keyword from first 4 words
	pdf_keywords = get_keywords(pdf_file[:-4], pdf_text, pdf_words)
	# load google word2vec
	model = gensim.models.KeyedVectors.load_word2vec_format('./../model/GoogleNews-vectors-negative300.bin', binary=True)  	
	vocab = model.vocab.keys()
	
	print("Getting boundaries ...")
	partition = 0
	total_time = sentence_list[-1][2]
	for i in range(1, len(pdf_keywords)):
		print("page: "+str(i+1))
		print("partition: "+ str(partition))
		slide = pdf_keywords[i]
		if partition == len(sentence_list):
			break

		s_set = {}
		for keyword in slide:
			for line in sentence_list[partition+1:]:
				if keyword in line[3]:
					idx = line[0]
					if idx in s_set:
						s_set[idx] += 1
					else:
						s_set[idx] = 1
					break
		s_lst = sorted(s_set.items(), key=lambda x: (-x[1], x[0]))
		print(s_lst)
		if not s_lst:
			partition = partition
			sentence_boundaries.append(partition)
		else:
			if s_lst[0][1] > 1:
				partition = s_lst[0][0]
				sentence_boundaries.append(partition)
			else:
				print("second")
				s_set = {}
				for keyword in slide:
					for line in sentence_list[partition+1:]:
						words_in_sentence = line[3].split()
						for word in words_in_sentence:
							if keyword == word:
								if line[1]<(i*total_time/len(pdf_keywords))*1.2:
									idx = line[0]
									if idx in s_set:
										s_set[idx] += 1
									else:
										s_set[idx] = 1
							elif keyword in vocab:
								if line[1]<(i*total_time/len(pdf_keywords))*1.2:
									if word in vocab:
										similarity = model.similarity(word, keyword)
										if similarity >= 0.8:
											print ("similarity:" + str(similarity))
											if idx in s_set:
												s_set[idx] += similarity
											else:
												s_set[idx] = similarity

				s_set = collections.OrderedDict(sorted(s_set.items()))
				print(s_set)
				if (len(s_set)) == 0:
				 	partition = s_lst[0][0]
				 	sentence_boundaries.append(partition)
				 	continue

				if not s_set:
					partition =partition
				else:
					max_from_slide = 0
					max_to_slide = 0
					max_count = 0
					start_slide = 0
					pre_slide = 0
					count = 0
					for key, value in s_set.items():
						if start_slide == 0:
							max_from_slide = key
							max_to_slide = key
							max_count = count
							start_slide = key
							pre_slide = key
							count = value
						elif pre_slide + 1 == key:
							pre_slide = key
							count += value
						else:
							if max_count<count:
								max_from_slide = start_slide
								max_to_slide = pre_slide
								max_count = count
							start_slide = key
							pre_slide = key
							count = value
						#print("max_slide: "+str(max_slide))
						#print("max_count: "+str(max_count))
						#print("start_slide: "+str(start_slide))
						#print("pre_slide: "+str(pre_slide))
						#print("count: "+str(count))
						#print("\n--------\n")
					partition = max_to_slide
				sentence_boundaries.append(max_from_slide)

	# # print(sentence_boundaries, len(sentence_boundaries))
	# x = 1;
	# print ("slide " + str(x) + ": " + sentence_list[0][3])
	# for i in sentence_boundaries:
	# 	x += 1
	# 	print ("slide " + str(x) + ": " + sentence_list[i][3])
	print("Making time boundaries ...")
	sentence_boundaries.append(len(sentence_list)-1)
	time_boundaries.append([0,0])
	for i in range(len(sentence_boundaries)):
		sentence_no = sentence_boundaries[i]
		prev_end_time = sentence_list[sentence_no-1][2]
		curr_start_time = sentence_list[sentence_no][1]
		time_boundaries[i][1] = prev_end_time
		time_boundaries.append([curr_start_time,0])
	time_boundaries[-1][1] = rec_len-1

	print("Making final set ...")
	final_set = []
	start_sentence = 0
	for i in range(len(sentence_boundaries)):
		end_sentence = sentence_boundaries[i]
		slide_script = ""
		highlight_set = get_highlight_set(pdf_words[i], pdf_keywords[i], sentence_list[start_sentence:end_sentence])
		for j in range(start_sentence, end_sentence):
			slide_script += " " + sentence_list[j][3][0].upper() + sentence_list[j][3][1:] + "."
		final_set.append([i+1, highlight_set, slide_script])
		start_sentence = end_sentence

	print("Cutting mp3 ...")
	mp3_segment_all(rec_file, rec_format, time_boundaries, rec_file[:-4])

	return final_set

def get_highlight_set(bold_words, keywords, sentences):
	highlight_words = []
	highlight_set = []
	for word in bold_words:
		if word[2] and len(word[0]) > 1:
			highlight_words.append(word[0])
	s_set = {}
	for word in keywords:
		s_set[word] = 0
		for line in sentences:
			if word in line:
				s_set[word] += 1
	s_lst = sorted(s_set.items(), key=lambda x: -x[1])
	count = 0
	for word in s_lst:
		if word[1] > 0:
			highlight_words.append(word[0])
		count += 1
		if count == 4 or count == len(s_lst):
			break

	stopwords_set = set(stopwords.words('english'))
	highlight_words = list(set(highlight_words).difference(stopwords_set))

	for word in highlight_words:
		script = ""
		for line in sentences:
			if word in line:
				script += '<sapn style="background-color: yellow;"> ' + line[3][0].upper() + line[3][1:] + ".</span>"
			else:
				script += " " + line[3][0].upper() + line[3][1:] + "."
		highlight_set.append([word, script])

	return highlight_set

print(synchronize("Lec01_voice.mp3", "mp3", "Lec01_note.pdf", "Lec01.json"))
# print (a[:3])


