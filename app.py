from flask import Flask, request, jsonify, send_from_directory
import base64
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Your existing /upload route
@app.route('/upload', methods=['POST'])


@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data['image']

    # OpenAI API Key
    api_key = os.environ.get('OPENAI_API_KEY')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Write an effusive poem about any individual seen in the image. Make it endearing and relatable. Use simple language."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
