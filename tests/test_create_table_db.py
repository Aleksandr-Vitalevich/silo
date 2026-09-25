import pytest
import sqlite3
import os
from db_manager.create_table_db import create_table

def test_create_table():
    '''Тест проверет создание базы данных'''
    test_path = "test_silo_temporary.db"
    try :
        res = create_table(test_path)
        assert res is True

        with sqlite3.connect(test_path) as connection :
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
            tables = [row[0] for row in cursor.fetchall()]
            assert "user" in tables
            assert "personal_safe" in tables
            assert "personal_diary" in tables
            assert "calendar_tasks" in tables
    finally :
        if os.path.exists(test_path):
            os.remove(test_path)
