import streamlit as st
from db_manager import add_data
from utils import generate_secure_password,encrypt_text
from time import sleep

def operation_tab1() :
    '''Функция отвечает за логику работу первой вкладки'''
    st.subheader("Данные")
    if "form_version" not in st.session_state :
        st.session_state.form_version = 0
    if "generated_pwd" not in st.session_state :
        st.session_state.generated_pwd = ""
    if st.button("Сгенерировать пароль",use_container_width=True) :
        st.session_state.generated_pwd = generate_secure_password(length=16)
        st.info(f'Создан пароль : `{st.session_state.generated_pwd}`(Пароль добавлен в форму)')
    st.info("Не забудьте обновить пароль в вашем сервисе")
    with st.form(key=f"form_input_user_data_tab1_v{st.session_state.form_version}") :
        st.markdown("Заполните нужные поля")
        name_service = st.text_input("Введите имя сервиса. Пример GITHUB ")
        login_service = st.text_input("Введите логин от сервиса")
        password_service = st.text_input(
            "Введите пароль от сервиса",
            value=st.session_state.generated_pwd,
            type="password")
        site_service = st.text_input("Введите или вставьте ссылку от сервиса")
        token_service = st.text_input("Введите токен")
        other_need_information_service = st.text_area("Дополнительная информация")
        submit_button_form = st.form_submit_button("Сохранить данные",use_container_width=True)
        if submit_button_form :
            check_name_service = name_service.strip()
            if not check_name_service :
                st.error('Это поле обязательно для заполнения')
            else :
                try :
                    master_pwd = st.session_state.master_password_key
                    raw_dct = {
                    "name_service" : name_service,
                    "login_service" : login_service,
                    "password_service" : encrypt_text(password_service,master_pwd),
                    "site_service" : encrypt_text(site_service,master_pwd),
                    "token_service" : encrypt_text(token_service,master_pwd),
                    "other_need_information_service" : encrypt_text(other_need_information_service,master_pwd)
                    }
                    dct = {key : value for key,value in raw_dct.items() if value != ""}
                    send = add_data(dct)
                    if send == "success" :
                        st.success('Данные успешно записаны')
                        st.session_state.generated_pwd = ""
                        st.session_state.form_version += 1
                        sleep(1.5)
                        st.rerun()
                except Exception :
                    st.error('Ошибка не удалось зашифровать или сохранить данные')
