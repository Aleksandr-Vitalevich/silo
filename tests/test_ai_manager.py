from utils.ai_manager import check_ollama_status,send_message_to_ai
import pytest


def test_check_ollama_status() :
    '''Тест запроса к ии'''
    status = check_ollama_status()
    assert isinstance(status,bool)

def test_send_message_to_ai() :
    '''Тест отправки сообщения ии'''
    if check_ollama_status() :
        test_history = [{"role": "user", "content": "Привет, проверь связь"}]
        result = send_message_to_ai(test_history)
        assert result is not None
        assert "Ошибка" not in result
    else :
        pytest.skip("Локальный сервер выключен")