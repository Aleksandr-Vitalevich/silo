from utils.security import hash_password,check_password,generate_secure_password,generate_crypto_key,decrypt_text,encrypt_text
import pytest

def test_hash_password() :
    '''Тест проверки записи хэша'''
    password = "123"
    res = hash_password(password)
    assert res is not None
    assert isinstance(res,str)

def test_password_hashing_unique() :
    '''Проверка генерации разных хэшей для одного пароля'''
    password = "bunker"
    hash_one = hash_password(password)
    hash_two = hash_password(password)
    assert hash_one != hash_two
    assert check_password(password,hash_one) is True
    assert check_password(password,hash_two) is True

def test_check_password() :
    '''Проверка совпадения пароля'''
    correct_password = "123"
    wrong_password = "456"
    real_password = hash_password(correct_password)
    assert check_password(correct_password,real_password) is True
    assert check_password(wrong_password,real_password) is False

def test_generate_secure_password() :
    '''Тест генерации случайного пароля'''
    length = 12
    password = generate_secure_password(length)
    assert len(password) == length
    assert isinstance(password,str)

def test_generate_crypto_key_decrypt_encrypt() :
    '''Тест проверки генерации крипто ключа и проверки записи расшифровки и дешивровки информации'''
    password = "master_pasword"
    text = "Hello"
    
    crypto = generate_crypto_key(password)
    assert isinstance(crypto,bytes)

    res_test1 = encrypt_text(text,password)
    assert isinstance(res_test1,str)
    assert res_test1 != text

    res_test2 = decrypt_text(res_test1,password)
    assert isinstance(res_test2,str)
    assert res_test2 == text
