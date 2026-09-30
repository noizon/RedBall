# ============================================================
#  🚀 RED BALL ADVENTURE — ПРОСТОЙ СЕРВЕР
#  Версия: 3.0 ULTIMATE
#  Функции: логи, статистика, рекорды, API, ZIP-скачивание,
#           автооткрытие браузера
# ============================================================

from flask import Flask, render_template, jsonify, send_file, request
import subprocess
import threading
import os
import sys
import io
import json
import zipfile
import logging
import time
import webbrowser
from datetime import datetime

# ============================================================
#  НАСТРОЙКИ
# ============================================================
APP_NAME = "Red Ball Adventure"
APP_VERSION = "3.0 ULTIMATE"
PORT = 5000
GAME_FILE = "game.py"
STATS_FILE = "stats.json"
RECORDS_FILE = "records.json"
LOG_FILE = "server.log"
MAX_RECORDS = 10

# ============================================================
#  ИНИЦИАЛИЗАЦИЯ FLASK
# ============================================================
app = Flask(__name__)

# ============================================================
#  ЛОГИРОВАНИЕ
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
#  РАБОТА СО СТАТИСТИКОЙ
# ============================================================
def load_stats():
    """Загрузить статистику из файла"""
    default_stats = {
        "total_launches": 0,
        "total_downloads": 0,
        "last_launch": None,
        "last_download": None,
        "first_launch": None
    }
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                return {**default_stats, **json.load(f)}
    except Exception as e:
        logger.error(f"Ошибка загрузки статистики: {e}")
    return default_stats

def save_stats(stats):
    """Сохранить статистику"""
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка сохранения статистики: {e}")

def update_stats(key):
    """Обновить поле статистики"""
    stats = load_stats()
    stats[key] = stats.get(key, 0) + 1
    if key == "total_launches":
        now = datetime.now().isoformat()
        stats["last_launch"] = now
        if not stats.get("first_launch"):
            stats["first_launch"] = now
    elif key == "total_downloads":
        stats["last_download"] = datetime.now().isoformat()
    save_stats(stats)
    return stats

# ============================================================
#  РАБОТА С РЕКОРДАМИ
# ============================================================
def load_records():
    """Загрузить таблицу рекордов"""
    try:
        if os.path.exists(RECORDS_FILE):
            with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки рекордов: {e}")
    return []

def save_records(records):
    """Сохранить таблицу рекордов"""
    try:
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка сохранения рекордов: {e}")

def add_record(name, score):
    """Добавить рекорд"""
    records = load_records()
    records.append({
        "name": name or "Игрок",
        "score": score,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M")
    })
    records.sort(key=lambda x: -x["score"])
    records = records[:MAX_RECORDS]
    save_records(records)
    logger.info(f"🏆 Новый рекорд: {name} — {score}")
    return records

# ============================================================
#  МАРШРУТ: ГЛАВНАЯ СТРАНИЦА
# ============================================================
@app.route('/')
def index():
    logger.info(f"🌐 Заход на сайт от {request.remote_addr}")
    return render_template('index.html')

