import streamlit as st

def main_files_interface():
    '''Функция отвечает за логику управления меню мои файлы'''
    tab1,tab2 = st.tabs(["Загрузка файла","Управление файлами"])

    with tab1 :
        from view.files.files_tab1_interface import operation_tab1
        operation_tab1()

    with tab2 :
        from view.files.files_tab2_interface import operation_tab2
        operation_tab2()