import cv2
from human_detection import detect_humans

def main():
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from webcam.")
            break

        # Process the frame for human detection
        processed_frame = detect_humans(frame)

        # Display the processed frame
        cv2.imshow('Human Detection', processed_frame)

        # Break the loop if 'q' is

