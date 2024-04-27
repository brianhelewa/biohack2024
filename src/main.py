import cv2

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frames from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
