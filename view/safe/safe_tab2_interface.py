import streamlit as st 
from db_manager import show_data,delete_data,update_data,get_data_by_id
import pandas as pd
from time import sleep
from utils.security import decrypt_text
def operation_tab2() :
    '''Функция отвечает за логику работу третьей вкладки'''
    st.subheader("Управление данными")
    sub_tab_2_1,sub_tab_2_2,sub_tab_2_3 = st.tabs(["Получить записи","Изменить запись","Удалить запись"])

    with sub_tab_2_1 :
        st.subheader('Меню мои записи')
        try :
            my_files = show_data()
            if my_files :
                master_pwd = st.session_state.master_password_key
                decrypt_files = []
                for rec in my_files :
                    rec_id,name,login,pwd,site,token,info = rec
                    dec_pwd = decrypt_text(pwd,master_pwd) if pwd else ""
                    dec_site = decrypt_text(site,master_pwd) if site else ""
                    dec_token = decrypt_text(token,master_pwd) if token else ""
                    dec_info = decrypt_text(info,master_pwd) if info else ""
                    decrypt_files.append((rec_id,name,login,dec_pwd,dec_site,dec_token,dec_info))
                columns = ["ID", "Сервис", "Логин", "Пароль", "Ссылка", "Токен", "Доп. информация"]
                df = pd.DataFrame(decrypt_files,columns=columns)
                st.dataframe(df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                            "Ссылка": st.column_config.LinkColumn("Ссылка")}
            )
            else :
                st.info("Нет записей в базе")
        except Exception :
            st.error('Ошибка расшифровки или загрузки данных')


    with sub_tab_2_2 :
        st.subheader('Меню изменить запись')
        if "edit_form_version" not in st.session_state :
            st.session_state.edit_form_version = 0
        user_input = st.number_input('Введите id записи для редактирования',step=1,min_value=1)
        try :
            change_data = get_data_by_id(user_input)
            if change_data is None:
                st.warning(f'Запись с id {user_input} не найдена в базе')
            else :
                rec_id,rec_name,rec_login,rec_password,rec_site,rec_token,rec_other= change_data

                with st.form(key=f"edit_form_v{st.session_state.get('edit_form_version', 0)}"):
                    st.markdown(f"Редактирование сервиса: **{rec_name}**")
                    
                    new_name = st.text_input("Название сервиса", value=rec_name)
                    new_login = st.text_input("Логин", value=rec_login if rec_login else "")
                    new_password = st.text_input("Пароль", value=rec_password if rec_password else "", type="password")
                    new_site = st.text_input("Ссылка", value=rec_site if rec_site else "")
                    new_token = st.text_input("Токен", value=rec_token if rec_token else "")
                    new_info = st.text_area("Доп. информация", value=rec_other if rec_other else "")
                    
                    submit_edit = st.form_submit_button("Сохранить изменения", use_container_width=True)
                
                    if submit_edit: 
                        check_name_service = new_name.strip()
                        if not check_name_service :
                            st.error('Это поле обязательно для заполнения')
                        else :
                            raw_dct = {
                            "name_service" : new_name.strip(),
                            "login_service" : new_login.strip(),
                            "password_service" : new_password.strip(),
                            "site_service" : new_site.strip(),
                            "token_service" : new_token.strip(),
                            "other_need_information_service" : new_info.strip()
                            }
                            dct = {key : value for key,value in raw_dct.items() if value != ""}
                            send = update_data(user_input,dct)
                            if send == "success" :
                                st.success('Данные успешно записаны')
                                st.session_state.edit_form_version += 1
                                sleep(1.5)
                                st.rerun()
        except Exception :
            st.error("Ошибка расшифровки или загрузки данных")

    with sub_tab_2_3 :
        st.subheader("Меню удаления записи")
        user_input = st.number_input('Введите id записи для удаления',step=1,min_value=1,key="delete_safe_record_id_input")
        if st.button("Удалить запись",use_container_width=True,key="delete_button_click") :
            try :
                delete_file = delete_data(user_input)
                if delete_file == "success" :
                    st.info(f"Удаление прошло успешно Запись с id = {user_input} удалена")
                    sleep(1.5)
                    st.rerun()
            except Exception :
                st.error("Ошибка расшифровки или загрузки данных")