import pytest
import os
from db_manager.create_table_db import create_table
from db_manager.work_with_personal_safe import add_data,delete_data,show_data,update_data,get_data_by_id

def test_work_with_operation_calendar():
    '''Тест проверки модуля календаря'''
    test_path = "test_records_temporary.db"
    args = {
    "name_service" : "Git",
    "login_service" : "Aleks",
    "password_service" : "password"
    }
    args2 = {
    "name_service" : "Yandex",
    "login_service" : "Aleks",
    "password_service": "password"
    }
    args_update = {
        "name_service" : "Github"
    }
    try :
        create_table(test_path)

        res_add = add_data(args,test_path)
        res_add1 = add_data(args2,test_path)
        assert res_add == "success"
        assert res_add1 == "success"
        
        res_show = show_data(test_path)
        assert len(res_show) >= 1 
        task_id = res_show[0][0]

        res_update = update_data(task_id,args_update,test_path)
        assert res_update == "success"

        res_get = get_data_by_id(task_id,test_path)
        assert res_get != ()

        res_delete = delete_data(task_id,test_path)
        assert res_delete == "success"

        res_show = show_data(test_path)
        assert len(res_show) == 1 

    finally :
        if os.path.exists(test_path) :
            os.remove(test_path)