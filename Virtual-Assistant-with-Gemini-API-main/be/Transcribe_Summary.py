import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
import mimetypes

# Cấu hình API key và Generative AI
os.environ["API_KEY"] = "AIzaSyAbTbqRQ1N6qjqTFnJQCqG2U6GXDRYiBSg"
genai.configure(api_key=os.environ["API_KEY"])

generation_configuration = {"temperature": 0.7, "top_p": 1, "top_k": 1}
safetySettings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    "gemini-1.5-flash-8b",
    generation_config=generation_configuration,
    safety_settings=safetySettings,
)


def transcribe_audio(file_path, context=""):
    Pr = """Please listen to the audio file provided and transcribe it into a readable dialogue format. 
Separate the roles of each speaker, for example, labeling them as 'Speaker A' and 'Speaker B' (or similar) 
based on their voices and intonation even if the roles are not explicitly marked."""
    Promt = f"{Pr} The context of the conversation is: {context}" if context else Pr

    try:
        # Determine MIME type based on file extension
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'  # Fallback MIME type

        print("Uploading file...")
        with open(file_path, 'rb') as f:
            uploaded_file = genai.upload_file(f, mime_type=mime_type)  # Specify MIME type

        # Transcribe
        print("Transcribing in process...")
        result = model.generate_content([uploaded_file, Promt])
        transcription = result.text.strip()

        return transcription

    except Exception as e:
        return f"Error during transcription: {str(e)}"

# Hàm lưu transcription vào file

def save_transcription(transcription, output_dir="be/backend/media"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "transcription.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcription)
    return output_path
