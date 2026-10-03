import streamlit as st
from datetime import date
from time import sleep
from utils.ai_manager import check_ollama_status, send_message_to_ai, load_prompt
from db_manager.work_with_personal_diary import show_data_to_diary_user_choise 
from db_manager.work_with_calendar import get_calandar_tasks_by_date
from utils.security import decrypt_text

def operation_tab2():
    '''Функция отвечает за логику сквозного анализа'''
    st.subheader("⚡ Сквозной анализ дня")
    
    ai_ready = check_ollama_status()
    if ai_ready == False:
        st.warning("Нет связи с агентом. Запустите Ollama на ПК")
        st.stop()
        
    if "ai_analysis_report" not in st.session_state:
        st.session_state.ai_analysis_report = ""
        
    password = st.session_state.master_password_key
    user_range = st.date_input(
        "Выберите диапазон дат",
        value=(date.today(), date.today()),
        key="diary_analysis_range"
    )


    if isinstance(user_range, tuple) and len(user_range) == 2:
        start_date, end_date = user_range
    
        start_str = f"{start_date} 00:00:00"
        end_str = f"{end_date} 23:59:59"
    
    
        if st.button("📊 Запустить сквозной анализ", use_container_width=True):
            diary_records = show_data_to_diary_user_choise(start_str, end_str)
        
            if diary_records:
                st.success(f"Найдено записей: {len(diary_records)}")
                with st.spinner("Ассистент стягивает данные из базы и проводит анализ..."):
                    try:
                        diary_list = []
                        if diary_records:
                            for row in diary_records:
                                decrypted_record = decrypt_text(row[0], password)
                                diary_list.append(f"- {decrypted_record}")
                            diary_text = "\n".join(diary_list)
                        else:
                            diary_text = "Записи в дневнике за выбранный период отсутствуют."

                        tasks_text = "Анализ задач за диапазон дат будет интегрирован в следующей версии."

                        prompt_instruction = f"""Вот выгрузка логов пользователя за период с {start_date} по {end_date}.
                                            ВАЖНО: Ответь строго на русском языке, используя структуру из системного промпта.
                                            Проанализируй эти данные:

                                            [СПИСОК ЗАДАЧ ИЗ КАЛЕНДАРЯ]:
                                            {tasks_text}

                                            [ЗАПИСИ ИЗ ДНЕВНИКА]:
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
