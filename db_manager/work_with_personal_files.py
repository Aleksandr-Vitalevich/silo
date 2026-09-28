import sqlite3
from db_manager.db_config import DB_PATH
from utils.logger import db_logger
from utils.retry import retry_on_lock
from utils.input_cleaner import clean_inputs
from db_manager.create_table_db import create_table

create_table()
@db_logger
@retry_on_lock
@clean_inputs
def add_file(file_name : str,file_bytes : bytes,db_path = DB_PATH) :
    '''Функция добавляет файлы в базу данных'''
    try :
        with sqlite3.Connection(db_path) as connection :
            cursor = connection.cursor()
            query_value = (file_name,file_bytes)
            query_add = 'INSERT OR IGNORE INTO user_files (file_name,file_content) VALUES (?,?)' 
            cursor.execute(query_add,query_value)
            connection.commit()
        return "success"
    except sqlite3.Error as e :
        raise e

@db_logger
@retry_on_lock
def delete_file(id : int,db_path = DB_PATH) :
    '''Функция удаляет файлы из базы данных'''
    try :
        with sqlite3.Connection(db_path) as connection :
            cursor = connection.cursor()
            query_value = (id,)
            query_delete = 'DELETE FROM user_files WHERE id = ?'
            cursor.execute(query_delete,query_value)
            connection.commit()
        return "success"
    except sqlite3.Error as e :
        raise e

@db_logger
@retry_on_lock
def get_all_files(db_path = DB_PATH) :
    '''Функция возвращает файлы из базы данных'''
    try :
        with sqlite3.Connection(db_path) as connection :
            cursor = connection.cursor()
            query_show = 'SELECT id , file_name, uploaded_at FROM user_files ORDER BY uploaded_at DESC'
            cursor.execute(query_show)
            res = cursor.fetchall()
        return res if res else []
    except sqlite3.Error as e :
        raise e

@db_logger
@retry_on_lock
def get_file(id : int, db_path = DB_PATH) :
    '''Функция возвращает файл по id'''
    try :
        with sqlite3.Connection(db_path) as connection :
            cursor = connection.cursor()
            query_value = (id,)
            query_show = 'SELECT file_name, file_content FROM user_files WHERE id = ?'
            cursor.execute(query_show,query_value)
            res = cursor.fetchone()
        return res if res else []
    except Exception as e :
        raise e