import openai
from flask import Flask, request, render_template, jsonify
import speech_recognition as sr

import json
import os
import glob


openai.api_key = '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'

r = sr.Recognizer()

def record():
    r = sr.Recognizer()
    print("Hello, please speak in the microphone.")
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            data = r.record(source, duration=10)
            try:
                text = r.recognize_google(data, language='en')
                print(text)
                return (text)
            except:
                print("Please speak clearly in the microphone!")
                return("Please speak clearly in the mic.")



def read_txt_file(filename):
    with open(filename, 'r') as file:
        return file.read()


# Set up Flask application
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('./index.html')


# Set up route to receive WhatsApp messages
@app.route('/get-response', methods=['POST'])
def get_response():


        # data = request.get_json()

        user_input = record()
        policies = read_txt_file("culinary.txt")


        # Construct conversation history including user data
        conversation = [
            {"role": "system", "content": f"You are a master chef working with Gordan Ramsey as a judge on his show. Analyze the contestant's response based on the following criteria: {policies}."},
            {"role": "user", "content": f"{user_input}"},
            {"role": "assistant", "content": f"{policies}"}
        ]

        # Use OpenAI API to generate response based on message and user data
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Extract the generated response from the OpenAI API
        response_text = response['choices'][0]['message']['content']

        obj = {
            'response_text': response_text,
            'user_input': user_input
        }

        print(obj)

        return (obj)



# @app.route('/record_audio', methods=['POST'])
# def record_audio():
#     pass


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
