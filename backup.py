from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import requests
app = Flask(__name__)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите что-то...")
        recognizer.adjust_for_ambient_noise(source)  # настройка шумоподавления
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print("Вы сказали:", text)
        return text
    except sr.UnknownValueError:
        print("Извините, не удалось распознать речь")
        return None
    except sr.RequestError as e:
        print("Ошибка при запросе к сервису распознавания речи; {0}".format(e))
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_user_input", methods=["POST"])
def process_user_input():
    user_input = request.json.get("user_input")
    if user_input:
        user_input = user_input.lower()
        if "баланс" in user_input:
            response = "Запрос на проверку баланса пользователя"
        elif "перевод" in user_input:
            response = "Запрос на перевод средств"
        elif "продукты" in user_input or "кредит" in user_input:
            response = "Запрос на информацию о кредитных продуктах"
        elif "пароль" in user_input:
            response = "Запрос на изменение пароля пользователя"
        elif "помощь" in user_input:
            response = "Запрос на помощь"
        elif "выход" in user_input:
            response = "Спасибо за использование нашего сервиса!"
        else:
            response = "Извините, я не могу понять ваш запрос. Пожалуйста, повторите или задайте другой вопрос."
    else:
        response = "Извините, не удалось распознать ваш запрос."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
