import streamlit as st

def main_diary_interface():
    '''Функция отвечает за логику управления меню дневника'''
    tab1,tab2 = st.tabs(["Дневник","Управление дневником"])

    with tab1 :
        from view.diary.diary_tab1_interface import operation_tab1
        operation_tab1()

    with tab2 :
        from view.diary.diary_tab2_interface import operation_tab2
        operation_tab2()