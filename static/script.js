document.addEventListener("DOMContentLoaded", () => {
    const imageInput = document.getElementById('imageUpload');
    const videoInput = document.getElementById('videoUpload');
    const displayContainer = document.getElementById('display-container');
    const webcamBtn = document.getElementById('start-webcam');
    const photoLabel = document.getElementById('upload-photo-label');
    const videoLabel = document.getElementById('upload-video-label');

    let isWebcamRunning = false;
    let statusInterval = null;

    function startStatusPolling() {
        if (statusInterval) clearInterval(statusInterval);
        statusInterval = setInterval(() => {
            fetch('/get_status')
                .then(res => res.json())
                .then(data => {
                    if (data.status) {
                        document.getElementById('waste-status').innerHTML = `<p style="color:#10b981; font-weight:bold;">${data.status}</p>`;
                        
                        // Clean up the text for the sub-label
                        let itemText = data.status.replace('Detected: ', '').replace('Finished! Found: ', '');
                        document.getElementById('item-type').innerText = `Item: ${itemText}`;
                        
                        // CRITICAL: Stop polling once the video finishes so the result stays on screen forever
                        if (data.status.includes("Finished!")) {
                            stopStatusPolling();
                        }
                    }
                });
        }, 500);
    }

    function stopStatusPolling() {
        if (statusInterval) clearInterval(statusInterval);
    }

    function stopWebcamIfRunning() {
        if (isWebcamRunning) {
            fetch('/stop_feed');
            webcamBtn.innerText = "Start Webcam";
            webcamBtn.style.background = "#10b981";
            isWebcamRunning = false;
            stopStatusPolling();
        }
    }

    function resetButtonLabels() {
        if (photoLabel) photoLabel.innerText = "Upload Photo";
        if (videoLabel) videoLabel.innerText = "Upload Video";
    }

    // Photo Upload
    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (!file) return;
        
        stopWebcamIfRunning();
        stopStatusPolling(); // Kill any lingering video status
        resetButtonLabels();
        photoLabel.innerText = "Upload Another Photo";
        displayContainer.innerHTML = `<p style="color: #38bdf8;">Analyzing...</p>`;
        
        const formData = new FormData();
        formData.append('file', file);
        fetch('/detect_image', { method: 'POST', body: formData })
            .then(res => res.json())
            .then(data => {
                displayContainer.innerHTML = `<img src="data:image/jpeg;base64,${data.image}" style="max-width:100%; max-height:100%; border-radius:8px; object-fit:contain;">`;
                document.getElementById('waste-status').innerHTML = `<p style="color:#10b981; font-weight:bold;">${data.status}</p>`;
                document.getElementById('item-type').innerText = `Item: ${data.status.replace('Detected: ', '')}`;
            });
        this.value = '';
    });

    // Video Upload
    videoInput.addEventListener('change', function() {
        const file = this.files[0];
        if (!file) return;

        stopWebcamIfRunning();
        stopStatusPolling();
        
        displayContainer.innerHTML = `<p style="color: #38bdf8;">Uploading New Video...</p>`;
        
        const formData = new FormData();
        formData.append('file', file);

        fetch('/stop_feed').then(() => {
            fetch('/upload_video', { method: 'POST', body: formData })
                .then(res => res.json())
                .then(data => {
                    resetButtonLabels();
                    videoLabel.innerText = "Upload Another Video";
                    const t = new Date().getTime();
                    displayContainer.innerHTML = `<img src="/uploaded_video_feed?t=${t}" style="width:100%; height:100%; object-fit:contain; border-radius:8px;">`;
                    startStatusPolling();
                });
        });
        this.value = '';
    });

    // Webcam Logic
    webcamBtn.addEventListener('click', function() {
        if (!isWebcamRunning) {
            resetButtonLabels();
            displayContainer.innerHTML = `<img src="/video_feed" style="width:100%; height:100%; object-fit:cover; border-radius:8px;">`;
            webcamBtn.innerText = "Stop Webcam";
            webcamBtn.style.background = "#ef4444";
            isWebcamRunning = true;
            startStatusPolling();
        } else {
            fetch('/stop_feed');
            displayContainer.innerHTML = `<p>Live Camera Feed / Uploaded Media</p>`;
            webcamBtn.innerText = "Start Webcam";
            webcamBtn.style.background = "#10b981";
            isWebcamRunning = false;
            stopStatusPolling();
            document.getElementById('waste-status').innerHTML = `<p>Waiting for item...</p>`;
            document.getElementById('item-type').innerText = `Item: None Detected`;
        }
    });
});