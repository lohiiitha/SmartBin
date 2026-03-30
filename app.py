import gradio as gr
from ultralytics import YOLO

# Load model
model = YOLO("weights/best.pt")

def detect(image):
    results = model(image)
    output = results[0].plot()
    return output

interface = gr.Interface(
    fn=detect,
    inputs=gr.Image(type="numpy"),
    outputs=gr.Image(type="numpy"),
    title="SmartBin AI - Waste Detection",
    description="Upload an image to detect waste"
)

interface.launch()