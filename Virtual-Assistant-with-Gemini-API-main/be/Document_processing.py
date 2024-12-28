import google.generativeai as genai
import os
import speech_recognition as sr
from PyPDF2 import PdfReader  # Import for PDF handling
from docx import Document  # Import for DOCX handling

os.environ["API_KEY"] = "AIzaSyAbTbqRQ1N6qjqTFnJQCqG2U6GXDRYiBSg"
genai.configure(api_key=os.environ["API_KEY"])

generation_configuration = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
}

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

model = genai.GenerativeModel("gemini-1.5-flash-8b", 
                              generation_config=generation_configuration, 
                              safety_settings=safetySettings)

def convert_docx_to_text(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def convert_pdf_to_text(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages])

def start_conversation(file_path):
    print("Uploading...")
    if file_path.endswith('.docx'):
        text_content = convert_docx_to_text(file_path)
    elif file_path.endswith('.pdf'):
        text_content = convert_pdf_to_text(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a .pdf or .docx file.")

    print("Processing...")
    response = model.generate_content(["Give me a summary of this document.", text_content])
    return response.text  # Return the generated summary
    
# Example usage
# response = start_conversation("path/to/your/file.pdf")
# print(response.text) 


