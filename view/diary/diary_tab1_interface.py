import streamlit as st 
from db_manager import add_data_to_diary
from time import sleep
from utils.security import encrypt_text
def operation_tab1() :
    '''Функция отвечает за логику работу первой вкладки'''
    st.subheader("Мой дневник")
    if "form_version_diary" not in st.session_state :
            st.session_state.form_version_diary = 0
    if "diary_text_value" not in st.session_state :
            st.session_state.diary_text_value = ""
    sub_tab_1_1,sub_tab_1_2 = st.tabs(["Ввод текста в ручную","Загрузка из файла"])

    with sub_tab_1_1 :
        with st.form(key=f"form_input_user_data_tab2_v{st.session_state.form_version_diary}") :
            user_text = st.text_area("Поделитесь вашими мыслями",value=st.session_state.diary_text_value)
            submit_diary = st.form_submit_button("Сохранить текст",use_container_width=True)
            if submit_diary :
                    if not user_text.strip() :
                        st.error('Нельзя сохранить пустую запись')
                    else :
                        try :
                            master_pwd = st.session_state.master_password_key
                            encrypted_text = encrypt_text(user_text,master_pwd)
                            send = add_data_to_diary(encrypted_text)
                            if send == "success" :
                                    st.success('Запись успешно внесена в базу')
                                    st.session_state.form_version_diary += 1
                                    st.session_state.diary_text_value = ""
                                    sleep(1.5)
                                    st.rerun()
                        except Exception :
                              st.error('Ошибка не удалось зашифровать или сохранить запись')
                              
    with sub_tab_1_2 :
            st.markdown("***Вставьте ваш файл***")
            uploaded_file = st.file_uploader(
                "Вставьте файл txt",
                type=["txt"],
                key="file_input_user_data_tab2"
            )

            if uploaded_file is not None :
                  file_text = uploaded_file.read().decode("utf-8")
                  if st.session_state.diary_text_value != file_text :
                    st.session_state.diary_text_value = file_text
                    st.session_state.form_version_diary += 1
                    st.info("Текст успешно считан перейдите на вкладку 'Ввод текста в ручную' для предпросмотра")
                    st.rerun()