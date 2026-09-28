import streamlit as st 
from db_manager.work_with_personal_files import get_file,get_all_files,delete_file
from time import sleep
from utils.security import decrypt_file
import base64

def operation_tab2() :
    '''Функция отвечает за управление файлами'''
    tab1,tab2 = st.tabs(["Открыть файл","Удалить файл"])
    with tab1 :
        st.subheader("Меню чтения и выбора файла")
        user_choice = st.selectbox("Выберите файл",get_all_files(),format_func=lambda x: x[1],key="choice_for_read")
        if st.button("Прочитать файл",use_container_width=True,key="read_file") :
            try :
                master_pwd = st.session_state.master_password_key
                file_name,file_content = get_file(user_choice[0])
                decrypted_file = decrypt_file(file_content,master_pwd)
                base64_pdf = base64.b64encode(decrypted_file).decode('utf-8')
                st.markdown(f"***{file_name}***")
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'            
                st.markdown(pdf_display, unsafe_allow_html=True)
                st.download_button("💾 Скачать оригинал на жесткий диск", data=decrypted_file, file_name=file_name, mime="application/pdf")
            except Exception :
                st.error("Не удалось прочитать файл")

    with tab2 :
        st.subheader("Меню удаления файла")
        files_list = get_all_files()
        if not files_list :
             st.info('Нет файлов для удаления')
        else :
            user_choice = st.selectbox("Выберите файл",files_list,format_func=lambda x: x[1],key="choice_for_delete")
            file_id = user_choice[0]
            file_name = user_choice[1]
            confirm_delete = st.checkbox(f"Я действительно хочу удалить файл '{file_name}'", key="confirm_delete_check")
            if st.button(f'Подтвердить удаление файла {file_name}',key="delese_file_accept") :
                try :
                    res_del = delete_file(file_id)
                    if res_del == "success" :
                        st.success(f"Файл успешно удален {file_name}")
                        sleep(1)
                        st.rerun()
                except Exception :
                    st.error("Не удалось удалить файл")       