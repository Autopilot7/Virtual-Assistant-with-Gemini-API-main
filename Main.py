import google.generativeai as genai
import os
import time  
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound



#Lên trang Gemini API, tạo API key (free)
os.environ["API_KEY"] = "AIzaSyAhuxSrWShqIKQUbptlrfIUnfsIg1XADv0" #Điền API trong ""
genai.configure(api_key=os.environ["API_KEY"])

# Điều chỉnh độ ngu học của AI
generation_configuration = {
    #Creativeness (0-1)
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
}

#Tắt hết chức năng an toàn 
safetySettings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE" 

    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE" 

    },
]

# Tạo model = API: gemini-1.5-flash: nhanh mà ngu, gemini-1.5-pro: khôn mà chậm
model = genai.GenerativeModel("gemini-1.5-flash", 
                              generation_config=generation_configuration, 
                              safety_settings= safetySettings)

#test
#respone = model.generate_content(input("Ask Gemini: "))
#print(respone.text)


#Promt cho AI
system_message1 = """
SYSTEM MESSAGE: You are being used to power a voice assistant and should respond as so.
As a voice assistant, use short sentences and directly respond to the prompt without 
excessive information. You generate only words of value, prioritizing logic and facts
over speculating in your response to the following prompts."""
system_message = system_message1.replace('\n', '')

personal_information = """
"Hello! I'm Sarah, your dedicated assistant. 
I'm here to help Hà Minh Dũng, a 20-year-old Information Technology student at VinUniversity, manage tasks, tackle assignments, and find resources to make studying easier. 
I know you enjoy reading manga and hitting the gym, so I can also provide recommendations and workout tips when needed. 
Whether it's academic assistance or daily reminders, I’m just a message away. Let's make your life easier, Dũng!
 And say hi to your roommates Đạt Chai, Thái Minh Dũng, and Lê Ngọc Toàn from me!"""
personal_information = personal_information.replace('\n', '')


#Khởi tạo promt
Chat = model.start_chat(
    history=[
        {"role": "user", "parts": system_message1},
        {"role": "model", "parts": "Ok"},
        {"role": "user", "parts": "Who are you?"},
        {"role": "model", "parts": personal_information},

    ]
)


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


def speech_to_text():
    # Khởi tạo recognizer
    recognizer = sr.Recognizer()
    
    # Sử dụng microphone làm nguồn âm thanh
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")

        # Lắng nghe âm thanh từ microphone
        audio = recognizer.listen(source)

        try:
            # Sử dụng Google Web Speech API để nhận diện giọng nói
            text = recognizer.recognize_google(audio, language="en-US")
            print("Client: ", text)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Sorry, there was an issue with the Google API.")
    
    return text if 'text' in locals() else None

#Check kết thúc chương trình
def Close_Program(text):
    keywords = ["bye", "rest"]
    for word in keywords:
        if word in text.lower():
            return True
    return False

#Code
print("Glad to see you again, boss, how may I help you today?")
text_to_speech("Glad to see you again, boss, how may I help you today?")

def main_voice_loop():
    # Code vòng lặp giọng nói chuyển vào hàm này
    print("Glad to see you again, boss, how may I help you today?")
    text_to_speech("Glad to see you again, boss, how may I help you today?")

    while True: 
        user_input = speech_to_text()  
        Chat.send_message(user_input)
        print(Chat.last.text)
        text_to_speech(Chat.last.text)
        if Close_Program(user_input):
            break

# Chỉ chạy vòng lặp khi chạy Main.py độc lập, không chạy khi import vào app.py
if __name__ == "__main__":
    main_voice_loop()


