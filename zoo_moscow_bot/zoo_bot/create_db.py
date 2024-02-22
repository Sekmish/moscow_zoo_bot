import psycopg2

def create_tables():
    conn = psycopg2.connect(database="m_zoo", user="pan", password="bd!!<FPF22lfyys[33", host="127.0.0.1", port="5432")
    cursor = conn.cursor()

    # Создание таблицы questions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            question_text TEXT
        )
    """)

    # Создание таблицы options
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS options (
            id SERIAL PRIMARY KEY,
            question_id INT REFERENCES questions(id),
            option_text TEXT,
            weight INT
        )
    """)

    # Создание таблицы results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id SERIAL PRIMARY KEY,
            animal_name TEXT,
            result_text TEXT
        )
    """)

    conn.commit()
    conn.close()

# Вызов функции для создания таблиц
create_tables()
