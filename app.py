from flask import Flask, request, jsonify, render_template
import os
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)

# Initialize Vertex AI and GenerativeModel
project_id = "vertext-0001"
vertexai.init(project=project_id, location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001")

# Personal assistant name
assistant_name = "Danish"

# Default responses for greetings and small talk
greetings = ["Hi there!", "Hello! How can I assist you today?", "Hey! What can I do for you?"]
small_talk_responses = {
    "how are you": "I'm here and ready to help!",
    "who are you": f"I'm {assistant_name}, your personal assistant.",
    "what can you do": "I can help you with various tasks like answering questions and providing information.",
    "thank you": "You're welcome!",
    "bye": "Goodbye! Have a great day!"
}

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("user_input", "").strip().lower()  # Get user input and normalize

    if not user_input:
        return jsonify({"message": "Please provide a valid input."}), 400

    # Check for greetings and small talk
    for phrase, response in small_talk_responses.items():
        if phrase in user_input:
            return jsonify({"message": response})

    try:
        response = model.generate_content(user_input)
        ai_message = response.text.strip()
        return jsonify({"message": ai_message})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