# ============================================================
#  МАРШРУТ: ЗАПУСК ИГРЫ
# ============================================================
@app.route('/start_game')
def start_game():
    logger.info(f"🎮 Запуск игры от {request.remote_addr}")
    
    try:
        if not os.path.exists(GAME_FILE):
            logger.error(f"❌ Файл {GAME_FILE} не найден!")
            return jsonify({
                'success': False,
                'error': f'Файл {GAME_FILE} не найден'
            }), 404
        
        def run_game():
            try:
                if os.name == 'nt':  # Windows
                    subprocess.Popen(
                        f'start /B python {GAME_FILE}',
                        shell=True,
                        cwd=os.getcwd()
                    )
                else:  # Linux/Mac
                    subprocess.Popen(
                        ['python3', GAME_FILE],
                        cwd=os.getcwd()
                    )
                logger.info("✅ Игра запущена в отдельном процессе")
            except Exception as e:
                logger.error(f"❌ Ошибка запуска: {e}")
        
        thread = threading.Thread(target=run_game)
        thread.daemon = True
        thread.start()
        
        stats = update_stats("total_launches")
        
        return jsonify({
            'success': True,
            'message': 'Игра запускается...',
            'total_launches': stats['total_launches']
        })
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
#  МАРШРУТ: СКАЧИВАНИЕ ZIP
# ============================================================
@app.route('/download_game')
def download_game():
    logger.info(f"⬇ Запрос на скачивание от {request.remote_addr}")
    
    try:
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 1. game.py
            if os.path.exists(GAME_FILE):
                zf.write(GAME_FILE, f'RedBallAdventure/{GAME_FILE}')
            else:
                return jsonify({
                    'success': False,
                    'error': f'{GAME_FILE} не найден'
                }), 404
            
            # 2. JSON-файлы
            for json_file in ['save_data.json', 'achievements.json']:
                if os.path.exists(json_file):
                    zf.write(json_file, f'RedBallAdventure/{json_file}')
            
            # 3. Папка assets
            if os.path.exists('assets'):
                for root, dirs, files in os.walk('assets'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.join('RedBallAdventure', file_path)
                        zf.write(file_path, arc_name)
            
            # 4. start.bat
            start_bat = '''@echo off
title Red Ball Adventure
cd /d "%~dp0"
color 0A

echo ========================================
echo    RED BALL ADVENTURE
echo ========================================
echo.
echo Запуск игры...
echo.

python game.py

if errorlevel 1 (
    echo.
    echo [ОШИБКА] Python не установлен или произошла ошибка!
    echo.
    echo Скачай Python: https://www.python.org/downloads/
    echo После установки выполни: pip install pygame
    echo.
    pause
)
'''
            zf.writestr('RedBallAdventure/start.bat', start_bat)
            
            # 5. README.txt
            readme = f'''============================================
   RED BALL ADVENTURE — Инструкция
============================================

КАК ЗАПУСТИТЬ:
1. Распакуйте архив в любую папку
2. Запустите start.bat (двойной клик)
3. Играйте!

УПРАВЛЕНИЕ:
A / стрелка влево   — движение влево
D / стрелка вправо  — движение вправо
ПРОБЕЛ              — прыжок
R                   — рестарт уровня
TAB                 — достижения

ТРЕБОВАНИЯ:
- Windows 7/10/11
- Python 3.8+ (https://www.python.org/downloads/)
- Pygame: pip install pygame

ЧТО В ИГРЕ:
- 20 уровней с разными темами
- 4 босса (огненный, ледяной, водяной, теневой)
- 15 достижений
- Система сохранений

АВТОР: NoiZoN
ВЕРСИЯ: {APP_VERSION}
============================================
'''
            zf.writestr('RedBallAdventure/README.txt', readme)
        
        memory_file.seek(0)
        
        update_stats("total_downloads")
        
        filename = f'RedBallAdventure_{datetime.now().strftime("%Y%m%d")}.zip'
        logger.info(f"✅ ZIP создан: {filename}")
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"❌ Ошибка создания ZIP: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
#  МАРШРУТ: СТАТИСТИКА
# ============================================================
@app.route('/stats')
def stats_page():
    """Страница со статистикой"""
    stats = load_stats()
    records = load_records()
    return jsonify({
        'app': APP_NAME,
        'version': APP_VERSION,
        'stats': stats,
        'records': records
    })

# ============================================================
#  МАРШРУТ: ТАБЛИЦА РЕКОРДОВ
# ============================================================
@app.route('/records')
def records_page():
    """Получить таблицу рекордов"""
    return jsonify({
        'success': True,
        'records': load_records()
    })

@app.route('/add_record', methods=['POST'])
def add_record_route():
    """Добавить новый рекорд"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Нет данных'}), 400
        
        name = data.get('name', 'Игрок')
        score = data.get('score', 0)
        
        if not isinstance(score, int) or score < 0:
            return jsonify({'success': False, 'error': 'Неверный счёт'}), 400
        
        records = add_record(name, score)
        
        return jsonify({
            'success': True,
            'message': 'Рекорд добавлен',
            'records': records
        })
        
    except Exception as e:
        logger.error(f"❌ Ошибка добавления рекорда: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================
#  МАРШРУТ: API
# ============================================================
@app.route('/api/stats')
def api_stats():
    """API: статистика"""
    return jsonify(load_stats())

@app.route('/api/records')
def api_records():
    """API: рекорды"""
    return jsonify(load_records())

@app.route('/api/info')
def api_info():
    """API: информация о сервере"""
    return jsonify({
        'app': APP_NAME,
        'version': APP_VERSION,
        'game_exists': os.path.exists(GAME_FILE),
        'stats': load_stats(),
        'records_count': len(load_records())
    })

@app.route('/api/health')
def api_health():
    """API: проверка сервера"""
    return jsonify({'status': 'ok', 'time': datetime.now().isoformat()})

# ============================================================
#  МАРШРУТ: ЛОГИ
# ============================================================
@app.route('/logs')
def logs_page():
    """Показать последние логи"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return '\n'.join(lines[-100:])
    except Exception as e:
        return f"Ошибка: {e}"
    return "Логов пока нет"

# ============================================================
#  ОБРАБОТКА ОШИБОК
# ============================================================
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Не найдено', 'message': 'Ресурс не существует'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"❌ Ошибка сервера: {e}")
    return jsonify({'error': 'Ошибка сервера', 'message': str(e)}), 500

# ============================================================
#  БАННЕР И АВТООТКРЫТИЕ БРАУЗЕРА
# ============================================================
def print_banner():
    """Красивый баннер при запуске"""
    stats = load_stats()
    records = load_records()
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎮 {APP_NAME}                                          ║
║   📦 Версия: {APP_VERSION}                                ║
║                                                           ║
║   🌐 Локальный: http://localhost:{PORT}                   ║
║   📂 Путь:      {os.getcwd()}                            ║
║                                                           ║
║   📊 СТАТИСТИКА:                                          ║
║   🎮 Запусков:  {stats['total_launches']}                 ║
║   ⬇ Скачиваний: {stats['total_downloads']}                ║
║   🏆 Рекордов:  {len(records)}                            ║
║                                                           ║
║   🌐 Браузер откроется автоматически через 1 секунду      ║
║   🛑 Остановка: Ctrl+C                                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")

def open_browser():
    """Автоматически открывает браузер"""
    time.sleep(1)
    try:
        webbrowser.open(f"http://localhost:{PORT}")
        logger.info("🌐 Браузер открыт автоматически")
    except Exception as e:
        logger.error(f"Не удалось открыть браузер: {e}")

# ============================================================
#  ЗАПУСК СЕРВЕРА
# ============================================================
if __name__ == '__main__':
    try:
        # Проверяем наличие игры
        if not os.path.exists(GAME_FILE):
            logger.warning(f"⚠️ Файл {GAME_FILE} не найден!")
        
        print_banner()
        logger.info(f"🚀 Сервер запущен на http://localhost:{PORT}")
        
        # Открываем браузер в отдельном потоке
        threading.Thread(target=open_browser, daemon=True).start()
        
        app.run('192.168.10.193',debug=False, port=PORT, threaded=True)
        
    except KeyboardInterrupt:
        logger.info("🛑 Сервер остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)