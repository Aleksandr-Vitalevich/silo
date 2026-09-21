from view import registration_page_interface,authorization_page_interface,main_interface
from db_manager import add_user,check_user_in_db,check_user_authorization
from db_manager import create_table
import streamlit as st

def main_operation_function() :
    '''Основная функция программы'''
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_file_path = os.path.join(BASE_DIR, "personal_manager.db")
    if not os.path.exists(db_file_path) :
        try :
            create_table()
        except Exception as e :
            st.error("Ошибка не удалось инициилизировать бд")
            st.stop()
    st.set_page_config(
        page_title="Silo",
        layout="wide",
        initial_sidebar_state="expanded"
        )

    if "authorization_user" not in st.session_state :
        st.session_state.authorization_user = False
    
    if st.session_state.authorization_user :
        main_interface()
    else :
        try :
            user = check_user_in_db()
            if not user :
                login,password,clicked = registration_page_interface()
                if clicked :
                    result = add_user(login,password)
                    if result == "success" :
                        st.session_state.authorization_user = True
                        st.session_state.master_password_key = password
                        st.success('Аккаунт успешно создан')
                        st.rerun()
            else:
                login,password,clicked = authorization_page_interface()
                if clicked :
                    is_valid = check_user_authorization(login,password)
                    if is_valid :
                        st.session_state.authorization_user = True
                        st.session_state.master_password_key = password
                        st.rerun()
                    else :
                        st.error("Ошибка не верный логин или пароль")
        except Exception as database_error :
            st.error('Ошибка при обмене данными с сервером')

        

if __name__ == "__main__" :
    main_operation_function()