from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from giao_tiep import chatbot_response
from Transcribe_Summary import transcribe_audio, save_transcription
from Document_processing import start_conversation
from giao_tiep import text_to_speech, speech_to_text 
import speech_recognition as sr

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "media/audio"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
chat_history = []  # Add this line
# Endpoint chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400
    
    response = chatbot_response(user_input)
    return jsonify({"response": response})

# Endpoint for transcription
@app.route('/transcribe', methods=['POST'])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    context = request.form.get("context", "")

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(file_path)
        print(f"Saved audio file to {file_path}")

        # Convert audio file to text
        user_input = transcribe_audio(file_path, context)
        print(f"Transcribed text: {user_input}")

        # Save transcription
        try:
            output_path = save_transcription(user_input)
            print(f"Saved transcription to {output_path}")
        except Exception as e:
            print(f"Error saving transcription: {e}")
            return jsonify({"error": "Failed to save transcription."}), 500

        # Delete the original audio file
        try:
            os.remove(file_path)
            print(f"Deleted audio file: {file_path}")
        except PermissionError as e:
            print(f"PermissionError while deleting file: {e}")
            return jsonify({"error": "File is in use and cannot be deleted."}), 500
        except Exception as e:
            print(f"Unexpected error while deleting file: {e}")
            return jsonify({"error": "Failed to delete audio file."}), 500

        # Return the transcription file
        return send_file(output_path, as_attachment=True)


# New endpoint for document processing
@app.route('/process_document', methods=['POST'])
def process_document():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join("media/documents", filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        summary = start_conversation(file_path)

        os.remove(file_path)

        return jsonify({"summary": summary})
    


@app.route('/record', methods=['POST'])
def record():
    if "file" not in request.files:
        print("No file part in the request.")
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        print("No selected file.")
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(file_path)
        print(f"Saved audio file to {file_path}")

        # Convert audio file to text
        user_input = speech_to_text(file_path)
        os.remove(file_path)  # Clean up the original file
        print(f"Transcribed text: {user_input}")

        if user_input:
            response_text = chatbot_response(user_input)
            print(f"Chatbot response: {response_text}")
            
            # Save chat history
            chat_history.append({'user': user_input, 'assistant': response_text})
            print(f"Updated chat history: {chat_history}")
            
            return jsonify({'response': response_text, 'history': chat_history})
        else:
            print("Could not understand the audio.")
            return jsonify({'response': 'Could not understand the audio.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
