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
        for (x, y, w, h) in faces:

            face_img = frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face_img, input_shape)
            face_norm = np.expand_dims(face_resized / 255.0, axis=0)

            preds = model.predict(face_norm, verbose=0)[0]
            best = int(np.argmax(preds))
            label = LABELS[best]
            confidence = preds[best]

            frame_predictions.append((label, confidence))

           #green box and label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence*100:.1f}%",
                        (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)
    else:
        frame_predictions.append(("No face detected", 0))

    #prints current status into terminal
    print("\n--- Frame Predictions ---")
    for lbl, conf in frame_predictions:
        if lbl == "No face detected":
            print("No face detected")
        else:
            print(f"Detected: {lbl}  |  Confidence: {conf*100:.1f}%")

    #shows active camera feed 
    cv2.imshow("Webcam", frame)

    # ESC to quit
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()
