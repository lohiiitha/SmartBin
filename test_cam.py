from ultralytics import YOLO
import cv2

# 1. Load your trained AI brain
model = YOLO('weights/best.pt')

# 2. Open your Mac's built-in webcam
cap = cv2.VideoCapture(0)

print("Starting VisionBin AI... Press 'q' to quit.")

while True:
    # Read the video frame
    success, frame = cap.read()
    if not success:
        break

    # 3. Let the AI look at the frame and make predictions
    # conf=0.4 means it will only show boxes if it is 40%+ confident
    results = model(frame, conf=0.4)

    # 4. Draw the bounding boxes and 'Dry/Wet' labels on the video
    annotated_frame = results[0].plot()

    # 5. Show the video window
    cv2.imshow("VisionBin AI - Live Feed", annotated_frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()