# importing libraries 
import speech_recognition as sr 
import os
import os.path
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()


#to write the processed text to output text files
#remove if only printing the outputs to the console
def wrie2file(text, output_dir, ref_name):

	#create a blank output text file for each processed aud piece
	text_file = ref_name

	#create an output text dir
	if not os.path.isdir(output_dir+"/output_texts"):
		os.mkdir(output_dir+"/output_texts")

	#open the file in write mode
	f = open(output_dir+"/output_texts/"+text_file+".txt", "w")
	f.write(text+"\n")
	f.close()



#main func
def main(aud_file):

	#src file location
	src_loc = "../src/"

	#output dir declaration and creation
	output_dir = "outputs"
	#check if the outputs dir is present
	output_dir_loc = "../"+output_dir
	if not os.path.isdir(output_dir_loc):
		os.mkdir(output_dir_loc)

	#open the audio using pydub
	sound = AudioSegment.from_wav(aud_file)

	#break the audio into pieces using silence as a delimiter
	pieces = split_on_silence(sound, min_silence_len = 500, silence_thresh = sound.dBFS-14, keep_silence=500)

	#store the broken audio into a new folder in the outputs directory
	processed_aud_fp = "processed_aud"
	if not os.path.isdir(output_dir_loc+"/"+processed_aud_fp):
		os.mkdir(output_dir_loc+"/"+processed_aud_fp)

	#sequentially iterate over the processed audio
	for i, piece in enumerate(pieces, start=1):
		#store the processed aud for manual verfication
		piece_fp = os.path.join(output_dir_loc+"/"+processed_aud_fp, f"piece{i}.wav")
		piece.export(piece_fp, format="wav")

		#try to process the broken aud piece
		with sr.AudioFile(piece_fp) as source:
			audio_listened = r.record(source)
			# try converting it to text
			try:
				text = r.recognize_google(audio_listened)
			except sr.UnknownValueError as e:
				print("\nError while converting the audio file to text:", str(e))
			else:
				text = f"{text.capitalize()}. "
				#uncomment the line below to print the processed text.
				# print("\n"+piece_fp, ":", text)
				ref_name = "piece"+str(i)
				wrie2file(text, output_dir_loc, ref_name)

	return 1

if __name__ == '__main__':

	#init the ret_val to 0
	#this indicates the code exited with an error
	ret_val = 0

	audio_dir_name = input("please enter the name of the file to be processed:\t")
	print("\n")

	audio_dir_loc = "../src/" + audio_dir_name

	if os.path.exists(audio_dir_loc):
		ret_val = main(audio_dir_loc)
	else:
		print("please enter a valid file name or verify if the file exists\n")

	print(f"Exiting with status {ret_val}\n")