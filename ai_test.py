from flask import Flask, render_template, request, jsonify
import openai
import sqlite3
import voice_support
import os

# Set OpenAI API key
OPENAI_API_KEY="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"
openai.api_key = os.getenv(OPENAI_API_KEY)

app = Flask(__name__)

'''def get_answer_from_db(question):
    """Fetch answer from SQLite database if question exists."""
    try:
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM college_queries WHERE question LIKE ?", (f'%{question}%',))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None'''

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    try:
        user_message = request.form.get("msg")
        if not user_message:
            return jsonify({'response': 'No message received'})

        # Check if the query exists in the database
        '''db_answer = get_answer_from_db(user_message)
        if db_answer:
            voice_support.speak(db_answer)
            return jsonify({'response': db_answer, 'audio': "static/bot_response.mp3"})'''

        # If not found, use OpenAI GPT response
        bot_response = get_chat_response(user_message)
        voice_support.speak(bot_response)
        return jsonify({'response': bot_response, 'audio': "static/bot_response.mp3"})

    except Exception as e:
        print(f"❌ Error processing chat: {e}")
        return jsonify({'response': 'Sorry, there was an error'})

@app.route("/voice", methods=["GET"])
def voice_chat():
    """Handles voice input, gets a response, and converts to speech."""
    try:
        user_message = voice_support.recognize_speech()
        if not user_message or user_message.lower() == "sorry, i couldn't understand that.":
            return jsonify({'response': "I couldn't understand your voice. Try again!"})

        db_answer = get_answer_from_db(user_message)
        if db_answer:
            voice_support.speak(db_answer)
            return jsonify({'response': db_answer, 'audio': "static/bot_response.mp3"})

        bot_response = get_chat_response(user_message)
        voice_support.speak(bot_response)
        return jsonify({'response': bot_response, 'audio': "static/bot_response.mp3"})

    except Exception as e:
        print(f"❌ Voice processing error: {e}")
        return jsonify({'response': 'Sorry, there was an error'})

def get_chat_response(text):
    """Generate a response using OpenAI's GPT model if no database answer is found."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=350
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"❌ AI response error: {e}")
        return "Sorry, I couldn't generate a response."

if __name__ == '__main__':
    app.run(debug=False)

#
# print(os.getenv("OPENAI_API_KEY"))
