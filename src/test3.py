import cv2

# Load the pre-trained Haar Cascade Classifier for detecting faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize VideoCapture object to capture video from webcam (0) or video file ('filename.mp4')
cap = cv2.VideoCapture(0)

# Number of frames without a face before considering someone has passed out
no_face_threshold = 30
no_face_count = 0

while True:
    # Read the frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        no_face_count += 1
    else:
        no_face_count = 0

    if no_face_count >= no_face_threshold:
        print("No face detected for", no_face_threshold, "frames. Possible pass out.")
        # Add your action here, like triggering an alarm or sending a notification

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()