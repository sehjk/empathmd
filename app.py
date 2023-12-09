from flask import Flask, request, jsonify, send_from_directory
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Your existing /upload route
@app.route('/upload', methods=['POST'])


def upload_image():
    data = request.get_json()  # Get JSON data
    image_data = data['image']  # Access the image data

    # Optional: Decode the image if you need to process it
    # image_data = image_data.split(",")[1]  # Remove the base64 header
    # image_bytes = base64.b64decode(image_data)

    # Code to handle image and send it to GPT-4 vision model
    return jsonify({'message': 'Image received', 'size': len(image_data)})

if __name__ == '__main__':
    app.run(debug=True)
