# logic/logger.py
import logging
import sys
from config import LOG_FILE, LOG_LEVEL

def setup_logger():
    """Настраивает логирование приложения"""
    logger = logging.getLogger("eva")
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Формат лога
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Логирование в файл
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Логирование в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
