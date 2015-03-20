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

def image_processing_with_threshold(filename):
	image = cv2.imread(filename)
	ret, threshold = cv2.threshold(image, 225,255, cv2.THRESH_BINARY_INV)
	cv2.imwrite(filename.replace(".jpg","")+"_thresholded.jpg", threshold)

def run(startMillisecond, frame_rate):

	names_buffer = open('names_buffer.csv', 'w')
	topics_buffer = open('topics_buffer.csv', 'w')
	functions_buffer = open('functions_buffer.csv', 'w')

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
		image_processing_with_threshold('frames.avi/'+filename)

	for i in range(0, len(frames_folder)):
		filename = frames_folder[i]
		current_time_stamp =  startMillisecond+i*frame_rate

		#print filename,current_time_stamp
		
		current_name = detect_words('frames.avi/'+filename.replace(".jpg","")+"_thresholded.jpg", 290, 450, 720-290, 500-450)
		current_function = ''
		current_topic = detect_words('frames.avi/'+filename, 0, 495, 720, 576-495)

		if '\n' in current_name:
			current_name = detect_words('frames.avi/'+filename.replace(".jpg","")+"_thresholded.jpg", 290, 450, 720-290, 480-450,)
			current_function = detect_words('frames.avi/'+filename.replace(".jpg","")+"_thresholded.jpg", 290, 475, 720-290, 500-475)

		names_buffer.write(str(current_time_stamp)+';'+current_name.strip()+'\n')
		functions_buffer.write(str(current_time_stamp)+';'+current_function.strip()+'\n')
		topics_buffer.write(str(current_time_stamp)+';'+current_topic.strip()+'\n')

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

def main():
	run(84.558, 3)
	
main()