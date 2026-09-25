import sqlite3
from pathlib import Path
from db_manager.db_config import DB_PATH
from utils.logger import db_logger
from utils.retry import retry_on_lock
from utils.input_cleaner import clean_inputs
from db_manager.create_table_db import create_table

create_table()

@db_logger
@retry_on_lock
@clean_inputs
def add_calendar_task(task_date : str,title : str,description : str, priority : str,db_path=DB_PATH) -> str:
    '''Функция принимает 5 параметров и добавляет запись в бд'''
    try :
        with sqlite3.connect(db_path) as connection :
            cursor = connection.cursor()
            query_add = f'''INSERT OR IGNORE INTO calendar_tasks(
                        task_date,title,description,priority
                        ) 
                        VALUES (?,?,?,?)
                        '''
            values_add = (task_date,title,description,priority)
            cursor.execute(query_add,values_add)
        return "success"
    except sqlite3.Error as e:
        raise e

@db_logger
@retry_on_lock
def get_calandar_tasks_by_date(task_date : str,db_path=DB_PATH) -> tuple:
    '''Функция возвращает список задач на выбранную дату'''
    try :
        with sqlite3.connect(db_path) as connection :
            cursor = connection.cursor()
            get_tasks = f'''SELECT 
                        id,title,description,is_completed,priority
                        FROM
                        calendar_tasks
                        WHERE 
                        task_date = ?
                        ORDER BY 
                        id DESC
                        '''
            get_values = (task_date,)
            cursor.execute(get_tasks,get_values)
            res = cursor.fetchall()
        return res
    except Exception as e :
        raise e

@db_logger
@retry_on_lock
def update_task_status(task_id,is_completed,db_path=DB_PATH) -> str:
    '''Функция изменяет статус выбранной задачи'''
    try :
        with sqlite3.connect(db_path) as connection :
            cursor = connection.cursor()
            update_task = f'''UPDATE
                        calendar_tasks 
                        SET
                        is_completed = ?
                        WHERE 
                        id = ?
            '''
            values_update = (is_completed,task_id)
            cursor.execute(update_task,values_update)
        return "success"
    except sqlite3.Error as e:
        raise e


@db_logger
@retry_on_lock
def delete_data_to_calendar(id,db_path=DB_PATH) :
    '''Функция принимает id записи и проводит удаление записи'''
    try :
        with sqlite3.connect(db_path) as connection :
            cursor = connection.cursor()
            delete_query = "DELETE FROM calendar_tasks WHERE id = ?"
            delete_value = (id,)
            cursor.execute(delete_query,delete_value)
        return "success"
    except sqlite3.Error as e :
            raise e