from config import DB_CONFIG

def connect():
    print(DB_CONFIG)   # ← сюда
    import psycopg2
    return psycopg2.connect(**DB_CONFIG)