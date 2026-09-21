import streamlit as st
from db_manager.work_with_calendar import get_calandar_tasks_by_date,update_task_status,add_calendar_task
from datetime import date
from time import sleep
from utils.security import encrypt_text,decrypt_text

def operation_tab6() :
    '''Функция отвечает за логику работу шестой вкладки'''
    if "form_version" not in st.session_state :
        st.session_state.form_version = 0
    st.header("Календарь - Заметки")
    selected_date_obj = st.date_input("Выберите день журнала",value=date.today())
    selected_date_str = str(selected_date_obj)
    sub_tab_6_1,sub_tab_6_2 = st.tabs(["Заметки Анализ","Добавить новую заметку"])

    with sub_tab_6_1 :
        st.subheader("Управление заметками")
        data_calendar = get_calandar_tasks_by_date(selected_date_str)
        if not data_calendar :
            st.info("Нет заметок")
        password = st.session_state.master_password_key
        for task_id,enc_title,enc_desk,is_completed,priority in data_calendar :
            clean_title = decrypt_text(enc_title,password)
            clean_desk = decrypt_text(enc_desk,password)
            display_label = f"Приоритет [{priority}] Заметка {clean_title}"
            if clean_desk :
                display_label += f"- ({clean_desk})"
            checkbox_value = True if is_completed == 1 else False
            status_click = st.checkbox(display_label,value=checkbox_value,key=f"task_check_{task_id}")
            new_status_value = 1 if status_click else 0
            if new_status_value != is_completed :
                update_task_status(task_id,new_status_value)
                st.info(f'заметка {clean_title} выполнены')
                sleep(1)
                st.rerun()
        st.markdown("---")
        if st.button("Анализ заметок") :
            ai_data = []
            for _,enc_title,enc_desk,is_completed,priority in data_calendar :
                title = decrypt_text(enc_title,password)
                status_text = "Выполнено" if is_completed == 1 else "В процессе"
                ai_data.append(f"- [{priority}] {title} (Статус : {status_text})")
            tasks_analyze = "\n".join(ai_data)
            prompt_calendar = (
                f"Система, перед тобой список задач владельца крепости Silo на день {selected_date_str}. "
                f"Оцени нагрузку, выдели критические заметки и дай краткие рекомендации по оптимизации времени. "
                f"Отвечай строго на русском языке, лаконично. Вот расписание:\n\n{tasks_analyze}"
                                )
            with st.spinner("Анализ заметок") :
                from utils.ai_manager import send_message_to_ai
                ai_response = send_message_to_ai([{"role": "user", "content": prompt_calendar}])
                st.info(ai_response)
    with sub_tab_6_2 :
        st.subheader("Меню добавления новой заметки")
        with st.form(key=f"new_task_form_v_{st.session_state.form_version}",clear_on_submit=True) :
            task_title = st.text_input("Название заметки",placeholder="Пример: Сделать домашние дела")
            task_description = st.text_input("Описание заметки (Необязательно)",placeholder="Детали заметки")
            task_priority = st.selectbox("Приоритет",["Low","Medium",'High'],index=1)
            submit_btn = st.form_submit_button("Сохранить")
            if submit_btn :
                if not task_title :
                    st.warning("Это поле обязательно для заполнения")
                else :
                    try :
                        password = st.session_state.master_password_key
                        enc_task_title = encrypt_text(task_title,password)
                        enc_task_description = encrypt_text(task_description,password) if task_description else ""
                        task = add_calendar_task(selected_date_str,enc_task_title,enc_task_description,task_priority)
                        if task == "success" :
                            st.success("Заметка успешно добавлена")
                            st.session_state.form_version += 1
                            sleep(1.5)
                            st.rerun()
                    except Exception :
                        st.error('Ошибка не удалось зашифровать или сохранить заметку')


