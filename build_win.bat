@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo 📦 [Silo Core Windows Build] Активация окружения...
if not exist ".venv" (
    echo 🚨 Ошибка: Окружение .venv не найдено! Запустите сначала run_desktop.bat
    pause
    exit /b
)

call .venv\Scripts\activate.bat

echo 🔍 Проверка шпионского снаряжения для сборки...
:: Пытаемся вызвать pyinstaller, если вылетает ошибка - устанавливаем пакеты
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Инструменты сборки не найдены. Автоматическая установка pyinstaller и зависимостей...
    python -m pip install --upgrade pip
    pip install pyinstaller streamlit-to-exe
)

echo 🔍 Определение системных путей Streamlit...
for /f "delims=" %%i in ('python -c "import streamlit; import os; print(os.path.dirname(streamlit.__file__))"') do set "STREAMLIT_DIR=%%i"

echo 🛠️ Запуск компиляции PyInstaller в один .exe...
pyinstaller --onefile --clean ^
    --copy-metadata streamlit ^
    --add-data "%STREAMLIT_DIR%\static;streamlit\static" ^
    --add-data "view;view" ^
    --add-data "utils;utils" ^
    main_operation.py --name "SiloCore"

echo 🎉 Сборка успешно завершена! Ищите файл SiloCore.exe в папке dist.
pause
