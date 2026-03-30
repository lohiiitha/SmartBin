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

# Global States
camera_active = False
video_active = False
cap = None
current_video_path = None
current_detections = "Waiting for item..."

def generate_frames():
    global camera_active, cap, current_detections
    cap = cv2.VideoCapture(0)
    camera_active = True
    while camera_active:
        success, frame = cap.read()
        if not success: break
        results = model(frame, conf=0.4)
        
        # Update sidebar status for Live Webcam
        found = list(set([model.names[int(b.cls[0])] for b in results[0].boxes]))
        current_detections = "Detected: " + ", ".join(found) if found else "Scanning..."
        
        annotated_frame = results[0].plot()
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    if cap: cap.release()

def generate_uploaded_frames():
    global current_video_path, current_detections, video_active
    if not current_video_path: return
    v_cap = cv2.VideoCapture(current_video_path)
    video_active = True
    
    # Track everything found throughout the entire video
    cumulative_found = set()
    
    while video_active:
        success, frame = v_cap.read()
        if not success: break
        
        results = model(frame, conf=0.4)
        found = set([model.names[int(b.cls[0])] for b in results[0].boxes])
        cumulative_found.update(found) # Add newly found items to the tracker
        
        # Real-time update while video plays
        current_detections = "Detected: " + ", ".join(list(found)) if found else "Scanning..."
        
        annotated_frame = results[0].plot()
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    
    v_cap.release()
    video_active = False
    
    # When video ends, show the cumulative results instead of erasing them
    if cumulative_found:
        current_detections = "Finished! Found: " + ", ".join(list(cumulative_found))
    else:
        current_detections = "Finished! Found: Nothing"

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/video_feed')
def video_feed(): 
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/uploaded_video_feed')
def uploaded_video_feed(): 
    return Response(generate_uploaded_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_status')
def get_status():
    global current_detections
    return jsonify({'status': current_detections})

@app.route('/stop_feed')
def stop_feed():
    global camera_active, video_active, current_detections
    camera_active = False
    video_active = False
    current_detections = "Waiting for item..."
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
    global current_video_path, video_active
    # Stop any current video stream before saving new one
    video_active = False 
    
    file = request.files['file']
    path = os.path.join(TEMP_DIR, 'temp_video.mp4')
    file.save(path)
    current_video_path = path
    return jsonify({'status': 'success'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))