from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import os

app = Flask(__name__)
model = YOLO('weights/best.pt')

# Directory for temp video storage
TEMP_DIR = 'static/temp'
os.makedirs(TEMP_DIR, exist_ok=True)

camera_active = False
cap = None
current_video_path = None

def generate_frames():
    global camera_active, cap
    cap = cv2.VideoCapture(0)
    camera_active = True
    while camera_active:
        success, frame = cap.read()
        if not success: break
        results = model(frame, conf=0.4)
        annotated_frame = results[0].plot()
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    if cap: cap.release()

def generate_uploaded_frames():
    global current_video_path
    if not current_video_path: return
    v_cap = cv2.VideoCapture(current_video_path)
    # Get total frames to know when to stop
    total_frames = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    while count < total_frames:
        success, frame = v_cap.read()
        if not success: break
        results = model(frame, conf=0.4)
        annotated_frame = results[0].plot()
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        count += 1
    v_cap.release()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/video_feed')
def video_feed(): return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/uploaded_video_feed')
def uploaded_video_feed(): return Response(generate_uploaded_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_feed')
def stop_feed():
    global camera_active
    camera_active = False
    return jsonify({'status': 'stopped'})

@app.route('/detect_image', methods=['POST'])
def detect_image():
    file = request.files['file']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    results = model(img, conf=0.4)
    _, buffer = cv2.imencode('.jpg', results[0].plot())
    
    detected = list(set([model.names[int(b.cls[0])] for b in results[0].boxes]))
    status = "Detected: " + ", ".join(detected) if detected else "None Detected"
    
    return jsonify({'image': base64.b64encode(buffer).decode('utf-8'), 'status': status})

@app.route('/upload_video', methods=['POST'])
def upload_video():
    global current_video_path
    file = request.files['file']
    path = os.path.join(TEMP_DIR, 'temp_video.mp4')
    file.save(path)
    current_video_path = path
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(debug=True, port=5000)