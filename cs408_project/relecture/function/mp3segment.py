from pydub import AudioSegment
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def mp3_length(input_file, input_format):
	if (input_format == "mp3"):
		recording = AudioSegment.from_mp3(input_file)
	elif (input_format == "wav"):
		recording = AudioSegment.from_wav(input_file)
	elif (input_format == "ogg"):
		recording = AudioSegment.from_ogg(input_file)
	else:
		return -1

	return len(recording)


def mp3_segment(input_file, input_format, output_file, start_time, end_time):
	if (input_format == "mp3"):
		recording = AudioSegment.from_mp3(input_file)
	elif (input_format == "wav"):
		recording = AudioSegment.from_wav(input_file)
	elif (input_format == "ogg"):
		recording = AudioSegment.from_ogg(input_file)
	else:
		return False

	# len() and slicing are in milliseconds
	if (len(recording) < end_time):
		return False

	segment = recording[start_time:end_time]
	segment.export(output_file, format="mp3")

	return True

def mp3_segment_all(input_file, input_format, boundaries, output_file):
	if (input_format == "mp3"):
		recording = AudioSegment.from_mp3(input_file)
	elif (input_format == "wav"):
		recording = AudioSegment.from_wav(input_file)
	elif (input_format == "ogg"):
		recording = AudioSegment.from_ogg(input_file)
	else:
		return False

	for i in range(1,len(boundaries)+1):
		start, end = boundaries[i]
		recording[start:end].export(BASE_DIR+"/slice_file/"+ output_file +"_"+str(i)+".mp3", format="mp3")

	return True

mp3_segment('/Users/haseongkwon/Downloads/test2.mp3','mp3','/Users/haseongkwon/Downloads/convert.mp3',0,5000)
