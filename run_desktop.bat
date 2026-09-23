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
:: Проверяем наличие Chrome в стандартных путях Windows
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    echo 🚀 Запуск через Google Chrome...
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app=%URL%
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    echo 🚀 Запуск через Google Chrome (x86)...
    start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --app=%URL%
) else (
    echo ⚠️ Chrome не найден, открываем в системном браузере по умолчанию...
    start %URL%
)
