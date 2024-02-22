import telebot
from telebot import types

from config import TOKEN, DB

bot = telebot.TeleBot(TOKEN)

try:
    connected = DB.connect()
    if not connected:
        print("Unable to connect to the database.")
        exit()
except Exception as e:
    print(f"Error while connecting to database: {e}")
    exit()

def init_questions():
    try:
        query = "SELECT * FROM questions"
        questions_data = DB.execute_query(query)

        questions = []
        for question_data in questions_data:
            question = {
                "question": question_data[1],
                "options": []
            }

            query = "SELECT id, option_text, weights FROM options WHERE question_id = %s"
            params = (question_data[0],)
            options_data = DB.execute_query(query, params)

            for option_data in options_data:
                option = {
                    "id": option_data[0],
                    "text": option_data[1],
                    "weights": option_data[2]
                }

                question["options"].append(option)

            questions.append(question)

        return questions
    except Exception as e:
        print(f"Error in init_questions: {e}")
        return []

def init_results():
    try:
        query = "SELECT animal_name, result_text FROM results"
        results_data = DB.execute_query(query)

        results = {}
        for result_data in results_data:
            animal_name = result_data[0]
            result_text = result_data[1]
            results[animal_name] = result_text

        return results
    except Exception as e:
        print(f"Error in init_results: {e}")
        return {}

questions = init_questions()
results = init_results()
points = {}

def update_points(answer, question_number):
    try:
        question_data = questions[question_number]
        for option in question_data["options"]:
            if answer == option["text"]:
                weights = option["weights"]
                for animal, weight in weights.items():
                    points[animal] += weight
    except Exception as e:
        print(f"Error in update_points: {e}")

def show_result(chat_id, message_id):
    try:
        max_animal = max(points, key=points.get)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Поздравляю! Ты - {max_animal}!\n{results.get(max_animal, '')}")
        handle_end_quiz(chat_id)
    except Exception as e:
        print(f"Error in show_result: {e}")

def handle_end_quiz(chat_id):
    try:
        points.clear()
        start_button = types.InlineKeyboardButton(text="Пройти опрос еще раз", callback_data="start_quiz")
        markup = types.InlineKeyboardMarkup().add(start_button)
        bot.send_message(chat_id, "Спасибо за участие в викторине! Хотите пройти ее еще раз?", reply_markup=markup)
    except Exception as e:
        print(f"Error in handle_end_quiz: {e}")

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    try:
        instructions = "Добро пожаловать в викторину 'Какое у вас тотемное животное?'\nОтветьте на следующие вопросы:"
        start_button = types.InlineKeyboardButton(text="Начать викторину", callback_data="start_quiz")
        markup = types.InlineKeyboardMarkup().add(start_button)
        bot.send_message(message.chat.id, instructions, reply_markup=markup)
    except Exception as e:
        print(f"Error in handle_start_help: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def handle_quiz(call):
    try:
        global questions, points
        questions = init_questions()
        points = {animal: 0 for animal in results.keys()}
        ask_question(0, call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"Error in handle_quiz: {e}")

def ask_question(question_number, chat_id, message_id):
    try:
        question_data = questions[question_number]
        question_text = question_data["question"]
        options = question_data["options"]

        markup = types.InlineKeyboardMarkup()
        for option in options:
            callback_data = f"answer_{question_number}_{options.index(option)}"
            markup.add(types.InlineKeyboardButton(text=option["text"], callback_data=callback_data))

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=question_text, reply_markup=markup)
    except Exception as e:
        print(f"Error in ask_question: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("answer"))
def handle_answer(call):
    try:
        data = call.data.split("_")
        question_number = int(data[1])
        option_index = int(data[2])
        answer_text = questions[question_number]["options"][option_index]["text"]
        update_points(answer_text, question_number)
        if question_number < len(questions) - 1:
            ask_question(question_number + 1, call.message.chat.id, call.message.message_id)
        else:
            show_result(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"Error in handle_answer: {e}")

if __name__ == '__main__':
    try:
        bot.polling()
    except Exception as e:
        print(f"Error in main: {e}")
