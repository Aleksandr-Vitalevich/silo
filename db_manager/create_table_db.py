import sqlite3
from db_manager.db_config import DB_PATH
from utils.logger import db_logger
from utils.retry import retry_on_lock

@db_logger
@retry_on_lock
def create_table(db_path=DB_PATH) :
    '''Функция создания базы данных'''
    try :
        with sqlite3.connect(db_path) as connection :
                cursor = connection.cursor()
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_login TEXT NOT NULL,
                        user_password TEXT NOT NULL)
                ''')
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS personal_safe (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_service TEXT NOT NULL UNIQUE,
                        login_service TEXT,
                        password_service TEXT,
                        site_service TEXT,
                        token_service TEXT,
                        other_need_information_service TEXT
                        )
                ''')
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS personal_diary (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text_diary TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                ''')
                cursor.execute('''
                        CREATE TABLE IF NOT EXISTS calendar_tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_date TEXT NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        is_completed INTEGER DEFAULT 0,
                        priority TEXT DEFAULT "Medium",
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                ''')
                return True
    except sqlite3.Error as e :
        raise e

        

