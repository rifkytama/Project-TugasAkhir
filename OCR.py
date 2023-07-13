import cv2
import numpy as np

# Set up webcam
cap = cv2.VideoCapture(1)  # Use the appropriate webcam index if multiple webcams are available

while True:
    # Capture frame from the webcam
    ret, frame = cap.read()
                                                                                                   
    # Preprocess the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian blur to reduce noise
    _, threshold = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # Apply thresholding to convert to binary image

    # Detect edges using Canny edge detection
    edges = cv2.Canny(threshold, 50, 150)

    # Find contours in the edge image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio
    min_area = 500  # Minimum contour area to consider
    min_aspect_ratio = 2.5  # Minimum aspect ratio of the bounding rectangle to consider
    detected_plates = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)

        if area > min_area and aspect_ratio > min_aspect_ratio:
            detected_plates.append(contour)

    # Draw contours on the frame
    cv2.drawContours(frame, detected_plates, -1, (0, 255, 0), 2)

    # Display the frame with detected contours
    cv2.imshow("Frame", frame)

    # Check for key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()