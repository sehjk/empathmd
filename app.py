from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files['image']
    # Code to handle image and send it to GPT-4 vision model
    return "Image received"

if __name__ == '__main__':
    app.run(debug=True)
