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
    const base64Image = imageData.split(',')[1];

    fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: base64Image })
    })
    .then(response => response.json())  // Parse the response as JSON
    .then(data => {
        console.log(data);
        displayResponse(data);  // Call function to display the response
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayResponse(data) {
    const responseElement = document.getElementById('response');
    // Assuming the response contains a text field you want to display
    // Modify as needed based on the actual structure of the response
    responseElement.textContent = data.choices[0].message.content;  // Or any other field from the response
}