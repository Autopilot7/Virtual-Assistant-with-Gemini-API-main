import time
import random
import google.generativeai as genai
import os


#Lên trang Gemini API, tạo API key (free)
os.environ["API_KEY"] = "AIzaSyAhuxSrWShqIKQUbptlrfIUnfsIg1XADv0" #Điền API trong ""
genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)
