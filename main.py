from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import time
import io
import base64
import re

# Создание и обучение чат-бота
chatbot = ChatBot('Мой чат-бот')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.russian")

app = Flask(__name__)

# Переменная для отслеживания времени приостановки
pause_until = 0

# Функция фильтрации нежелательного контента
def filter_profanity(text):
    profanity_list = ['сука', 'блять', 'х**', 'член', 'говно','какашки']  # добавьте сюда ненормативную лексику
    replacement_word = "[цензура]"

    pattern = r'\b(' + '|'.join([re.escape(word) for word in profanity_list]) + r')\b'
    regex = re.compile(pattern, flags=re.IGNORECASE)

    # Замена найденных слов на "[цензура]"
    return regex.sub(replacement_word, text)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_user_input", methods=["POST"])
def process_user_input():
    global pause_until
    current_time = time.time()

    if current_time < pause_until:
        return jsonify({'text': "Сервис временно приостановлен. Попробуйте позже.", 'audio': ''})

    user_input = request.json.get("user_input")

    # Фильтрация нежелательного контента
    user_input = filter_profanity(user_input)

    if user_input:
        if user_input.lower() == "люда":
            pause_until = current_time + 10  # Приостановка на 10 секунд
            return jsonify({'text': "Сервис приостановлен на 10 секунд.", 'audio': ''})

        # Проверка на наличие символа "*" в сообщении
        if '*' in user_input:
            return jsonify({'text': "Пожалуйста, избегайте использования неприличных слов или выражений.", 'audio': ''})

        try:
            response_text = str(chatbot.get_response(user_input))
            tts = gTTS(text=response_text, lang='ru')
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            mp3_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')

            return jsonify({
                'text': response_text,
                'audio': mp3_base64
            })
        except Exception as e:
            return jsonify({'text': str(e), 'audio': ''})
    else:
        return jsonify({'text': "Извините, не удалось распознать ваш запрос.", 'audio': ''})


if __name__ == "__main__":
    app.run(debug=True)