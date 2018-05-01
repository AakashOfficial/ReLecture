from pydub import AudioSegment

def segment_mp3(input_file, input_format, output_file, start_time, end_time):
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

	# writing mp3 files is a one liner
	segment.export(output_file, format="mp3")

	return True