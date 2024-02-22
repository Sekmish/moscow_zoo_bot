import telebot
from telebot import types
import psycopg2
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

def init_questions():
    conn = psycopg2.connect(database="m_zoo", user="pan", password="bd!!<FPF22lfyys[33", host="127.0.0.1", port="5432")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")
    questions_data = cursor.fetchall()

    questions = []
    for question_data in questions_data:
        question = {
            "question": question_data[1],
            "options": []
        }

        cursor.execute("SELECT id, option_text, weights FROM options WHERE question_id = %s", (question_data[0],))
        options_data = cursor.fetchall()

        for option_data in options_data:
            option = {
                "id": option_data[0],
                "text": option_data[1],
                "weights": option_data[2]
            }

            question["options"].append(option)

        questions.append(question)

    conn.close()

    return questions

def init_results():
    conn = psycopg2.connect(database="m_zoo", user="pan", password="bd!!<FPF22lfyys[33", host="127.0.0.1", port="5432")
    cursor = conn.cursor()

    cursor.execute("SELECT animal_name, result_text FROM results")
    results_data = cursor.fetchall()

    results = {}
    for result_data in results_data:
        results[result_data[0]] = result_data[1]

    conn.close()

    return results

questions = init_questions()
results = init_results()

points = {"Рысь": 0, "Медведь": 0, "Панда": 0, "Лев": 0, "Коала": 0, "Волк": 0}

def update_points(answer, question_number):
    question_data = questions[question_number]
    for option in question_data["options"]:
        if answer == option["text"]:
            weights = option["weights"]
            for animal, weight in weights.items():
                points[animal] += weight

def show_result(chat_id, message_id):
    max_animal = max(points, key=points.get)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Поздравляю! Ты - {max_animal}!\n{results[max_animal]}")
    handle_end_quiz(chat_id)

def handle_end_quiz(chat_id):
    start_button = types.InlineKeyboardButton(text="Пройти опрос еще раз", callback_data="start_quiz")
    markup = types.InlineKeyboardMarkup().add(start_button)
    bot.send_message(chat_id, "Спасибо за участие в викторине! Хотите пройти ее еще раз?", reply_markup=markup)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = "Добро пожаловать в викторину 'Какое у вас тотемное животное?'\nОтветьте на следующие вопросы:"
    start_button = types.InlineKeyboardButton(text="Начать викторину", callback_data="start_quiz")
    markup = types.InlineKeyboardMarkup().add(start_button)
    bot.send_message(message.chat.id, instructions, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def handle_quiz(call):
    global questions, points
    questions = init_questions()
    points = {"Рысь": 0, "Медведь": 0, "Панда": 0, "Лев": 0, "Коала": 0, "Волк": 0}
    ask_question(0, call.message.chat.id, call.message.message_id)

def ask_question(question_number, chat_id, message_id):
    question_data = questions[question_number]
    question_text = question_data["question"]
    options = question_data["options"]

    markup = types.InlineKeyboardMarkup()
    for option in options:
        callback_data = f"answer_{question_number}_{options.index(option)}"
        markup.add(types.InlineKeyboardButton(text=option["text"], callback_data=callback_data))

    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=question_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("answer"))
def handle_answer(call):
    data = call.data.split("_")
    question_number = int(data[1])
    option_index = int(data[2])
    answer_text = questions[question_number]["options"][option_index]["text"]
    update_points(answer_text, question_number)
    if question_number < len(questions) - 1:
        ask_question(question_number + 1, call.message.chat.id, call.message.message_id)
    else:
        show_result(call.message.chat.id, call.message.message_id)

if __name__ == '__main__':
    bot.polling()
