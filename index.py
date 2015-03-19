import tesseract, sys

api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = sys.argv[1]
pixImage=tesseract.pixRead(mImgFile)
api.SetImage(pixImage)
outText=api.GetUTF8Text()


print("OCR output:\n%s"%outText);
api.End()