import pytest
import os
from db_manager.create_table_db import create_table
from db_manager.work_with_personal_map import get_all_points,add_new_point,delete_point,update_point

def test_work_with_operation_map() :
    '''Тест проверки модуля карт'''
    test_path = "test_records_temporary.db"
    args = {
        "title" : "Meet",
        "description" : "meet with friend",
        }
    args2 = {
        "title" : "Work",
        "description" : "working adress",
        }
    args_update = {
        "title" : "Github"
        }
    try :
        create_table(test_path)
    
        res_add = add_new_point(args,test_path)
        res_add1 = add_new_point(args2,test_path)
        assert res_add == "success"
        assert res_add1 == "success"
            
        res_show = get_all_points(test_path)
        assert len(res_show) >= 1 
        task_id = res_show[0][0]
    
        res_update = update_point(task_id,args_update,test_path)
        assert res_update == "success"
    
        res_show = get_all_points(test_path)
        assert res_show != ()
    
        res_delete = delete_point(task_id,test_path)
        assert res_delete == "success"
    
        res_show = get_all_points(test_path)
        assert len(res_show) == 1 
    
    finally :
        if os.path.exists(test_path) :
            os.remove(test_path)