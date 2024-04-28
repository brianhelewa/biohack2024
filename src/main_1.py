import tkinter as tk
from PIL import Image, ImageTk
import cv2
from threading import Thread
from human_detection1 import detect_humans 

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Camera Feed")
        self.label = tk.Label(self)  
        self.label.pack()
        self.running = True
        self.tracker = None
        self.previous_bbox = None
        self.is_alert_active = False

        # Create a separate window for displaying the alert image but don't show it yet
        self.alert_window = tk.Toplevel(self)
        self.alert_window.title("Alert Image")
        self.alert_window.withdraw() 

        self.alert_label = tk.Label(self.alert_window)
        self.alert_label.pack()

        # Prepare the button but do not display it yet
        self.prepare_button()

    def prepare_button(self):
        button_img_path = 'data/OcEsda_Button.png'  
        button_img = Image.open(button_img_path)
        button_img = button_img.resize((250, 80))  
        button_photo_img = ImageTk.PhotoImage(button_img)
        self.button = tk.Button(self.alert_window, image=button_photo_img, command=self.open_new_image_window)
        self.button.image = button_photo_img  

    def display_alert_image(self):
        if self.is_alert_active:
            # Show the alert window
            self.alert_window.deiconify() 
            alert_image_path = 'data/OcEsda_WarningScreen.png' 
            alert_image = Image.open(alert_image_path)
            alert_image = ImageTk.PhotoImage(alert_image)
            self.alert_label.configure(image=alert_image)
            self.alert_label.image = alert_image 
            self.button.place(x=750, y=800) 

    def open_new_image_window(self):
        # This function is called when the button is clicked
        new_image_window = tk.Toplevel(self)
        new_image_window.title("New Image")
        new_image_path = 'data/OcEsda.png' 
        new_image = Image.open(new_image_path)

        # Calculate new dimensions based on the scaling factor
        scale_factor = 0.75 
        new_width = int(new_image.width * scale_factor)
        new_height = int(new_image.height * scale_factor)

        # Resize the image
        new_image = new_image.resize((new_width, new_height), Image.Resampling.LANCZOS)  
        new_image = ImageTk.PhotoImage(new_image)
        new_image_label = tk.Label(new_image_window, image=new_image)
        new_image_label.image = new_image  
        new_image_label.pack()

    def update_image(self, img):
        tk_img = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.label.configure(image=tk_img)
        self.label.image = tk_img 

    def video_loop(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame, self.tracker, new_bbox, status, self.is_alert_active = detect_humans(
                frame, self.tracker, self.previous_bbox, self.is_alert_active)
            self.previous_bbox = new_bbox
            if self.is_alert_active:
                self.display_alert_image()
            else:
                self.update_image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def on_closing(self):
        self.running = False
        self.alert_window.destroy() 
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    Thread(target=app.video_loop).start()
    app.mainloop()
