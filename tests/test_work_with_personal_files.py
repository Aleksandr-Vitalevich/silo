import pytest
import os
from db_manager.create_table_db import create_table
from db_manager.work_with_personal_files import add_file,delete_file,get_all_files,get_file

def test_work_with_operation_files():
    '''Тест проверки модуля работы с файлами'''
    test_path = "test_records_temporary.db"
    test_name = "Тест.pdf"
    test_text = b"Hello test text"
    try :
        create_table(test_path)
        res_add1 = add_file(test_name,test_text,test_path)
        assert res_add1 == "success"

        res_show = get_all_files(test_path)
        assert len(res_show) >=1
        task_id1 = res_show[0][0]

        res_show_user = get_file(task_id1,test_path)
        assert len(res_show_user) == 2

        res_delete = delete_file(task_id1,test_path)
        assert res_delete == "success"

        res_show = get_all_files(test_path)
        assert len(res_show) == 0

    finally :
        if os.path.exists(test_path) :
            os.remove(test_path)