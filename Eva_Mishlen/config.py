# config.py
import os
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# Создаём папки если их нет
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Логирование
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOG_DIR / "app.log"

# API для 1С
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "5000"))
API_DEBUG = os.getenv("API_DEBUG", "False") == "True"

# Бизнес-логика
DEFAULT_PACKAGING = 180  # стоимость упаковки
DEFAULT_PAYMENT = "card"  # способ оплаты по умолчанию

DISCOUNT_CODES = {
    "SWEET10": 0.10,
    "SWEET20": 0.20,
    "BIRTHDAY": 0.15,
    "VIP": 0.25,
}

# 1С Integration
EXPORT_FORMAT = "json"  # json или xml
SYNC_INTERVAL = 300  # секунды между синхронизациями
