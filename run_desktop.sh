#!/bin/bash
# Автоматически определяем текущую папку проекта (работает на флешках и в любых директориях)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE}" )" && pwd )"
cd "$SCRIPT_DIR"
# 🌟 МАКСИМАЛЬНАЯ ОЧИСТКА: Находим PID процесса, который держит порт 9999, и жестко убиваем его (kill -9)
echo "🧹 Проверяем и освобождаем порт 9999..."
PID=$(lsof -t -i:9999)
if [ ! -z "$PID" ]; then
    echo "💀 Найдена старая сессия (PID: $PID). Уничтожаем..."
    kill -9 $PID
    sleep 0.5
fi
# 1. Очищаем старые зависшие процессы Streamlit перед стартом, чтобы порт 9999 был всегда свободен
pkill -f streamlit
sleep 0.5

# === БЛОК УМНОЙ АВТОНАСТРОЙКИ ОКРУЖЕНИЯ ===
# Проверяем тип операционной системы
if [[ "$OSTYPE" == "darwin"* ]]; then
    # --- ЛОГИКА ОПРЕДЕЛЕНИЯ ДЛЯ macOS ---
    echo "🍏 Обнаружена система macOS"
else
    # --- ЛОГИКА ОПРЕДЕЛЕНИЯ ДЛЯ LINUX (Ubuntu/Mint/Debian) ---
    echo "🐧 Обнаружена система семейства Linux (Ubuntu/Mint)"
    # Проверяем, установлен ли системный пакет venv (он вырезан в Linux по умолчанию)
    if ! dpkg -l | grep -q "python3-venv"; then
        echo "🔧 Системный пакет python3-venv не найден. Устанавливаем через apt..."
        sudo apt update && sudo apt install -y python3-venv
    fi
fi

# Проверяем наличие виртуального окружения в текущей папке проекта
if [ ! -d ".venv" ]; then
    echo "📦 Первичный запуск: создание локального виртуального окружения .venv..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        echo "📥 Установка боевых библиотек из requirements.txt..."
        pip install -r requirements.txt
        echo "✅ Все зависимости успешно установлены!"
    fi
else
    # Если .venv уже создан — просто активируем его
    source .venv/bin/activate
fi
# ===============================================

# 🚀 2. ЗАПУСК СЕРВЕРА STREAMLIT
# Запускаем чистый сервер текущей папки на уникальном порту 9999 в фоновом режиме
"$SCRIPT_DIR/.venv/bin/python" -m streamlit run main_operation.py --server.headless true --server.port 9999 &
#.venv/bin/streamlit run main_operation.py --server.headless true --server.port 9999 &
#sleep 1.5

URL="http://localhost:9999"

# 🖥 3. ЗАПУСК ИЗОЛИРОВАННОГО ОКНА ПРИЛОЖЕНИЯ
if [[ "$OSTYPE" == "darwin"* ]]; then
    # --- СТАРТ НА macOS ---
    if open -Ra "Google Chrome" 2>/dev/null; then
        echo "🌐 Запуск изолированного окна через Google Chrome..."
        open -a "Google Chrome" --args --app="$URL"
    elif open -Ra "Yandex" 2>/dev/null; then
        echo "🌐 Запуск изолированного окна через Яндекс.Браузер..."
        open -a "Yandex" --args --user-data-dir="/tmp/yandex_safe_profile" --app="$URL"
    else
        echo "💡 Для запуска в виде отдельного окна без рамок рекомендуется установить Google Chrome."
        open -a "Safari" "$URL"
    fi
else
    # --- СТАРТ НА LINUX (Ubuntu/Mint) ---
    if command -v google-chrome &> /dev/null; then
        echo "🌐 Запуск изолированного окна через Google Chrome (Linux)..."
        google-chrome --app="$URL"
    elif command -v yandex-browser &> /dev/null; then
        echo "🌐 Запуск изолированного окна через Яндекс.Браузер (Linux)..."
        yandex-browser --user-data-dir="/tmp/yandex_safe_profile" --app="$URL"
    elif command -v chromium-browser &> /dev/null; then
        echo "🌐 Запуск изолированного окна через Chromium Browser (Linux)..."
        chromium-browser --app="$URL"
    else
        # Отказоустойчивый вариант: если Chromium-браузеров вне Flatpak нет, открываем в системном браузере по умолчанию
        echo "💡 Для скрытия рамок установите Chromium-браузер вне пакета Flatpak."
        xdg-open "$URL"
    fi
fi
