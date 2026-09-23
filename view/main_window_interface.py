import streamlit as st

def main_interface() :
    '''Основная функция управления интерфейсом'''
    with st.sidebar :
        st.title("Silo")
        st.markdown("---")
    
        user_choice = st.radio("Выбор Меню",["Выход",
                                             "Данные",
                                             "Дневник",
                                             "Ассистент Silo",
                                             "Календарь и Заметки",
                                             "Карта"],
                                index=1)
        st.markdown("---")
    

    if user_choice == "Выход" :
        from view.tab0_interface import operation_tab0
        operation_tab0()

    elif user_choice == "Данные":
        from view.safe.safe_interface import main_safe_interface
        main_safe_interface()

    elif user_choice == "Дневник":
        from view.diary.diary_interface import main_diary_interface
        main_diary_interface()

    elif user_choice == "Ассистент Silo":
        from view.tab5_interface import operation_tab5
        operation_tab5()

    elif user_choice == "Календарь и Заметки":
        from view.tab6_interface import operation_tab6
        operation_tab6()
        
    elif user_choice == "Карта" :
        from view.tab_maps import operation_maps
        operation_maps()
