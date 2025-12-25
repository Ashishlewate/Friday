# Friday
Friday is a AI who helps us while driving bike by wearing helmet , also shows speed and contact with nearest police station and hospital
An Iron Man-inspired "Friday" AI assistant for motorcycle helmets. This prototype uses computer vision to detect vehicles and calculate relative speed, while employing voice recognition for emergency protocols and automated data logging.

🚀 Features
Iron Man HUD UI: A real-time Heads-Up Display (HUD) overlay built with OpenCV, providing visual feedback and targeting.

Intelligent Object Detection: Utilizes YOLOv8 (You Only Look Once) to identify cars, motorcycles, and pedestrians in real-time.

Dynamic Speed Estimation: Calculates vehicle velocity based on pixel displacement over frame-rate intervals.

Voice-Activated Command System: A multithreaded architecture that listens for "Friday" triggers to perform status checks or emergency calls.

Automated SOS Protocol: Simulated emergency response system that alerts authorities and medical services upon request.

QR Telemetry Logging: Automatically encodes trip data (Max Speed, Timestamp) into a QR code for post-ride analysis.
