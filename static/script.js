document.addEventListener("DOMContentLoaded", () => {
    const imageInput = document.getElementById('imageUpload');
    const videoInput = document.getElementById('videoUpload');
    const displayContainer = document.getElementById('display-container');
    const webcamBtn = document.getElementById('start-webcam');
    const photoLabel = document.getElementById('upload-photo-label');
    const videoLabel = document.getElementById('upload-video-label');

    let isWebcamRunning = false;

    function stopWebcamIfRunning() {
        if (isWebcamRunning) {
            fetch('/stop_feed');
            webcamBtn.innerText = "Start Webcam";
            webcamBtn.style.background = "#10b981";
            isWebcamRunning = false;
        }
    }

    function resetButtonLabels() {
        if (photoLabel) photoLabel.innerText = "Upload Photo";
        if (videoLabel) videoLabel.innerText = "Upload Video";
    }

    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (!file) return;
        stopWebcamIfRunning();
        resetButtonLabels();
        photoLabel.innerText = "Upload Another Photo";
        displayContainer.innerHTML = `<p style="color: #38bdf8;">Analyzing...</p>`;
        
        const formData = new FormData();
        formData.append('file', file);
        fetch('/detect_image', { method: 'POST', body: formData })
            .then(res => res.json())
            .then(data => {
                displayContainer.innerHTML = `<img src="data:image/jpeg;base64,${data.image}" style="max-width:100%; border-radius:8px;">`;
                document.getElementById('waste-status').innerHTML = `<p style="color:#10b981;">${data.status}</p>`;
                document.getElementById('item-type').innerText = `Item: ${data.status.replace('Detected: ', '')}`;
            });
        this.value = '';
    });

    videoInput.addEventListener('change', function() {
        const file = this.files[0];
        if (!file) return;
        stopWebcamIfRunning();
        resetButtonLabels();
        videoLabel.innerText = "Upload Another Video";
        displayContainer.innerHTML = ""; // Kill previous streams

        const formData = new FormData();
        formData.append('file', file);
        fetch('/upload_video', { method: 'POST', body: formData })
            .then(res => res.json())
            .then(data => {
                const t = new Date().getTime();
                displayContainer.innerHTML = `<img src="/uploaded_video_feed?t=${t}" style="width:100%; height:100%; object-fit:cover; border-radius:8px;">`;
                document.getElementById('waste-status').innerHTML = `<p style="color:#10b981;">🟢 Video Analysis Active</p>`;
            });
        this.value = '';
    });

    webcamBtn.addEventListener('click', function() {
        if (!isWebcamRunning) {
            resetButtonLabels();
            displayContainer.innerHTML = `<img src="/video_feed" style="width:100%; height:100%; object-fit:cover; border-radius:8px;">`;
            webcamBtn.innerText = "Stop Webcam";
            webcamBtn.style.background = "#ef4444";
            isWebcamRunning = true;
        } else {
            fetch('/stop_feed');
            displayContainer.innerHTML = `<p>Live Camera Feed / Uploaded Media</p>`;
            webcamBtn.innerText = "Start Webcam";
            webcamBtn.style.background = "#10b981";
            isWebcamRunning = false;
        }
    });
});