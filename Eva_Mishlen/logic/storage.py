# logic/storage.py (исправленная версия)
import json
import os
from datetime import datetime
from config import DATA_DIR, DEFAULT_PACKAGING
from logic.logger import logger

def _path(filename):
    """Возвращает полный путь к файлу данных"""
    return os.path.join(str(DATA_DIR), filename)


def load_products():
    """Загружает товары из JSON"""
    try:
        with open(_path("products.json"), "r", encoding="utf-8") as f:
            products = json.load(f)
            logger.info(f"Загружено {len(products)} товаров")
            return products
    except FileNotFoundError:
        logger.error("Файл products.json не найден")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга products.json: {e}")
        return []


def load_users():
    """Загружает пользователей"""
    try:
        with open(_path("users.json"), "r", encoding="utf-8") as f:
            users = json.load(f)
            logger.info(f"Загружено {len(users)} пользователей")
            return users
    except FileNotFoundError:
        logger.error("Файл users.json не найден")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга users.json: {e}")
        return []


def load_orders():
    """Загружает заказы"""
    try:
        path = _path("orders.json")
        if not os.path.exists(path):
            logger.info("Файл orders.json ещё не создан")
            return []
        
        with open(path, "r", encoding="utf-8") as f:
            orders = json.load(f)
            logger.info(f"Загружено {len(orders)} заказов")
            return orders
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга orders.json: {e}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка при загрузке заказов: {e}")
        return []


def save_order(order_dict):
    """Сохраняет заказ в JSON"""
    try:
        orders = load_orders()
        orders.append(order_dict)
        
        path = _path("orders.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Заказ {order_dict['order_id']} сохранён")
        return True
    except Exception as e:
        logger.error(f"Ошибка сохранения заказа: {e}")
        return False


def next_order_number():
    """Возвращает номер следующего заказа"""
    try:
        orders = load_orders()
        if not orders:
            return "00001"
        last = orders[-1]["order_id"]
        return f"{int(last) + 1:05d}"
    except Exception as e:
        logger.error(f"Ошибка при получении номера заказа: {e}")
        return "00001"


def now_iso():
    """Возвращает текущее время в ISO формате"""
    return datetime.now().isoformat(timespec="seconds")


def get_order_by_id(order_id):
    """Получает заказ по ID"""
    try:
        orders = load_orders()
        for order in orders:
            if order["order_id"] == order_id:
                return order
        logger.warning(f"Заказ {order_id} не найден")
        return None
    except Exception as e:
        logger.error(f"Ошибка при поиске заказа: {e}")
        return None


def get_orders_by_date(start_date, end_date):
    """Получает заказы за период"""
    try:
        orders = load_orders()
        filtered = [
            o for o in orders
            if start_date <= o["created_at"][:10] <= end_date
        ]
        logger.info(f"Найдено {len(filtered)} заказов за период {start_date}-{end_date}")
        return filtered
    except Exception as e:
        logger.error(f"Ошибка при фильтрации заказов: {e}")
        return []


def get_sales_report():
    """Возвращает сводку по продажам"""
    try:
        orders = load_orders()
        total_amount = sum(o["total"] for o in orders)
        total_items = sum(len(o["items"]) for o in orders)
        
        report = {
            "total_orders": len(orders),
            "total_amount": total_amount,
            "total_items": total_items,
            "average_check": total_amount // len(orders) if orders else 0
        }
        logger.info(f"Отчёт по продажам: {report}")
        return report
    except Exception as e:
        logger.error(f"Ошибка при генерации отчёта: {e}")
        return {}
