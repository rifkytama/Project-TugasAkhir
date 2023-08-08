import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd =r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread('beat.jpg')
image = imutils.resize(image, width=500)

cv2.imshow('Original Image', image)
cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

smooth = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("Gray Image", gray)
cv2.waitKey(0)

corner = cv2.Canny(gray, 170, 200)
cv2.imshow("Highlighted edges", corner)
cv2.waitKey(0)

seg , new = cv2.findContours(corner.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

image1 = image.copy()
cv2.drawContours(image1, seg, -1, (0,0,255),3)
cv2.imshow('Edge segmention', image1)
cv2.waitKey(0)

seg=sorted(seg , key=cv2.contourArea, reverse=True)[:30]
NoPlate = None

image2 = image.copy()
cv2.drawContours(image2, seg, -1, (0,255,0),3)
cv2.imshow("Number plate segmention", image2)
cv2.waitKey(0)

count = 0
name = 1

for i in seg:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.02*perimeter, True)

    if(len(approx == 4)):
        NoPlate = approx
        x, y, w, h = cv2.boundingRect(i)
        crp_image = image[y:y+h, x:x+w]

        cv2.imwrite(str(name)+ '.png', crp_image)
        name += 1

        break

cv2.drawContours(image,[NoPlate], -1, (0,255,0),3)
cv2.imshow("Final Image", image)
cv2.waitKey(0)

crp_img = '1.png'
cv2.imshow('Number Plate', cv2.imread(crp_img))
cv2.waitKey(0)