import bcrypt
import secrets
import string
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def hash_password(password : str) -> str :
    '''Хэш пароля перед записью в бд'''
    try :
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes,salt).decode("utf-8")
        return hashed
    except Exception as e:
        raise e

def check_password(plain_password : str, hashed_password : str) -> bool :
    '''Проверка совпадения пароля с хэшем из базы'''
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def generate_secure_password(length=12) -> str :
    '''Генерация случайного пароля'''
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(characters) for _ in range(length))

def generate_crypto_key(master_password : str) -> bytes :
    '''Функция преобразует пароль аккаунта в 32 байтный ключ шифрования'''
    password_bytes = master_password.encode()
    salt = b"salt_for_personal_manager_secure_safe"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    return base64.urlsafe_b64encode(kdf.derive(password_bytes))

def encrypt_text(plain_text : str, master_password : str) -> str :
    '''Функция шифрует любой текст'''
    if not plain_text :
        return ""
    try :
        key = generate_crypto_key(master_password)
        f = Fernet(key)
        return f.encrypt(plain_text.encode()).decode()
    except Exception as e :
        raise e

def decrypt_text(cipher_text : str,master_password : str) -> str :
    '''Расшифровываем строку обратно в текст'''
    if not cipher_text :
        return ""
    try :
        key = generate_crypto_key(master_password)
        f = Fernet(key)
        return f.decrypt(cipher_text.encode()).decode()
    except Exception as e:
        raise e