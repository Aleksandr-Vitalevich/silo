import streamlit as st
from datetime import date
from time import sleep
from utils.ai_manager import check_ollama_status, send_message_to_ai, load_prompt
from db_manager.work_with_personal_diary import show_data_to_diary_user_choise 
from db_manager.work_with_calendar import get_calandar_tasks_by_date
from utils.security import decrypt_text

def operation_tab2():
    '''Функция отвечает за логику сквозного анализа за текущий день'''
    st.subheader("⚡ Сквозной анализ дня")
    
    ai_ready = check_ollama_status()
    if ai_ready == False:
        st.warning("Нет связи с агентом. Запустите Ollama на ПК")
        st.stop()
        
    if "ai_analysis_report" not in st.session_state:
        st.session_state.ai_analysis_report = ""
        
    password = st.session_state.master_password_key
    current_date_str = str(date.today())
    
    st.info(f"Анализ будет проведен за сегодня: **{current_date_str}**")
    
    if st.button("📊 Запустить сквозной анализ", use_container_width=True):
        with st.spinner("Ассистент стягивает данные из базы и проводит анализ..."):
            try:
                data_calendar = get_calandar_tasks_by_date(current_date_str)
                tasks_list = []
                if data_calendar:
                    for task_id, enc_title, enc_desk, is_completed, priority in data_calendar:
                        title = decrypt_text(enc_title, password)
                        status = "Выполнено" if is_completed == 1 else "В процессе"
                        tasks_list.append(f"- [{priority}] {title} ({status})")
                tasks_text = "\n".join(tasks_list) if tasks_list else "Нет запланированных задач на сегодня."

                diary_data = show_data_to_diary_user_choise(1) 
                diary_text = "Записи в дневнике за сегодня отсутствуют."
                
                if diary_data:
                    clean_text = decrypt_text(diary_data[0][0], password)
                    diary_text = clean_text

                prompt_instruction = f"""Вот выгрузка логов пользователя за сегодня ({current_date_str}). 
                prompt_instruction += "\n\nВАЖНО: Ответь на русском языке, используя структуру из системного промпта."
                Проанализируй эти данные:

                [СПИСОК ЗАДАЧ ИЗ КАЛЕНДАРЯ]:
                {tasks_text}

                [ЗАПИСЬ ИЗ ДНЕВНИКА]:
                {diary_text}"""

                analysis_sys_prompt = load_prompt("analysis_prompt.md")
                
                chat_context = [{"role": "user", "content": prompt_instruction}]
                
                response = send_message_to_ai(chat_context, system_instruction=analysis_sys_prompt)
                
                st.session_state.ai_analysis_report = response
                st.rerun()

            except Exception:
                st.error("Не удалось собрать данные или провести анализ.")

    if st.session_state.ai_analysis_report:
        st.markdown("---")
        st.markdown(st.session_state.ai_analysis_report)
