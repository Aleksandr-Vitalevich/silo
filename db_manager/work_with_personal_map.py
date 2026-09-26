import sqlite3
from db_manager.db_config import DB_PATH
from utils.logger import db_logger
from utils.retry import retry_on_lock
from utils.input_cleaner import clean_inputs
from db_manager.create_table_db import create_table

create_table()

@db_logger
@retry_on_lock
def get_all_points(db_path=DB_PATH) :
    '''Функция возвращает все записи с карты'''
    try :
        with sqlite3.connect(db_path) as connection :
            cursor = connection.cursor()
            requests_get = '''SELECT * FROM map_tasks ORDER BY created_at DESC'''
            cursor.execute(requests_get)
            res = cursor.fetchall()
        return res
    except Exception as e :
        raise e

@db_logger
@retry_on_lock
@clean_inputs
def add_new_point(args,db_path=DB_PATH) :
    '''Функция добавления новой заметки на карту'''
    try :
        with sqlite3.connect(db_path) as connection :
            cursor = connection.cursor()
            get_values_place = ', '.join(['?'] * len(args))
            get_placeholders = ', '.join(args)
            get_values = tuple(args.values())
            add_query = f"INSERT OR IGNORE INTO map_tasks ({get_placeholders}) VALUES ({get_values_place}) "
            cursor.execute(add_query,get_values)
        return "success"
    except sqlite3.Error as e :
        raise e

@db_logger
@retry_on_lock
def delete_point(id,db_path=DB_PATH) :
    '''Функция удаления заметки из карты'''
    try :
        with sqlite3.connect(db_path) as connection :
            cursor = connection.cursor()
            delete_query = '''DELETE FROM map_tasks WHERE id = ?'''
            delete_value = (id,)
            cursor.execute(delete_query,delete_value)
        return "success"
    except sqlite3.Error as e :
        raise e

@db_logger
@retry_on_lock
@clean_inputs
def update_point(id,args,db_path=DB_PATH) :
    '''Функция обновления заметки на карте'''
    try :
        with sqlite3.connect(db_path) as connection :
            cursor = connection.cursor()
            get_values_place = ', '.join(['?'] * len(args))
            get_placeholders = ', '.join(args)
            get_values = tuple(args.values())
            sum_values = get_values + (id,)
            update_query = f"UPDATE map_tasks SET ({get_placeholders}) = ({get_values_place}) WHERE id = ?"
            cursor.execute(update_query,sum_values)
        return "success"
    except sqlite3.Error as e :
         raise e