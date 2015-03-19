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
	img = cv2.imread(filename)
	name_board = img[450:500, 290:720]
	topic_board = img[495:576, 0:720]
	cv2.imwrite(filename+'_name.jpg', name_board)
	cv2.imwrite(filename+'_topic.jpg', topic_board)

def clean_cropped_images():
	dir = '.'
	for f in os.listdir(dir):
		if re.search('_(name|topic)\.jpg', f):
			os.remove(os.path.join(dir, f))

def main():
	clean_cropped_images()

	orginal_files_extensions = (".png",".jpg",".tiff")
	cropped_files_extensions = ("_name.jpg","_topic.jpg")

	filenames = next(os.walk('.'))[2]

	for filename in filenames:
		if filename.endswith(orginal_files_extensions):
			crop_image(filename)

	for filename in filenames:
		if filename.endswith(cropped_files_extensions):
			print filename,':'
			print detect_words(filename)
			print '-'*100
main()