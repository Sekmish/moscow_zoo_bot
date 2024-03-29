import psycopg2
import json
from config import DB_NAME, DB_PORT, DB_HOST, DB_USER, DB_PASSWORD

def connect():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
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


    # Создание таблицы results
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id SERIAL PRIMARY KEY,
            animal_name TEXT,
            result_text TEXT,
            image_url TEXT
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

    # Заполнение таблицы вопросов
    questions_data = [
        {
            "question": "Какой цвет шерсти больше всего нравится?",
            "options": [
                {"text": "Коричневый", "weights": {"Медведь": 3, "Лев": 1, "Сурикат": 1, "Лошадь": 2, "Соболь": 1}},
                {"text": "Черный", "weights": {"Панда": 3, "Шиншилла": 1, "Пингвин": 2, "Павлин": 1, "Тигр": 2}},
                {"text": "Белый", "weights": {"Аист": 2, "Коала": 1, "Песец": 2, "Ласка": 3, "Фламинго": 2}},
                {"text": "Рыжий", "weights": {"Лиса": 3, "Леопард": 1, "Динго": 2, "Кенгуру": 2, "Рысь": 1}},
                {"text": "Серый", "weights": {"Волк": 3, "Носорог": 2, "Слон": 2, "Крокодил": 1, "Африканская мышь": 2}}
            ]
        },

        {
            "question": "Какую еду предпочитаешь?",
            "options": [
                {"text": "Мясо", "weights": {"Лев": 3, "Тигр": 3, "Леопард": 3, "Крокодил": 3, "Волк": 3}},
                {"text": "Овощи", "weights": {"Слон": 1, "Коала": 2, "Африканская мышь": 1, "Носорог": 3, "Павлин": 1}},
                {"text": "Фрукты", "weights": {"Панда": 1, "Кенгуру": 2, "Лошадь": 3, "Шиншилла": 1, "Сурикат": 1}},
                {"text": "Рыбу", "weights": {"Аист": 3, "Медведь": 1, "Фламинго": 2, "Павлин": 1, "Рысь": 1}},
                {"text": "Ягоды", "weights": {"Соболь": 1, "Песец": 1, "Ласка": 1, "Лиса": 2, "Динго": 2}}
            ]
        },

        {
            "question": "Какое животное в Московском зоопарке прожило дольше всего?",
            "options": [
                {"text": "Слон", "weights": {"Слон": 3, "Лев": 2, "Лошадь": 1, "Носорог": 1, "Крокодил": 2}},
                {"text": "Панда", "weights": {"Панда": 2, "Коала": 2, "Аист": 2, "Африканская мышь": 1, "Павлин": 1}},
                {"text": "Медведь", "weights": {"Медведь": 2, "Шиншилла": 1, "Рысь": 2, "Тигр": 2, "Лиса": 2}},
                {"text": "Леопард", "weights": {"Леопард": 2, "Динго": 2, "Волк": 2, "Сурикат": 2, "Пингвин": 2}},
                {"text": "Павлин", "weights": {"Соболь": 3, "Песец": 2, "Ласка": 2, "Фламинго": 1, "Кенгуру": 2}}
            ]
        },

        {
            "question": "Как называется единственный вид пингвинов, который обитает в Московском зоопарке?",
            "options": [
                {"text": "Императорский пингвин", "weights": {"Пингвин": 2, "Аист": 1, "Лошадь": 1, "Носорог": 2, "Крокодил": 3}},
                {"text": "Гумбольдтов пингвин", "weights": {"Панда": 1, "Коала": 2, "Песец": 2, "Африканская мышь": 3, "Павлин": 2}},
                {"text": "Королевский пингвин", "weights": {"Медведь": 1, "Слон": 1, "Рысь": 3, "Шиншилла": 3, "Ласка": 2}},
                {"text": "Аделиев пингвин", "weights": {"Леопард": 2, "Фламинго": 1, "Волк": 1, "Сурикат": 2, "Лиса": 2}},
                {"text": "Жентушки", "weights": {"Лев": 2, "Соболь": 2, "Кенгуру": 2, "Тигр": 1, "Динго": 1}}
            ]
        },

        {
            "question": "Как называются павильоны в Московском зоопарке, где можно увидеть экзотических птиц?",
            "options": [
                {"text": "Орнитологический комплекс", "weights": {"Пингвин": 1, "Аист": 2, "Лошадь": 3, "Носорог": 2, "Крокодил": 2}},
                {"text": "Птичий дом", "weights": {"Панда": 2, "Коала": 2, "Слон": 1, "Африканская мышь": 1, "Павлин": 1}},
                {"text": "Птичий рай", "weights": {"Медведь": 1, "Лев": 1, "Рысь": 3, "Шиншилла": 2, "Динго": 2}},
                {"text": "Орнитологический рай", "weights": {"Леопард": 1, "Сурикат": 2, "Соболь": 3, "Тигр": 2, "Лиса": 2}},
                {"text": "Орнитарий", "weights": {"Песец": 3, "Ласка": 2, "Фламинго": 3, "Кенгуру": 1, "Волк": 1}}
            ]
        },

        {
            "question": "Какое животное было символом Московского зоопарка в 90-ые годы?",
            "options": [
                {"text": "Панда", "weights": {"Панда": 2, "Аист": 1, "Лошадь": 1, "Носорог": 2, "Рысь": 2}},
                {"text": "Тигр", "weights": {"Тигр": 2, "Пингвин": 1, "Ласка": 2, "Лиса": 1, "Леопард": 2}},
                {"text": "Слон", "weights": {"Слон": 3, "Коала": 2, "Песец": 1, "Волк": 3, "Крокодил": 2}},
                {"text": "Лев", "weights": {"Лев": 3, "Медведь": 2, "Кенгуру": 3, "Павлин": 2, "Соболь": 1}},
                {"text": "Заяц", "weights": {"Сурикат": 2, "Шиншилла": 2, "Фламинго": 1, "Африканская мышь": 2, "Динго": 1}}
            ]
        },

        {
            "question": "Какой вид обезьян в Московском зоопарке наиболее многочисленный?",
            "options": [
                {"text": "Бонобо", "weights": {"Пингвин": 2, "Аист": 3, "Кенгуру": 1, "Медведь": 1, "Крокодил": 2}},
                {"text": "Шимпанзе", "weights": {"Лев": 2, "Коала": 1, "Сурикат": 1, "Африканская мышь": 2, "Павлин": 2}},
                {"text": "Гориллы", "weights": {"Панда": 1, "Тигр": 2, "Рысь": 1, "Шиншилла": 3, "Носорог": 3}},
                {"text": "Орангутанги", "weights": {"Леопард": 1, "Лошадь": 1, "Волк": 2, "Слон": 2, "Лиса": 2}},
                {"text": "Макаки", "weights": {"Соболь": 2, "Песец": 2, "Ласка": 3, "Фламинго": 2, "Динго": 2}}
            ]
        },

        {
            "question": "Какой зверь является символом Московского зоопарка сегодня?",
            "options": [
                {"text": "Белый медведь", "weights": {"Медведь": 3, "Крокодил": 1, "Ласка": 1, "Волк": 1, "Панда": 2}},
                {"text": "Тигр", "weights": {"Тигр": 3, "Рысь": 2, "Леопард": 2, "Африканская мышь": 1, "Динго": 2}},
                {"text": "Панда", "weights": {"Песец": 1, "Коала": 1, "Носорог": 1, "Шиншилла": 1, "Соболь": 2}},
                {"text": "Лев", "weights": {"Лев": 2, "Лошадь": 2, "Лиса": 2, "Сурикат": 3, "Павлин": 2}},
                {"text": "Волк", "weights": {"Слон": 2, "Кенгуру": 2, "Пингвин": 3, "Аист": 2, "Фламинго": 2}}
            ]
        },

        {
            "question": "В каком году был открыт Московский зоопарк?",
            "options": [
                {"text": "1857", "weights": {"Пингвин": 2, "Аист": 1, "Лошадь": 2, "Носорог": 3, "Крокодил": 2}},
                {"text": "1864", "weights": {"Панда": 1, "Коала": 2, "Фламинго": 1, "Волк": 2, "Павлин": 2}},
                {"text": "1900", "weights": {"Медведь": 2, "Слон": 1, "Рысь": 2, "Леопард": 1, "Кенгуру": 2}},
                {"text": "1910", "weights": {"Динго": 3, "Тигр": 1, "Африканская мышь": 3, "Сурикат": 2, "Лиса": 3}},
                {"text": "1920", "weights": {"Лев": 1, "Соболь": 2, "Шиншилла": 1, "Песец": 3, "Ласка": 1}}
            ]
        },

        {
            "question": "Какое животное в Московском зоопарке имеет свой 'день рождения', который отмечается ежегодно?",
            "options": [
                {"text": "Слон", "weights": {"Слон": 3, "Носорог": 2, "Лошадь": 2, "Кенгуру": 2, "Динго": 1}},
                {"text": "Панда", "weights": {"Панда": 3, "Шиншилла": 2, "Аист": 3, "Медведь": 3, "Пингвин": 1}},
                {"text": "Медведь", "weights": {"Волк": 1, "Коала": 3, "Павлин": 2, "Ласка": 1, "Соболь": 1}},
                {"text": "Лев", "weights": {"Лев": 1, "Африканская мышь": 1, "Крокодил": 1, "Сурикат": 1, "Песец": 1}},
                {"text": "Тигр", "weights": {"Тигр": 2, "Фламинго": 2, "Леопард": 3, "Рысь": 3, "Лиса": 1}}
            ]
        },

        {
            "question": "Как называется главный 'аквариум' Московского зоопарка?",
            "options": [
                {"text": "Морской дом", "weights": {"Пингвин": 2, "Медведь": 2, "Сурикат": 3, "Носорог": 1, "Панда": 1}},
                {"text": "Океанариум", "weights": {"Фламинго": 1, "Павлин": 3, "Аист": 2, "Африканская мышь": 2, "Крокодил": 3}},
                {"text": "Аквадом", "weights": {"Коала": 2, "Лиса": 2, "Рысь": 1, "Шиншилла": 1, "Лошадь": 2}},
                {"text": "Морской мир", "weights": {"Леопард": 1, "Динго": 2, "Волк": 3, "Слон": 1, "Кенгуру": 1}},
                {"text": "Акваленд", "weights": {"Лев": 3, "Соболь": 2, "Тигр": 1, "Песец": 2, "Ласка": 2}}
            ]
        },

        {
            "question": "Почему слон не играет в карты с зеброй?",
            "options": [
                {"text": "Зебра всегда 'перебивает' его", "weights": {"Аист": 1, "Лошадь": 3, "Носорог": 2, "Крокодил": 1, "Слон": 2}},
                {"text": "Слон не умеет хорошо играть", "weights": {"Коала": 1, "Тигр": 2, "Лиса": 1, "Павлин": 1, "Шиншилла": 3}},
                {"text": "Слон боится, что зебра 'вскочит' на стол ", "weights": {"Волк": 2, "Рысь": 2, "Африканская мышь": 3, "Медведь": 1, "Соболь": 2}},
                {"text": "Зебра всегда 'растягивает' игру", "weights": {"Леопард": 2, "Лев": 2, "Сурикат": 2, "Панда": 2, "Пингвин": 1}},
                {"text": "Слон не может 'прятать карты'", "weights": {"Песец": 2, "Волк": 2, "Ласка": 2, "Фламинго": 3, "Динго": 1}}
            ]
        },

        {
            "question": "Как зовут самого музыкального попугая на свете?",
            "options": [
                {"text": "Бетховен", "weights": {"Слон": 1, "Коала": 2, "Динго": 3, "Пингвин": 3, "Кенгуру": 1}},
                {"text": "Чайковский", "weights": {"Рысь": 2, "Аист": 2, "Африканская мышь": 2, "Павлин": 2, "Шиншилла": 2}},
                {"text": "Моцарт", "weights": {"Ласка": 3, "Фламинго": 2, "Крокодил": 2, "Носорог": 1, "Соболь": 1}},
                {"text": "Шопен", "weights": {"Медведь": 2, "Волк": 1, "Сурикат": 1, "Лиса": 1, "Панда": 2}},
                {"text": "Римский-Корсаков", "weights": {"Лев": 1, "Лошадь": 2, "Тигр": 1, "Песец": 3, "Леопард": 3}}
            ]
        },

        {
            "question": "Как называется самая модная обезьяна в зоопарке?",
            "options": [
                {"text": "Шимпан-гламур", "weights": {"Пингвин": 2, "Лошадь": 1, "Носорог": 1, "Крокодил": 1, "Слон": 3}},
                {"text": "Макак-стиль", "weights": {"Панда": 2, "Коала": 1, "Аист": 1, "Павлин": 3, "Шиншилла": 2}},
                {"text": "Горилла-тренд", "weights": {"Лиса": 2, "Рысь": 1, "Леопард": 2, "Африканская мышь": 2, "Соболь": 3}},
                {"text": "Орангутанг-чик", "weights": {"Медведь": 2, "Лев": 2, "Сурикат": 3, "Тигр": 2, "Волк": 1}},
                {"text": "Бонобо-мода", "weights": {"Песец": 1, "Фламинго": 3, "Ласка": 1, "Динго": 1, "Кенгуру": 3}}
            ]
        },
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
        "Рысь": {"text": "Вы энергичны, быстры в принятии решений и всегда готовы к новым приключениям.", "image_url": "img/1.jpeg"},
        "Медведь": {"text": "Вы сильны, мудры и защищаете своих близких. Вас привлекает спокойная и уединенная обстановка.", "image_url": "img/2.jpeg"},
        "Панда": {"text": "Вы спокойны, милы и миролюбивы. Вас привлекает обилие еды и уютная обстановка.", "image_url": "img/3.jpeg"},
        "Лев": {"text": "Вы смелы, лидер по своей натуре и всегда готовы защищать свою территорию.", "image_url": "img/4.jpeg"},
        "Коала": {"text": "Вы спокойны, ленивы и предпочитаете проводить время на деревьях.", "image_url": "img/5.jpeg"},
        "Волк": {"text": "Вы умны, сообразительны и предпочитаете работать в команде. Вас привлекают сложные задачи.", "image_url": "img/6.jpeg"},
        "Шиншилла": {"text": "Вы обожаете чистоту, активны и общительны. Вас привлекает мода и стиль.", "image_url": "img/7.jpeg"},
        "Африканская мышь": {"text": "Вы творческая личность, независимы и интуитивны. Вас привлекает загадочность и загадки.", "image_url": "img/8.jpeg"},
        "Пингвин": {"text": "Вы общительны, дружелюбны и имеете чувство юмора. Вас привлекает море и путешествия.", "image_url": "img/9.jpeg"},
        "Сурикат": {"text": "Вы отзывчивы, заботливы и всегда готовы помочь другим. Вас привлекает семейная обстановка и теплые отношения.", "image_url": "img/10.jpeg"},
        "Лиса": {"text": "Вы хитры, умны и обладаете тонким чувством интуиции. Вас привлекает загадочность и приключения.", "image_url": "img/11.jpeg"},
        "Тигр": {"text": "Вы амбициозны, сильны и целеустремленны. Вас привлекает динамичная и активная жизнь.", "image_url": "img/12.jpeg"},
        "Лошадь": {"text": "Вы энергичны, грациозны и обладаете высокой степенью самодисциплины. Вас привлекает свобода и приключения.", "image_url": "img/13.jpeg"},
        "Леопард": {"text": "Вы грациозны, хитры и обладаете сильным чувством независимости. Вас привлекает загадочность и скорость.", "image_url": "img/14.jpeg"},
        "Носорог": {"text": "Вы упрямы, сильны и надежны. Вас привлекает спокойствие и стабильность.", "image_url": "img/15.jpeg"},
        "Слон": {"text": "Вы мудры, добры и ответственны. Вас привлекает семейные ценности и гармония.", "image_url": "img/16.jpeg"},
        "Аист": {"text": "Вы обладаете высоким уровнем интеллекта, легки в общении и дружелюбны. Вас привлекает путешествия и новые открытия.", "image_url": "img/17.jpeg"},
        "Крокодил": {"text": "Вы упорны, терпеливы и обладаете сильным характером. Вас привлекает мудрость и долговечность.", "image_url": "img/18.jpeg"},
        "Павлин": {"text": "Вы ярки, креативны и обожаете привлекать внимание. Вас привлекает красота и изысканность.", "image_url": "img/19.jpeg"},
        "Соболь": {"text": "Вы настойчивы, целеустремленны и обладаете тонким вкусом. Вас привлекает комфорт и стиль.", "image_url": "img/20.jpeg"},
        "Песец": {"text": "Вы хитры, обладаете острым умом и чувством юмора. Вам нравится разгадывать загадки и приключения.", "image_url": "img/21.jpeg"},
        "Ласка": {"text": "Вы ласковы, заботливы и всегда готовы поддержать близких.Вас привлекает теплая обстановка и уютный дом.", "image_url": "img/22.jpeg"},
        "Фламинго": {"text": "Вы экстравагантны, ярки и обожаете выделяться среди других. Вас привлекает красота природы и изящество.", "image_url": "img/23.jpeg"},
        "Кенгуру": {"text": "Вы энергичны, имеете высокий уровень адаптивности и любите новые вызовы. Вам нравится свобода движения и активный образ жизни.", "image_url": "img/24.jpeg"},
        "Динго": {"text": "Вы независимы, загадочны и имеете сильную интуицию. Вас привлекает тайна прошлого и необычные путешествия.", "image_url": "img/25.jpeg"},
    }

    for animal_name, result_data in results.items():
        result_text = result_data["text"]
        image_url = result_data["image_url"]
        cur.execute("INSERT INTO results (animal_name, result_text, image_url) VALUES (%s, %s, %s)",
                    (animal_name, result_text, image_url))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
