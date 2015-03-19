import cv2

def inverte(imagem, name):
	imagem = (255-imagem)
	cv2.imwrite(name, imagem)

def main():
	img = cv2.imread('frames_cropped/00000010.jpg_function.jpg')

	inverte(img, "image.jpg")

main()
