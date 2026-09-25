import pytest
import os
import sqlite3
from db_manager.work_with_add_user import add_user,check_user_in_db,check_user_authorization
from db_manager.create_table_db import create_table

def test_work_with_operation_user():
    '''Тест проверки модуля работы с пользователем'''
    test_path = "test_records_temporary.db"
    user_login = "Aleks"
    user_password = "456"
    try :
        create_table(test_path)
        res_test_add = add_user(user_login,user_password,test_path)
        assert res_test_add is "success"
        res_check_user = check_user_in_db(test_path)
        assert res_check_user is True
        res_check_auth = check_user_authorization(user_login,user_password,test_path)
        assert res_check_auth is True
    finally :
        if os.path.exists(test_path) :
            os.remove(test_path)