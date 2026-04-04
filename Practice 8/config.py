# config.py
def get_config():
    return {
        "dbname": "Phonebook",      # ← измени, если у тебя другое название базы
        "user": "postgres",         # ← твой пользователь
        "password": "1234",     # ← твой пароль (скорее всего)
        "host": "localhost",
        "port": "5432"
    }