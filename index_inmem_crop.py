import cv2
import tesseract
import numpy
import sys
import os
import re

def detect_words(filename, left, top, width, height):
	api = tesseract.TessBaseAPI()
	api.SetOutputName("outputName");
	api.Init(".","fra",tesseract.OEM_DEFAULT)
	api.SetPageSegMode(tesseract.PSM_AUTO)
	pixImage=tesseract.pixRead(filename)
	api.SetImage(pixImage)
	api.SetRectangle(left,top,width,height)
	outText=api.GetUTF8Text()
	api.End()
	return outText

def main():
	startMillisecond = 500

	names_buffer = open('names_buffer.txt', 'w')
	topics_buffer = open('topics_buffer.txt', 'w')
	functions_buffer = open('functions_buffer.txt', 'w')

	names_array = []
	topics_array = []
	functions_array = []

	orginal_files_extensions = (".png",".jpg",".tiff")
	cropped_files_extensions = ("_name.jpg","_topic.jpg")
	name_files_extension = "_name.jpg"
	topic_files_extension = "_topic.jpg"
	function_files_extension = "_function.jpg"

	frames_folder = next(os.walk("frames.avi"))[2]
	
	for filename in frames_folder:
		current_name = detect_words('frames.avi/'+filename, 290, 450, 720-290, 500-450)
		current_function = ''
		current_topic = detect_words('frames.avi/'+filename, 0, 495, 720, 576-495)

		if '\n' in current_name:
			current_name = detect_words('frames.avi/'+filename, 290, 450, 720-290, 480-450,)
			current_function = detect_words('frames.avi/'+filename, 290, 475, 720-290, 500-475)

		names_buffer.write(current_name+'\n')
		functions_buffer.write(current_function+'\n')
		topics_buffer.write(current_topic+'\n')

		names_array.append(current_name)
		functions_array.append(current_function)
		topics_array.append(current_topic)
		
	
	names_buffer.close()
	functions_buffer.close()
	topics_buffer.close()

	print names_array

	print '\n'

	print topics_array

	print '\n'

	print functions_array

	print '\n'

	print len(names_array), len(functions_array), len(topics_array)

main()