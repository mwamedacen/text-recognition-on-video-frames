import cv2
import tesseract
import numpy
import sys
import os

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
	name_board = img[200:225, 130:350]
	topic_board = img[220:400, 0:350]

def main():

	extensionsToCheck = (".png",".jpg",".tiff")

	filenames = next(os.walk('.'))[2]

	for filename in filenames:
		if filename.endswith(extensionsToCheck):
			crop_image(filename)

	for filename in filenames:
		if filename.endswith(extensionsToCheck):
			print filename,':'
			print detectWords(filename)
			print '-'*100
main()