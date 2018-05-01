
def synchronize(rec_file, rec_format, slides):
	rec_len = length_mp3(rec_file, rec_format)
	slide_len = 10 #get total number of slides

	seg_len = rec_len / slide_len
	for i in range(slide_len):
		seg_name = rec_file[:-4] + "_" + str(i) + ".mp3"
		segment_mp3(rec_file, rec_format, segment_name, i*seg_len, (i+1)*seg_len)