import cv2
import tesseract
import numpy
import sys
import os
import re

def detect_words(filename):
	api = tesseract.TessBaseAPI()
	api.SetOutputName("outputName");
	api.Init(".","eng",tesseract.OEM_DEFAULT)
	api.SetPageSegMode(tesseract.PSM_AUTO)
	pixImage=tesseract.pixRead(filename)
	api.SetImage(pixImage)
	outText=api.GetUTF8Text()
	api.End()
	return outText

def crop_image(filename):
	img = cv2.imread('frames.avi/'+filename)
	name_board = img[450:500, 290:720]
	#name_board = img[450:480, 290:720]
	#name_board = img[475:500, 290:720]
	topic_board = img[495:576, 0:720]
	cv2.imwrite('frames_cropped/'+filename+'_name.jpg', name_board)
	cv2.imwrite('frames_cropped/'+filename+'_topic.jpg', topic_board)

def crop_image_name_function(filename):
	img = cv2.imread('frames.avi/'+filename)
	name_board = img[450:480, 290:720]
	function_board = img[475:500, 290:720]
	
	cv2.imwrite('frames_cropped/'+filename+'_name.jpg', name_board)
	cv2.imwrite('frames_cropped/'+filename+'_function.jpg', function_board)
	

def clean_cropped_images(dir):
	for f in os.listdir(dir):
		if re.search('_(name|topic)\.jpg', f):
			os.remove(os.path.join(dir, f))

def main():
	clean_cropped_images("frames_cropped")

	names_array = []
	topics_array = []

	orginal_files_extensions = (".png",".jpg",".tiff")
	cropped_files_extensions = ("_name.jpg","_topic.jpg")
	name_files_extension = "_name.jpg"
	topic_files_extension = "_topic.jpg"

	frames_folder = next(os.walk("frames.avi"))[2]

	for filename in frames_folder:
		if filename.endswith(orginal_files_extensions):
			crop_image(filename)

	
	cropped_folder = next(os.walk("frames_cropped"))[2]

	for filename in cropped_folder:
		if filename.endswith(name_files_extension):
			current_name = detect_words('frames_cropped/'+filename)
			names_array.append(current_name)
		elif filename.endswith(topic_files_extension):
			current_topic = detect_words('frames_cropped/'+filename)
			topics_array.append(current_topic)

	print names_array

	print topics_array

main()