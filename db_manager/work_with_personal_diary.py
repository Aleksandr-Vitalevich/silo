import sqlite3
from db_manager.db_config import DB_PATH
from utils.logger import db_logger
from utils.retry import retry_on_lock

@db_logger
@retry_on_lock
def add_data_to_diary(text) :
    '''Функция принимает текст и записывает их в базу'''
    try :
        with sqlite3.connect(DB_PATH) as connection :
            cursor = connection.cursor()
            value = (text,)
            add_query = f"INSERT OR IGNORE INTO personal_diary (text_diary) VALUES (?) "
            cursor.execute(add_query,value)
        return "success"
    except sqlite3.Error as e :
        raise e

@db_logger
@retry_on_lock
def delete_data_to_diary(id) :
    '''Функция принимает id записи и проводит удаление записи'''
    try :
        with sqlite3.connect(DB_PATH) as connection :
            cursor = connection.cursor()
            delete_query = "DELETE FROM personal_diary WHERE id = ?"
            delete_value = (id,)
            cursor.execute(delete_query,delete_value)
        return "success"
    except sqlite3.Error as e :
            raise e
    

@db_logger
@retry_on_lock
def show_data_to_diary() :
    '''Функция возвращает все записи из базы'''
    try :
        with sqlite3.connect(DB_PATH) as connection :
            cursor = connection.cursor()
            show_query = "SELECT * FROM personal_diary ORDER BY created_at DESC"
            cursor.execute(show_query)
            res = cursor.fetchall()
        return res
    except sqlite3.Error as e :
            raise e


@db_logger
@retry_on_lock
def show_data_to_diary_user_choise(number) :
    '''Функция возвращает записи из базы количество записей выбирает пользователь'''
    try :
        with sqlite3.connect(DB_PATH) as connection :
            cursor = connection.cursor()
            show_query = "SELECT text_diary FROM personal_diary ORDER BY created_at DESC LIMIT ?"
            cursor.execute(show_query,(number,))
            res = cursor.fetchall()
        return res if res else []
    except sqlite3.Error as e :
            raise e