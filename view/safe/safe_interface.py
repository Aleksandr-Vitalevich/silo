import streamlit as st

def main_safe_interface() :
    '''Функция отвечает за логику управления меню сейфа с данными'''
    tab1,tab2 = st.tabs(["Запись данных","Управление данными"])

    with tab1 :
        from view.safe.safe_tab1_interface import operation_tab1
        operation_tab1()
    with tab2 :
        from view.safe.safe_tab2_interface import operation_tab2
        operation_tab2()