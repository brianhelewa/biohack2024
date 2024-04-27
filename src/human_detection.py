import cv2

def detect_humans(frame):
    # Initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Resize for faster detection
    frame = cv2.resize(frame, (640, 480))
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Detect people in the image
    boxes, weights = hog.detectMultiScale(gray, winStride=(8,8), padding=(8,8), scale=1.05)

    # Draw bounding boxes around detected humans
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    return frame

