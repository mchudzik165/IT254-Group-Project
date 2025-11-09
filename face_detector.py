# Teachable Machine AI face detection test code
# Ran on python 3.11 
# May need to update modules found in code in order to run correctly
# Provides a warning while startup - ignore code warning 
# ENSURE THAT KERAS FILE IS IN THE SAME FOLDER AS THE CODE IS BEING LAUNCHED FROM
# AI GENERATED CODE - NOT FINAL PRODUCT, MEANT FOR AI TESTING PURPOSES

import cv2
import tensorflow as tf
import numpy as np
import zipfile
import os
import tempfile

# === Extract Model from ZIP ===
ZIP_PATH = "converted_keras (3).zip" # change name based on whatever keras file your using 
tmp_dir = tempfile.mkdtemp()
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(tmp_dir)

# Find model file (.h5)
model_path = None
for root, _, files in os.walk(tmp_dir):
    for f in files:
        if f.endswith(".h5"):
            model_path = os.path.join(root, f)
            break
if not model_path:
    raise FileNotFoundError("No .h5 model found in zip archive!")

print(f"[INFO] Loaded model from: {model_path}")

# === LOAD MODEL ===
model = tf.keras.models.load_model(model_path)
input_shape = model.input_shape[1:3]
LABELS = ["Group members", "Other"]  # adjust if keras model your using has multiple classes

# === START CAMERA ===
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

print("[INFO] Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face_img, input_shape)
            face_norm = np.expand_dims(face_resized / 255.0, axis=0)
            preds = model.predict(face_norm, verbose=0)[0]
            best = int(np.argmax(preds))
            current_label = LABELS[best]
            current_confidence = preds[best]

        # GREEN BOX AI GENERATION - REMOVE '#' TO ACTIVATE
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.putText(frame, f"{label} {confidence*100:.1f}%", (x, y-10),
                    #cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # If no face detected, classify full frame
    if len(faces) == 0:
        img_resized = cv2.resize(frame, input_shape)
        img_norm = np.expand_dims(img_resized / 255.0, axis=0)
        preds = model.predict(img_norm, verbose=0)[0]
        best = np.argmax(preds)
        label = LABELS[best]
        confidence = preds[best]
        cv2.putText(frame, f"{label} {confidence*100:.1f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

