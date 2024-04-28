import cv2
from playsound import playsound
import tkinter as tk
from PIL import Image, ImageTk

import geocoder
from twilio.rest import Client




def send_text_message(message):
    # Twilio credentials
    account_sid = 'AC3ea64897585ff44f57b338a3f400de0a'
    auth_token = '4b370b8517e9403987f8c98cea6bf570'
    twilio_phone_number = '+18889953912'
    recipient_phone_number = '' #fill with phone numbers

    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Send the message
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )

        print("Message sent successfully! SID:", message.sid)
    except Exception as e:
        print("Error:", str(e))

# Example usage
message = "Hello from Twilio! This is a test message."
send_text_message(message)



def get_user_location():
    # Get the user's location using IP address
    g = geocoder.ip('me')

    if g.ok:
        # Extract latitude and longitude
        latitude = g.latlng[0]
        longitude = g.latlng[1]

        return latitude, longitude
    else:
        print("Failed to retrieve user's location.")

# Test the function

def emergency():
    latitude, longitude = get_user_location()
    print("Latitude:", latitude)
    print("Longitude:", longitude)

    message = str(latitude+" "+ longitude)
    print(message)
    send_text_message(message)

    screen("911.png")



def printLocation():
    latitude, longitude = get_user_location()
    print("Latitude:", latitude)
    print("Longitude:", longitude)




def screen(image):
    # Read the image
    img = cv2.imread(image)

    # Get screen dimensions
    root = tk.Toplevel()
    screen_width = root.winfo_screenwidth()  # Change this to your screen's width
    screen_height = root.winfo_screenheight()  # Change this to your screen's height
    root.destroy()  # Destroy the temporary Tkinter window

    # Get image dimensions
    img_height, img_width = img.shape[:2]

    # Calculate position to center the image
    x_pos = (screen_width - img_width*2) // 2
    y_pos = (screen_height - img_height*2) // 2

    # Create a window and display the image
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Image', x_pos, y_pos)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def create_popup():
    # Create the pop-up window
    popup_window = tk.Toplevel()
    popup_window.title("Popup Window")

    root = tk.Toplevel()
    screen_width = root.winfo_screenwidth()  # Change this to your screen's width
    screen_height = root.winfo_screenheight()  # Change this to your screen's height

    # Load and resize the image
    image_path = "OcEsda.png"  # Provide the path to your image file
    image = Image.open(image_path)
    image = image.resize((screen_width-200, screen_height-200))  # Resize the image as needed
    photo = ImageTk.PhotoImage(image)

    # Display the image on the pop-up window
    image_label = tk.Label(popup_window, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.pack()

    # Create buttons and pack them horizontally
    button1 = tk.Button(popup_window, text="Button 1", command=lambda: screen("seizure.png"), compound=tk.CENTER)
    button1.pack(side=tk.LEFT)

    button2 = tk.Button(popup_window, text="Button 2", command=lambda: screen("heart.png"), compound=tk.CENTER)
    button2.pack(side=tk.LEFT)

    button3 = tk.Button(popup_window, text="Button 3", command=lambda: screen("drugs.png"), compound=tk.CENTER)
    button3.pack(side=tk.LEFT)

    button4 = tk.Button(popup_window, text="Button 4", command=lambda: screen("blood.png"), compound=tk.CENTER)
    button4.pack(side=tk.LEFT)

    button5 = tk.Button(popup_window, text="Call 911", command=lambda: emergency(),  compound=tk.CENTER)
    button5.pack(side=tk.LEFT)

    # Run the Tkinter event loop
    popup_window.mainloop()

# Load the pre-trained Haar Cascade Classifier for detecting faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize VideoCapture object to capture video from webcam (0) or video file ('filename.mp4')
cap = cv2.VideoCapture(0)

# Minimum height threshold for detecting a lying person
min_height = 250  # Adjust this value according to your needs

dead = False
while True:
    # Read the frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        print("This is y ", y)
        # Check if the face height is below the minimum threshold
        if y > min_height:
            cv2.putText(frame, 'Person dead', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            dead = True

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if dead:
        print("Dead, need help")
        break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Play sound if the person is detected as "dead"
if dead:
    screen("warning.png")
    playsound("sirin.wav")
    printLocation()

# Test the function
create_popup()