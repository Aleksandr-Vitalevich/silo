import streamlit as st

def main_interface() :
    '''Основная функция управления интерфейсом'''
    with st.sidebar :
        st.title("Silo")
        st.markdown("---")
    
        user_choice = st.radio("Выбор Меню",["Выход",
                                             "Данные",
                                             "Дневник",
                                             "Управление данными",
                                             "Управление дневником",
                                             "Ассистент Silo",
                                             "Календарь и Заметки"],
                                index=1)
        st.markdown("---")
    

    if user_choice == "Выход" :
        from view.tab0_interface import operation_tab0
        operation_tab0()

    elif user_choice == "Данные":
        from view.tab1_interface import operation_tab1
        operation_tab1()

    elif user_choice == "Дневник":
        from view.tab2_interface import operation_tab2
        operation_tab2()

    elif user_choice == "Управление данными":
        from view.tab3_interface import operation_tab3
        operation_tab3()

    elif user_choice == "Управление дневником":
        from view.tab4_interface import operation_tab4
        operation_tab4()

    elif user_choice == "Ассистент Silo":
        from view.tab5_interface import operation_tab5
        operation_tab5()

    elif user_choice == "Календарь и Заметки":
        from view.tab6_interface import operation_tab6
        operation_tab6()
