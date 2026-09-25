import sqlite3
from pathlib import Path
from utils import check_password,hash_password
from db_manager.db_config import DB_PATH
from utils.logger import db_logger
from utils.retry import retry_on_lock
from utils.input_cleaner import clean_inputs

@db_logger
@retry_on_lock
@clean_inputs
def add_user(login,password,db_path=DB_PATH) :
        '''Функция принимает два параметра логин и пароль и создает запись в бд'''
        try :
            with sqlite3.connect(db_path) as connection :
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM user")
                if cursor.fetchone()[0] >= 1:
                    return "forbidden"
                hash_password_user = hash_password(password)
                values = (login,hash_password_user)
                add_query = f"INSERT OR IGNORE INTO user (user_login,user_password) VALUES (?, ?) "
                cursor.execute(add_query,values)
                return "success"
        except sqlite3.Error as e:
                raise e

@db_logger
@retry_on_lock
@clean_inputs
def check_user_in_db(db_path=DB_PATH) :
        '''Функция проверяет наличие пользователя в базе данных'''
        try :
            with sqlite3.connect(db_path) as connection :
                cursor = connection.cursor()
                check_query = 'SELECT COUNT(*) FROM user'
                cursor.execute(check_query)
                res = cursor.fetchone()[0]
                return True if res > 0 else False
        except sqlite3.Error as e:
                raise e

@db_logger
@retry_on_lock
@clean_inputs
def check_user_authorization(login,password,db_path=DB_PATH) :
        '''Функция принимает логин и пароль'''
        try :
            with sqlite3.connect(db_path) as connection :
                    cursor = connection.cursor()
                    get_user_password = "SELECT user_password FROM user WHERE user_login = ?"
                    values_login = (login,)
                    cursor.execute(get_user_password,values_login)
                    res = cursor.fetchone()
                    if not res :
                        return False
                    elif res :
                        check_password_user = check_password(password,res[0])
                        if check_password_user :
                               return True
                        else : 
                               return False
        except sqlite3.Error as e:
                raise e
                