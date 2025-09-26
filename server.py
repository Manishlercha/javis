from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import jarvis
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/ask', methods=['POST'])
def ask_jarvis():
    data = request.json
    user_input = data.get('message', '')
    # Call your Jarvis process_command and get a string response
    response = jarvis.process_command(user_input)
    # If process_command returns True/False, you may want to return a custom string
    if response is True:
        response = "Command processed."
    elif response is False:
        response = "Goodbye, sir."
    elif not response:
        response = "No response from Jarvis."
    return jsonify({'response': response})

@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/index.html')
def serve_index_html():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), filename)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
