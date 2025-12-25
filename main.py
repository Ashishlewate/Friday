import os
import cv2
import time
import qrcode
import pyttsx3
import threading
import speech_recognition as sr
from ultralytics import YOLO

# Prevents the common Windows DLL/KMP crash
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# --- 1. GLOBAL SETTINGS & INITIALIZATION ---
tracker = {} 
max_speed_recorded = 0  # Global variable to track highest speed
start_time = time.strftime("%Y-%m-%d %H:%M:%S")

def speak(text):
    print(f"FRIDAY: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop() 
    except Exception as e:
        print(f"Audio Error: {e}")

# --- 2. BACKGROUND VOICE LISTENING ---
def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Friday is calibrated and listening...")
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=4)
                command = recognizer.recognize_google(audio).lower()
                print(f"Heard: {command}")

                if "friday" in command:
                    if "status" in command:
                        speak("All systems are operational. HUD is active.")
                    elif "emergency" in command:
                        speak("Alerting police and ambulance. Coordinates sent.")
                    elif "good bye" in command:
                        generate_report()
                        speak("Shutting down. Stay safe, Boss.")
                        os._exit(0)
                    else:
                        speak("I am here, Boss.")
            except:
                continue

def generate_report():
    """Generates the QR code summary of the drive."""
    global max_speed_recorded
    trip_data = f"TRIP SUMMARY\nDate: {start_time}\nMax Speed: {max_speed_recorded} KM/H\nStatus: Secure"
    qr = qrcode.make(trip_data)
    qr.save("driving_details_qr.png")
    print("\n--- REPORT GENERATED ---")
    print(trip_data)

# Start Voice Thread
threading.Thread(target=listen_for_commands, daemon=True).start()

# --- 3. MAIN VISION & SPEED LOOP ---
model = YOLO('yolov8n.pt') 
cap = cv2.VideoCapture(0)
speak("Systems online. Vision initialized.")

# 

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # Object Detection (Project Point 2)
    results = model(frame, conf=0.4, verbose=False)
    current_time = time.time()

    # IRON MAN HUD - Static Elements
    cv2.rectangle(frame, (20, 20), (620, 460), (0, 255, 0), 1)
    cv2.putText(frame, f"MAX SPD: {max_speed_recorded} KM/H", (450, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            
            # Detect Bikes and Cars
            if label in ['car', 'motorcycle', 'bus']:
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                obj_id = f"{label}_{center_x // 30}" # Simple spatial tracking

                speed = 0
                if obj_id in tracker:
                    prev_x, prev_y, prev_time = tracker[obj_id]
                    distance = ((center_x - prev_x)**2 + (center_y - prev_y)**2)**0.5
                    dt = current_time - prev_time
                    if dt > 0:
                        speed = int((distance / dt) * 0.7) # Scale factor for simulation
                        if speed > max_speed_recorded:
                            max_speed_recorded = speed # Error fixed here

                tracker[obj_id] = (center_x, center_y, current_time)

                # Target HUD
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"{label.upper()} {speed} KM/H", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow("Friday Helmet Simulation", frame)
    
    # Press 'q' to quit manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        generate_report()
        speak("Session terminated.")
        break

cap.release()
cv2.destroyAllWindows()