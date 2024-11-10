from flask import Flask, render_template, request, jsonify
from Main import text_to_speech, Chat, Close_Program, speech_to_text  # Import các hàm từ Main.py

app = Flask(__name__)

# Biến lưu lịch sử trò chuyện
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.json['input']  # Nhận input từ người dùng trên front-end
    Chat.send_message(user_input)       # Gửi input đến mô hình AI
    response_text = Chat.last.text      # Nhận phản hồi từ AI
    
    # Lưu lịch sử trò chuyện
    chat_history.append({'user': user_input, 'assistant': response_text})
    
    # Chuyển phản hồi thành giọng nói và phát
    text_to_speech(response_text)
    
    return jsonify({'response': response_text, 'history': chat_history})  # Trả về kết quả dưới dạng JSON

@app.route('/record', methods=['POST'])
def record():
    user_input = speech_to_text()  # Ghi âm và chuyển thành văn bản từ microphone
    if user_input:
        Chat.send_message(user_input)  # Gửi input đến mô hình AI
        response_text = Chat.last.text  # Nhận phản hồi từ AI
        
        # Lưu lịch sử trò chuyện
        chat_history.append({'user': user_input, 'assistant': response_text})
        
        # Chuyển phản hồi thành giọng nói và phát
        text_to_speech(response_text)
        
        return jsonify({'response': response_text, 'history': chat_history})  # Trả về kết quả dưới dạng JSON
    else:
        return jsonify({'response': 'Could not understand the audio.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
