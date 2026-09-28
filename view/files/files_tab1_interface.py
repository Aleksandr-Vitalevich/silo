import streamlit as st 
from db_manager.work_with_personal_files import add_file
from time import sleep
from utils.security import encrypt_file

def operation_tab1() :
    '''Функция отвечает за добавление файла'''
    st.markdown("***Вставьте ваш файл***")
    if "uploader_id" not in st.session_state:
        st.session_state.uploader_id = 0
    uploaded_file = st.file_uploader(
        "Вставьте файл pdf",
            type=["pdf"],
            key=f"file_input_user_file_tab1_{st.session_state.uploader_id}",
            accept_multiple_files=False
                                    )
    
    if uploaded_file is not None :
        max_size = 50 * 1024 * 1024
        if uploaded_file.size > max_size :
            st.error("Файл слишком большой максимальный размер 50 мб")
        else :
            file_bytes = uploaded_file.read()
            if st.button("Сохранить файл",use_container_width=True) :
                try :
                    master_pwd = st.session_state.master_password_key
                    encrypted_text = encrypt_file(file_bytes,master_pwd)
                    save_file = add_file(uploaded_file.name,encrypted_text) 
                    if save_file == "success":
                        st.success("Данные успешно записаны")
                        st.session_state.uploader_id += 1 
                        sleep(1)
                        st.rerun()
                except Exception :
                    st.error('Ошибка не удалось зашифровать или сохранить запись')