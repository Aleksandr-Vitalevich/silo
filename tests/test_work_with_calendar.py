import pytest
import os
from datetime import datetime
from db_manager.create_table_db import create_table
from db_manager.work_with_calendar import add_calendar_task,get_calandar_tasks_by_date,update_task_status,delete_data_to_calendar

def test_work_with_operation_calendar():
    '''Тест проверки модуля календаря'''
    test_path = "test_records_temporary.db"
    test_date = datetime.now().strftime("%Y-%m-%d")
    test_title = "Тест"
    test_description = "Тест функций"
    test_priority = "Low"
    try :
        create_table(test_path)
        res_add = add_calendar_task(test_date,test_title,test_description,test_priority,test_path)
        assert res_add == "success"

        res_get_tasks = get_calandar_tasks_by_date(test_date,test_path)
        assert len(res_get_tasks) >= 1
        task_id = res_get_tasks[0][0]

        res_update_status = update_task_status(task_id,1,test_path)
        # Первый параметр id второй параметр 0 или 1 обозначают нажатие или нет галочки 
        assert res_update_status == "success"

        res_delete = delete_data_to_calendar(task_id,test_path)
        assert res_delete == "success"

    finally :
        if os.path.exists(test_path) :
            os.remove(test_path)