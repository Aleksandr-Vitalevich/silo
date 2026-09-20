import streamlit as st
from utils.ai_manager import check_ollama_status,send_message_to_ai
from db_manager.work_with_personal_diary import show_data_to_diary_user_choise
def operation_tab5() :
    '''Функция отвечает за логику работу пятой вкладки'''
    ai_ready = check_ollama_status()
    if ai_ready == False:
        st.warning("Нет связи с агентом. Запустите Ollama на ПК")
        st.stop()

    if "ai_talk" not in st.session_state:
        st.session_state.ai_talk = []
    if 'ai_analize' not in st.session_state :
        st.session_state.ai_analize = []

    sub_tab5_1,sub_tab5_2 = st.tabs(['Беседа','Анализ'])

    with sub_tab5_1 :
        st.subheader("Управление агентом")
    
        for message in st.session_state.ai_talk :
            with st.chat_message(message["role"]) :
                st.write(message["content"])
        
        if user_query := st.chat_input("Задайте вопрос ассистенту"):
            with st.chat_message("user"):
                st.write(user_query)
            st.session_state.ai_talk.append({"role": "user", "content": user_query})
            with st.spinner("Бортовой компьютер генерирует ответ..."):
                response = send_message_to_ai(st.session_state.ai_talk)
            st.session_state.ai_talk.append({"role": "assistant", "content": response})
            st.rerun()

    with sub_tab5_2 :
        st.subheader("Анализ дневника")
        for message in st.session_state.ai_analize:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        count_to_analyze = st.slider("Введите число записей для анализа",min_value=1)
        if st.button("Запустить анализ дневника") :
            with st.spinner("Ассистент извлекает и анализирует данные") :
                diary_data = show_data_to_diary_user_choise(count_to_analyze)
                if not diary_data :
                    st.info("В вашем дневнике пока нет записей")
                else :
                    from utils.security import decrypt_text
                    decrypted_text = []
                    user_password = st.session_state.master_password_key
                    for row in diary_data :
                        clean_text = decrypt_text(row[0],user_password)
                        decrypted_text.append(f'- {clean_text}')
                    text = '\n'.join(decrypted_text)
                    prompt_instruction = (
                    f"Система, перед тобой {count_to_analyze} последних записей из дневника владельца крепости. "
                    f"Проведи их глубокий анализ: выдели главные темы, отследи изменения в настроении и сформулируй "
                    f"краткие выводы. Отвечай строго на русском языке. Вот записи:\n\n{text}"
                    )
                    
                    st.session_state.ai_analize.append({"role": "user", "content": f"🤖 Запрос: Проанализируй мои последние {count_to_analyze} записей в Дневнике."})
                
                
                    temp_chat_context = st.session_state.ai_analize.copy()
                    temp_chat_context.append({"role": "user", "content": prompt_instruction})
                
                
                    ai_analysis_response = send_message_to_ai(temp_chat_context)
                
                
                    st.session_state.ai_analize.append({"role": "assistant", "content": ai_analysis_response})

                    st.rerun()