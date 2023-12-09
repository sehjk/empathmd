let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let context = canvas.getContext('2d');
let captureButton = document.getElementById('capture');

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing webcam:", err);
    });

captureButton.addEventListener('click', function() {
    context.drawImage(video, 0, 0, 640, 480);
    let image = canvas.toDataURL('image/png');
    // Send the image to the server
    sendImageToServer(image);
});

function sendImageToServer(imageData) {
    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
