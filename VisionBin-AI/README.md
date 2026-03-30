# ♻️ VisionBin AI
**Real-Time Smart Waste Detection & Segregation Dashboard**

Built for the DTI Internship Project (2026), VisionBin AI is an end-to-end web application that uses computer vision to automatically detect and categorize waste (e.g., Plastic, Biodegradable) in real-time. 

## ✨ Features
* **Live Webcam Feed:** Streams video directly from your local camera, drawing AI bounding boxes in real-time with an integrated hardware kill-switch.
* **Photo Analysis:** Upload static images for instant waste categorization.
* **Video Processing:** Upload `.mp4` or `.mov` files to see frame-by-frame AI tracking and multi-object detection.
* **Dynamic UI Dashboard:** Custom-built dark theme dashboard that polls the Python backend twice a second for live detection updates.

## 🛠️ Tech Stack
* **AI Model:** YOLO (Ultralytics) custom-trained on waste datasets (`best.pt`).
* **Backend:** Python, Flask, OpenCV (`cv2`).
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (with AJAX polling).

---

## 🚀 Installation & Setup

This application is fully cross-platform and will run on both Mac and Windows.

### 1. Prerequisites
Ensure you have Python installed on your system. 
* **Windows Users:** Download from [python.org](https://www.python.org/downloads/). *Crucial: Check the box that says "Add python.exe to PATH" during installation.*
* **Mac Users:** Python3 is usually pre-installed, but can be updated via Homebrew.

### 2. Clone the Repository
Download the ZIP or clone the repo to your local machine:
```bash
git clone [https://github.com/YOUR_USERNAME/VisionBin_AI.git](https://github.com/YOUR_USERNAME/VisionBin_AI.git)
cd VisionBin_AI
3. Install Dependencies
Open your terminal (or VS Code terminal) and run the following command to install the required computer vision and web libraries:

For Windows:

Bash
pip install flask ultralytics opencv-python
For Mac:

Bash
pip3 install flask ultralytics opencv-python
4. Folder Structure Check
Before running the app, ensure your directory looks exactly like this:

Plaintext
VisionBin_AI/
│
├── app.py                  # Main Flask Server
├── weights/
│   └── best.pt             # Your trained YOLO AI model
├── templates/
│   └── index.html          # Dashboard UI
└── static/
    ├── style.css           # UI Styling
    ├── script.js           # Frontend Logic & Polling
    ├── logo.jpeg           # Dashboard Logo
    └── favicon.png         # Browser Tab Icon
💻 How to Run
Start the Flask server from your terminal:

For Windows:

Bash
python app.py
For Mac:

Bash
python3 app.py
You should see a message saying * Running on http://127.0.0.1:5000.

Open your web browser (Chrome, Safari, or Edge) and navigate to: https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:5000

Click "Start Webcam" to begin real-time detection, or use the upload buttons to test media!

⚠️ Troubleshooting
1. Port 5000 is in use (Mac Users):
macOS sometimes uses Port 5000 for the AirPlay Receiver. If the app crashes silently:

Go to System Settings > General > AirPlay & Handoff and turn off "AirPlay Receiver".

Alternatively, change the port in app.py from 5000 to 5001.

2. Python command opens the Windows Store:

Go to Windows Settings > Manage app execution aliases.

Turn OFF the "App Installer" toggles next to python.exe and python3.exe.

Turn ON "Python (default)" and "Python install manager".


Let me know if there's any other documentation you need to generate before your submission!