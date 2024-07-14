from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant.And your name is Danish"},
            {"role": "user", "content": user_message}
        ]
    )

    ai_message = response['choices'][0]['message']['content'].strip()
    return jsonify({"message": ai_message})

if __name__ == '__main__':
    app.run(debug=True)

