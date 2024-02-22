import psycopg2
import json

def connect():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="m_zoo",
        user="pan",
        password="bd!!<FPF22lfyys[33",
        port="5432"
    )
    return conn

def create_tables():
    conn = connect()
    cur = conn.cursor()

    # Создание таблицы вопросов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            question_text TEXT NOT NULL
        )
    """)

    # Создание таблицы вариантов ответов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS options (
            id SERIAL PRIMARY KEY,
            question_id INTEGER REFERENCES questions(id),
            option_text TEXT NOT NULL,
            weights JSONB NOT NULL
        )
    """)

    # Удаление таблицы options, если она уже существует
    cur.execute("DROP TABLE IF EXISTS options")

    # Создание таблицы вариантов ответов с правильной схемой
    cur.execute("""
        CREATE TABLE IF NOT EXISTS options (
            id SERIAL PRIMARY KEY,
            question_id INTEGER REFERENCES questions(id),
            option_text TEXT NOT NULL,
            weights JSONB NOT NULL
        )
    """)

    # Заполнение таблицы вопросов
    questions_data = [
        {
            "question": "Вопрос 1: Какой цвет шерсти больше всего нравится?",
            "options": [
                {"text": "Коричневый", "weights": {"Рысь": 1, "Медведь": 1, "Панда": 1, "Лев": 1, "Коала": 1, "Волк": 0}},
                {"text": "Черный", "weights": {"Рысь": 0, "Медведь": 0, "Панда": 0, "Лев": 1, "Коала": 0, "Волк": 1}},
                {"text": "Белый", "weights": {"Рысь": 0, "Медведь": 0, "Панда": 1, "Лев": 0, "Коала": 1, "Волк": 0}},
                {"text": "Рыжий", "weights": {"Рысь": 1, "Медведь": 0, "Панда": 0, "Лев": 0, "Коала": 0, "Волк": 0}},
                {"text": "Серый", "weights": {"Рысь": 0, "Медведь": 1, "Панда": 0, "Лев": 0, "Коала": 0, "Волк": 0}}
            ]
        },
        {
            "question": "Вопрос 2: Какую еду предпочитаешь?",
            "options": [
                {"text": "Мясо", "weights": {"Рысь": 2, "Медведь": 1, "Панда": 0, "Лев": 3, "Коала": 0, "Волк": 2}},
                {"text": "Овощи", "weights": {"Рысь": 0, "Медведь": 1, "Панда": 2, "Лев": 0, "Коала": 2, "Волк": 0}},
                {"text": "Фрукты", "weights": {"Рысь": 0, "Медведь": 0, "Панда": 2, "Лев": 0, "Коала": 2, "Волк": 0}},
                {"text": "Рыбу", "weights": {"Рысь": 1, "Медведь": 3, "Панда": 0, "Лев": 0, "Коала": 5, "Волк": 0}},
                {"text": "Ягоды", "weights": {"Рысь": 0, "Медведь": 2, "Панда": 3, "Лев": 0, "Коала": 2, "Волк": 0}}
            ]
        }
        # Добавьте остальные вопросы здесь
    ]

    for question_data in questions_data:
        question_text = question_data["question"]
        options = question_data["options"]

        cur.execute("INSERT INTO questions (question_text) VALUES (%s) RETURNING id", (question_text,))
        question_id = cur.fetchone()[0]

        for option in options:
            option_text = option["text"]
            weights = json.dumps(option["weights"])
            cur.execute("INSERT INTO options (question_id, option_text, weights) VALUES (%s, %s, %s)",
                        (question_id, option_text, weights))

    # Заполнение таблицы результатов
    results = {
        "Рысь": "Вы энергичны, быстры в принятии решений и всегда готовы к новым приключениям.",
        "Медведь": "Вы сильны, мудры и защищаете своих близких. Вас привлекает спокойная и уединенная обстановка.",
        "Панда": "Вы спокойны, милы и миролюбивы. Вас привлекает обилие еды и уютная обстановка.",
        "Лев": "Вы смелы, лидер по своей натуре и всегда готовы защищать свою территорию.",
        "Коала": "Вы спокойны, ленивы и предпочитаете проводить время на деревьях.",
        "Волк": "Вы умны, сообразительны и предпочитаете работать в команде. Вас привлекают сложные задачи."
    }

    for animal_name, result_text in results.items():
        cur.execute("INSERT INTO results (animal_name, result_text) VALUES (%s, %s)",
                    (animal_name, result_text))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
