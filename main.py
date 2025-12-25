import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE" # Prevents DLL crash

import cv2
from ultralytics import YOLO
import pyttsx3
import speech_recognition as sr
import threading

# --- 1. Improved Voice Function ---
def speak(text):
    print(f"FRIDAY: {text}")
    try:
        # Re-initialize inside the function to prevent "locking"
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop() # Release the audio driver
    except Exception as e:
        print(f"Audio Error: {e}")

# --- 2. Background Listening Loop ---
def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust for background noise once at the start
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Friday is listening for commands...")
        
        while True:
            try:
                # Listen with a strict time limit so she doesn't get stuck
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=4)
                command = recognizer.recognize_google(audio).lower()
                print(f"Heard: {command}")

                if "friday" in command:
                    if "status" in command:
                        speak("All systems are operational. HUD is active.")
                    elif "emergency" in command:
                        speak("Alerting police and ambulance. Coordinates sent.")
                    elif "good bye" in command:
                        speak("Shutting down. Stay safe, Boss.")
                        os._exit(0)
                    else:
                        speak("I am here, Boss. How can I help?")
            except:
                continue

# Start the ear (Microphone) thread
threading.Thread(target=listen_for_commands, daemon=True).start()

# --- 3. Main Eye (Camera) Loop ---
model = YOLO('yolov8n.pt') #
cap = cv2.VideoCapture(0)
speak("Systems online. Vision initialized.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # Object Detection (Point 2 of your project)
    results = model(frame, conf=0.4, verbose=False)
    cv2.rectangle(frame, (20, 20), (620, 460), (0, 255, 0), 1)

    cv2.imshow("Friday Helmet Simulation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()