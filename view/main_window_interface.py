from view.tab1_interface import operation_tab1
from view.tab2_interface import operation_tab2
from view.tab3_interface import operation_tab3
from view.tab4_interface import operation_tab4
from view.tab0_interface import operation_tab0
from view.tab5_interface import operation_tab5
import streamlit as st


def main_interface() :
    '''Основная функция управления интерфейсом'''
    st.title("Silo")
    st.write("---")
        
    tab0,tab1,tab2,tab3,tab4,tab5 = st.tabs(["Выход",
                                             "Данные",
                                             "Дневник",
                                             "Управление данными",
                                             "Управление дневником",
                                             "Ассистент Silo"])

    with tab0 :
        operation_tab0()

    with tab1 :
        operation_tab1()

    with tab2 :
        operation_tab2()

    with tab3 :
        operation_tab3()

    with tab4 :
        operation_tab4()

    with tab5 :
        operation_tab5()

