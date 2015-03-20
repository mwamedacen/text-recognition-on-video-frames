import cv2
import tesseract
import numpy
import sys
import os
import re
import csv
from datetime import timedelta, date
import time


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

def run(startSecond, frame_rate):
	with open("names_annotations.csv","wb") as names_csv:
		with open("functions_annotations.csv","wb") as functions_csv:
			with open("topics_annotations.csv","wb") as topics_csv:			
				names_writer = csv.writer(names_csv, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				functions_writer = csv.writer(functions_csv, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				topics_writer = csv.writer(topics_csv, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
					
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
					duration = 3
					current_time_stamp =  startSecond+i*frame_rate
					start_time = timedelta(0, current_time_stamp)
					stop_time = timedelta(0, current_time_stamp+duration)
					duration = timedelta(0, duration)
					

					print filename,current_time_stamp
					
					current_name = detect_words('frames.avi/'+filename.replace(".jpg","")+"_thresholded.jpg", 290, 450, 720-290, 500-450)
					current_function = ''
					current_topic = detect_words('frames.avi/'+filename, 0, 495, 720, 576-495)

					if '\n' in current_name:
						current_name = detect_words('frames.avi/'+filename.replace(".jpg","")+"_thresholded.jpg", 290, 450, 720-290, 480-450,)
						current_function = detect_words('frames.avi/'+filename.replace(".jpg","")+"_thresholded.jpg", 290, 475, 720-290, 500-475)

					if current_name.strip() != "":
						print 'OCR_NAME', current_name.strip(), start_time, stop_time, duration
						names_writer.writerow(['OCR_NAME', current_name.strip(), start_time, stop_time, duration])
						names_array.append(current_name)
					
					if current_function.strip() != "":
						print 'OCR_FUNCTION', current_function.strip(), start_time, stop_time, duration
						functions_writer.writerow(['OCR_FUNCTION', current_function.strip(), start_time, stop_time, duration])
						functions_array.append(current_function)
					
					if current_topic.strip() != "":
						print 'OCR_TOPIC', current_topic.strip(), start_time, stop_time, duration
						topics_writer.writerow(['OCR_TOPIC', current_topic.strip(), start_time, stop_time, duration])
						topics_array.append(current_topic)
				
				print names_array

				print '\n'

				print topics_array

				print '\n'

				print functions_array

				print '\n'

				print len(names_array), len(functions_array), len(topics_array)

def main():
	run(263, 3)

main()
