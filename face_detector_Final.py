# Teachable Machine AI face detection code
# Ran on python 3.11 
# May need to update modules found in code in order to run correctly
# Provides a tensorflow warning while startup - ignore code warning 
# ENSURE THAT KERAS FILE IS IN THE SAME FOLDER AS THE CODE IS BEING LAUNCHED FROM

import cv2
import tensorflow as tf
import numpy as np
import zipfile
import os
import tempfile
import time

# Serial (pyserial) may not be installed on the user's system.
# Attempt an import and provide a graceful fallback so the
# rest of the script (face detection) still runs.
try:
    import serial
    SERIAL_AVAILABLE = True
except ModuleNotFoundError:
    serial = None
    SERIAL_AVAILABLE = False
    print("Warning: pyserial is not installed. Serial features disabled.\nInstall with: python -m pip install pyserial")

face_start_time = None
no_face_start_time = None
door_open = False

OPEN_DELAY = 3     # seconds needed to OPEN
CLOSE_DELAY = 3    # seconds needed to CLOSE

# open serial connection (set your COM port)
arduino = None
if SERIAL_AVAILABLE:
    try:
        arduino = serial.Serial('COM7', 9600, timeout=1)
        time.sleep(2)  # give Arduino time to reset
    except Exception as e:
        print(f"Warning: could not open serial port: {e}")
        arduino = None
else:
    arduino = None

# Helper for safe writes
def send_serial_byte(b):
    if arduino:
        try:
            arduino.write(b)
        except Exception as e:
            print(f"Serial write error: {e}")

LABELS = ["Matt","Elliott", "Brayden", "Michael", "No one", "Other"] # adjust if keras model your using has multiple classes

#extracts and finds keras model
ZIP_PATH = "converted_keras (5).zip" # change name based on whatever keras file your using 
tmp_dir = tempfile.mkdtemp()
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(tmp_dir)

model_path = None
for root, _, files in os.walk(tmp_dir):
    for f in files:
        if f.endswith(".h5"):
            model_path = os.path.join(root, f)
            break

#loads model and camera
model = tf.keras.models.load_model(model_path)
input_shape = model.input_shape[1:3]

camera = cv2.VideoCapture(0) # change to 1 if doesn't work
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#live output + camera box detection
print("\n--- Live Status Output ---\n")

while True:
    ret, frame = camera.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    frame_predictions = []

    if len(faces) > 0:
        # Start timing face detection
        if face_start_time is None:
            face_start_time = time.time()

        no_face_start_time = None  # reset "no face" timer

        # Check if door should open
        if not door_open and (time.time() - face_start_time >= OPEN_DELAY):
            send_serial_byte(b'O')   # tell Arduino to open door
            door_open = True
            print(">>> DOOR OPENED")

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face_img, input_shape)
            face_norm = np.expand_dims(face_resized / 255.0, axis=0)

            preds = model.predict(face_norm, verbose=0)[0]
            best = int(np.argmax(preds))
            label = LABELS[best]
            confidence = preds[best]

            frame_predictions.append((label, confidence))

            # green box and label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence*100:.1f}%",
                        (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)

    else:
        # No face detected — start timer
        if no_face_start_time is None:
            no_face_start_time = time.time()

        face_start_time = None  # reset "face present" timer

        # Check if door should close
        if door_open and (time.time() - no_face_start_time >= CLOSE_DELAY):
            send_serial_byte(b'C')   # tell Arduino to close door
            door_open = False
            print(">>> DOOR CLOSED")

        frame_predictions.append(("No face detected", 0))

    # Overlay summary text of top predictions (first 3)
    if frame_predictions:
        preds_to_show = frame_predictions[:3]
        summary = " | ".join([f"{p[0]} {p[1]*100:.0f}%" for p in preds_to_show])
        cv2.putText(frame, summary, (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Display the frame in a window and allow quitting with 'q'
    cv2.imshow('Face Detector', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print('Exiting on user request')
        break

# Close serial port if opened
if arduino:
    try:
        arduino.close()
    except Exception:
        pass

camera.release()
cv2.destroyAllWindows()
