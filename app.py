from flask import Flask, request, jsonify, send_from_directory, Response
import base64
import requests
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


chat_history = []

@app.route('/chat', methods=['POST'])
def chat_with_gpt():
    global chat_history
    data = request.get_json()
    user_message = {"role": "user", "content": data['message']}
    
    # Append the user message to the history
    chat_history.append(user_message)

    # OpenAI API Key
    api_key = os.environ.get('OPENAI_API_KEY')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-1106-preview",  # Adjust the model name as needed
        "messages": chat_history,
        "stream": True
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    def generate():
        for chunk in response.iter_content(chunk_size=None):  # None means it will stream as the data comes in
            if chunk:
                json_chunk = json.loads(chunk)
                assistant_response = json_chunk['choices'][0]['message']['content']
                yield f"data:{assistant_response}\n\n"
    
    return Response(generate(), content_type='text/event-stream')

    
    # Extract the assistant's response and append it to the chat history
    #assistant_response = response.json()['choices'][0]['message']['content']
    #chat_history.append({"role": "assistant", "content": assistant_response})
    
    #return jsonify({"response": assistant_response})


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
                        "text": "Here's a picture of a person. Describe the posture and their facial expressions, briefly."
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
