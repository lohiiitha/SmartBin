from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import os

app = Flask(__name__)

# Load model ONCE
model = YOLO('VisionBin-AI/weights/best.pt')

# Temp directory
TEMP_DIR = 'VisionBin-AI/static/temp'
os.makedirs(TEMP_DIR, exist_ok=True)

# -------------------- ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html')


# ---------- IMAGE DETECTION ----------

@app.route('/detect_image', methods=['POST'])
def detect_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    results = model(img, conf=0.4)

    _, buffer = cv2.imencode('.jpg', results[0].plot())

    detected = list(set([model.names[int(b.cls[0])] for b in results[0].boxes]))
    status = "Detected: " + ", ".join(detected) if detected else "None Detected"

    return jsonify({
        'image': base64.b64encode(buffer).decode('utf-8'),
        'status': status
    })


# ---------- VIDEO UPLOAD + PROCESS ----------

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    filepath = os.path.join(TEMP_DIR, 'temp_video.mp4')
    file.save(filepath)

    # Process video FRAME BY FRAME
    cap = cv2.VideoCapture(filepath)

    cumulative_found = set()

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, conf=0.4)
        found = set([model.names[int(b.cls[0])] for b in results[0].boxes])
        cumulative_found.update(found)

    cap.release()

    if cumulative_found:
        status = "Finished! Found: " + ", ".join(list(cumulative_found))
    else:
        status = "Finished! Found: Nothing"

    return jsonify({'status': status})


# ---------- OPTIONAL: SIMPLE STATUS CHECK ----------

@app.route('/health')
def health():
    return "OK"


# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))