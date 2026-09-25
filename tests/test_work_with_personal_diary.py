import pytest
import os
from db_manager.create_table_db import create_table
from db_manager.work_with_personal_diary import add_data_to_diary,delete_data_to_diary,show_data_to_diary,show_data_to_diary_user_choise

def test_work_with_operation_diary():
    '''Тест проверки модуля дневника'''
    test_path = "test_records_temporary.db"
    test_text = "Тест"
    try :
        create_table(test_path)
        res_add1 = add_data_to_diary(test_text,test_path)
        assert res_add1 == "success"
        res_add2 = add_data_to_diary(test_text,test_path)
        assert res_add2 == "success"

        res_show = show_data_to_diary(test_path)
        assert len(res_show) >=1
        task_id1 = res_show[0][0]
        task_id2 = res_show[1][0]

        res_show_user = show_data_to_diary_user_choise(1,test_path)
        assert len(res_show_user) == 1

        res_delete = delete_data_to_diary(task_id2,test_path)
        assert res_delete == "success"

        res_show = show_data_to_diary(test_path)
        assert len(res_show) ==1

    finally :
        if os.path.exists(test_path) :
            os.remove(test_path)