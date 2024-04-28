import cv2
import tkinter as tk

def initialize_tracker(frame):
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    upper_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)
    upper_bodies = upper_body_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)

    # Combine detections to get a better initial bounding box
    if len(bodies) > 0 or len(upper_bodies) > 0:
        if len(bodies) > 0:
            (x, y, w, h) = bodies[0]
        if len(upper_bodies) > 0:
            (ux, uy, uw, uh) = upper_bodies[0]
            if len(bodies) == 0 or (uy + uh) > (y + h):
                x, y, w, h = ux, uy, uw, uh
        
        x_adjust = w * 0.1
        y_adjust = h * 0.2
        x = max(0, int(x - x_adjust / 2))
        y = max(0, int(y - y_adjust / 2))
        w = int(w + x_adjust)
        h = int(h + y_adjust)

        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, (x, y, w, h))
        return tracker, (x, y, w, h)

    return None, None  


def update_tracker(tracker, frame):
    if tracker is not None:
        success, bbox = tracker.update(frame)
        return success, bbox
    else:
        return False, None  

def analyze_fall(current_bbox, previous_bbox, frame_height, is_alert_active):
    if not previous_bbox or not current_bbox:
        # Default to healthy if no data to compare
        return "Healthy", is_alert_active  

    x, y, w, h = current_bbox
    px, py, pw, ph = previous_bbox

    # Check if the bounding box has moved out of the bottom of the frame
    if y + h > frame_height:
        return "Alert", True

    # Vertical movement check (upward movement might indicate recovery)
    vertical_movement = y - py

    # Check for recovery only if alert is active
    if is_alert_active:
        if vertical_movement < -20 or (y + h < frame_height and h/ph > 0.8):
            # Reset if the object moves up or re-enters the frame properly
            return "Healthy", False  

    return ("Alert" if is_alert_active else "Healthy"), is_alert_active

def detect_humans(frame, tracker=None, previous_bbox=None, is_alert_active=False):
    frame_resized = cv2.resize(frame, (800, 500))
    frame_height = frame_resized.shape[0]
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2GRAY)

    if tracker is None:
        tracker, bbox = initialize_tracker(frame_resized)
        if tracker is None:
            return frame_resized, None, None, "No Human Detected", is_alert_active
    else:
        success, bbox = update_tracker(tracker, frame_resized)
        if not success:
            tracker, bbox = initialize_tracker(frame_resized)
            if not tracker:
                return frame_resized, None, None, "Tracking Lost", is_alert_active

    status, is_alert_active = analyze_fall(bbox, previous_bbox, frame_height, is_alert_active) if previous_bbox else ("Healthy", is_alert_active)

    if bbox:
        x, y, w, h = [int(v) for v in bbox]
        color = (0, 0, 255) if status == "Alert" else (0, 255, 0)
        cv2.rectangle(frame_resized, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame_resized, status, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    return frame_resized, tracker, bbox, status, is_alert_active

def detect_people(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    bodies = body_cascade.detectMultiScale(gray, 1.1, 2)
    return bodies 
