from flask import jsonify
import google.generativeai as genai
import os
from gtts import gTTS
from playsound import playsound
import time
import speech_recognition as sr
import subprocess

def convert_to_pcm_wav(input_path, output_path):
    try:
        subprocess.run([
            'ffmpeg', '-i', input_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            output_path
        ], check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio: {e}")
        return None
# API Key và cấu hình Generative AI
os.environ["API_KEY"] = "AIzaSyAbTbqRQ1N6qjqTFnJQCqG2U6GXDRYiBSg"
genai.configure(api_key=os.environ["API_KEY"])

generation_configuration = {"temperature": 0.7, "top_p": 1, "top_k": 1}
safetySettings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_configuration, safety_settings=safetySettings)

system_message1 = """
SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so.
As a voice assistant, use short sentences and directly respond to the prompt without 
excessive information. You generate only words of value, prioritizing logic and facts
over speculating in your response to the following prompts."""
system_message = system_message1.replace('\n', '')

personal_information = """
"Hello! you are Sarah, my dedicated assistant. 
I'm  Hà Minh Dũng, a 20-year-old Information Technology student at VinUniversity, manage tasks, tackle assignments, and find resources to make studying easier. 
I enjoy reading manga and hitting the gym, and i need recommendations and workout tips when needed. 
Whether it's academic assistance or daily reminders, you are just a message away. You are here to make my life easier, 
 And say hi to my roommates Đạt Chai, Thái Minh Dũng, and Lê Ngọc Toàn"""
personal_information = personal_information.replace('\n', '')

Chat = model.start_chat(
    history=[
        {"role": "user", "parts": system_message1},
        {"role": "model", "parts": "Ok"},
        {"role": "user", "parts": personal_information},
        {"role": "model", "parts": "Sure"},
    ]
)

def chatbot_response(user_input):
    Chat.send_message(user_input)
    return Chat.last.text



def text_to_speech(text, lang='en', slow=False):
    # Chuyển văn bản thành tệp âm thanh với tốc độ nhanh và giọng tiếng Anh
    tts = gTTS(text=text, lang=lang, slow=slow)
    filename = "speech.mp3"
    tts.save(filename)
    
    # Phát tệp âm thanh
    playsound(filename)
    
    # Thêm thời gian chờ để đảm bảo âm thanh đã phát xong
    time.sleep(0)  # Thay đổi thời gian nếu cần thiết
    
    # Xoá tệp sau khi phát
    os.remove(filename)


def speech_to_text(file_path):
    try:
        # Check if the file is already PCM WAV
        if not is_pcm_wav(file_path):
            print("Audio file is not PCM WAV. Conversion is required.")
            return None  # or handle accordingly

        # Initialize recognizer
        recognizer = sr.Recognizer()

        print(f"Processing audio file: {file_path}")

        with sr.AudioFile(file_path) as source:
            print("Reading audio file...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)

        print("Performing speech recognition...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"Recognized text: {text}")
        return text
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def is_pcm_wav(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(44)  # WAV header size
        return b'fmt ' in header and b'PCM' in header