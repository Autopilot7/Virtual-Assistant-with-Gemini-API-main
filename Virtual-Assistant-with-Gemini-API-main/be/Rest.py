import time
import random
import google.generativeai as genai
import os


#Lên trang Gemini API, tạo API key (free)
os.environ["API_KEY"] = "AIzaSyBLUy4Rjlmeban5sw8YsmQwpMokvuJBY7E" #Điền API trong ""
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

# Correct the model name if necessary
model = genai.GenerativeModel("gemini-1.5-flash", 
                              generation_config=generation_configuration, 
                              safety_settings= safetySettings)

# Correct the prompts definition
prompt = """You are a voice assistant and should respond as so.
As a voice assistant, your master has been studying for an hour and you should remind he/her to rest in shorts sentences
by jokes or songs or poems, etc """




# Function to generate and print content every hour
def hourly_check_in():
    while True:
        # Generate content using the model
        response = model.generate_content(prompt)
        print(response.text)
        # Wait for 1 hour (3600 seconds) before next check-in
        time.sleep(3600)

# Run the hourly check-in function
hourly_check_in()
