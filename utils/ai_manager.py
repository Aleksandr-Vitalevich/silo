import requests
import json
from utils.logger import db_logger
from utils.retry import retry_on_lock

import os

def load_prompt(file_name: str) -> str:
    '''Читает markdown-файл с промптом из папки utils/prompts/'''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "prompts", file_name)
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception:
        return "Ты — ассистент Silo Core."

def check_ollama_status() :
    '''Функция отправляет запрос к ии ollama'''
    try :
        response = requests.get("http://localhost:11434",timeout=1)
        return True if response.status_code == 200 else False
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) :
        return False
    except Exception :
        raise False
    
@db_logger
@retry_on_lock
def send_message_to_ai(chat_history : list,system_instruction:str = None) :
    '''Функция отправляет сообщения ии'''
    if system_instruction is None:
        system_instruction = load_prompt("chat_prompt.md")
    try :
        url = "http://localhost:11434/api/chat"
        chat_instruction = load_prompt("chat_prompt.md")
        
        system_instruction = {
            "role": "system",
            "content": chat_instruction
        }
        full_messages = [system_instruction] + chat_history
        dct_response = {
            "model": "llama3", 
            "messages": full_messages,
            "stream": False 
        }
        response = requests.post(url,json=dct_response)
        res_json = response.json()
        if "message" in res_json and "content" in res_json["message"]:
            return res_json["message"]["content"]
        else:
            return "Ошибка: Не удалось извлечь ответ из формата чата Ollama."
    except Exception as e :
        raise e

if __name__ == "__main__" :
    print(check_ollama_status())
    print(send_message_to_ai("Hello"))