import streamlit as st 
from db_manager import show_data_to_diary,delete_data_to_diary
from time import sleep
from utils.security import decrypt_text


def operation_tab2() :
    '''Функция отвечает за логику работу второй вкладки'''
    st.subheader("Управление дневником")
    sub_tab_2_1,sub_tab_2_2 = st.tabs(["Получить записи","Удалить запись"])

    with sub_tab_2_1 :
        st.subheader('Меню мои записи')
        try :
            my_notes = show_data_to_diary()
        except Exception :
            st.error('Не удалось загрузить данные')
            my_notes = None
        if my_notes :
            master_pwd = st.session_state.master_password_key
            for note in my_notes :
                id, text, date = note
                decrypted_diary_text = decrypt_text(text,master_pwd)
                with st.chat_message("user", avatar="📝"):
                    st.caption(f"ID {id} Время: {date}")
                    st.write(decrypted_diary_text)

    with sub_tab_2_2 :
        st.subheader("Меню удаления записи")
        user_input = st.number_input('Введите id записи для удаления',step=1,min_value=1,key="delete_diary_record_id_input")
        if st.button("Удалить запись",use_container_width=True,key="delete_diary_button_click") :
            try :
                delete_file = delete_data_to_diary(user_input)
                if delete_file == "success" :
                    st.info(f"Удаление прошло успешно Запись с id = {user_input} удалена")
                    sleep(1.5)
                    st.rerun()
            except Exception :
                st.error('Ошибка при удалении записи')

    