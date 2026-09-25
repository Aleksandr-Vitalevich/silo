@echo off
chcp 65001 > nul
:: 1. Автоматически определяем текущую папку проекта в Windows
cd /d "%~dp0"
set "SCRIPT_DIR=%~dp0"

echo 🔍 [Silo Core Windows] Проверка и освобождение порта 9999...
:: Находим процесс на порту 9999 и жестко убиваем его (kill), если он есть
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9999') do taskkill /f /pid %%a 2>nul

echo 📦 Проверка наличия виртуального окружения...
if not exist ".venv" (
    echo 🛠️ Первичный запуск: создание локального окружения .venv...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    if exist "requirements.txt" (
        echo 📥 Установка боевых библиотек из requirements.txt...
        pip install -r requirements.txt
    )
) else (
    call .venv\Scripts\activate.bat
)

echo 🚀 Запуск сервера Streamlit в фоновом режиме...
:: Запускаем через локальный python.exe с перенаправлением путей
start /b "" ".venv\Scripts\python.exe" -m streamlit run main_operation.py --server.headless true --server.port 9999

timeout /t 2 > nul
set "URL=http://localhost:9999"

echo 🌐 Запуск изолированного окна приложения...
:: 1. Проверяем Google Chrome (64-bit и 32-bit)
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    echo 🚀 Запуск через Google Chrome...
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app=%URL%
    goto :end
)
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    echo 🚀 Запуск через Google Chrome (x86)...
    start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --app=%URL%
    goto :end
)

:: 2. Проверяем Яндекс.Браузер (в общих программах и в папке пользователя AppData)
if exist "%ProgramFiles%\Yandex\YandexBrowser\Application\browser.exe" (
    echo 🚀 Запуск через Яндекс.Браузер (System)...
    start "" "%ProgramFiles%\Yandex\YandexBrowser\Application\browser.exe" --app=%URL%
    goto :end
)
if exist "%LOCALAPPDATA%\Yandex\YandexBrowser\Application\browser.exe" (
    echo 🚀 Запуск через Яндекс.Браузер (User AppData)...
    start "" "%LOCALAPPDATA%\Yandex\YandexBrowser\Application\browser.exe" --app=%URL%
    goto :end
)

:: 3. Аварийный вариант: если ничего не найдено, открываем в браузере по умолчанию
echo ⚠️ Специализированные браузеры не найдены, открываем в стандартном браузере...
start %URL%

:end
echo 🎉 Система Silo Core успешно запущена!
