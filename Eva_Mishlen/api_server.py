# api_server_1c_extended.py
"""
Расширенный REST API сервис для интеграции Python (Ева-Мишлен) с 1С
Добавлены специальные endpoints для работы с 1С
"""

from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import json
from config import API_HOST, API_PORT, API_DEBUG
from logic.storage import (
    load_products, load_orders, load_users,
    get_orders_by_date, get_sales_report, get_order_by_id
)
from logic.logger import logger

app = Flask(__name__)
app.json.ensure_ascii = False

# ============================================================================
# 1С INTEGRATION ENDPOINTS
# ============================================================================

@app.route("/api/1c/orders/create", methods=["POST"])
def create_order_from_1c():
    """
    POST /api/1c/orders/create
    Создаёт заказ из 1С
    
    Ожидает JSON:
    {
        "order_id": "00001",
        "cashier": "Оператор ПВЗ",
        "items": [
            {"product_id": 1, "name": "Торт", "qty": 2, "price": 1890, "sum": 3780}
        ],
        "subtotal": 3780,
        "packaging": 180,
        "discount": 0,
        "total": 3960,
        "payment_method": "card",
        "created_at": "2024-10-05T14:30:00"
    }
    """
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ["order_id", "cashier", "items", "total"]
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            logger.warning(f"1С: отсутствуют поля {missing}")
            return jsonify({
                "success": False,
                "error": f"Отсутствуют поля: {', '.join(missing)}"
            }), 400
        
        # Проверяем что items не пуст
        if not data.get("items") or len(data["items"]) == 0:
            return jsonify({
                "success": False,
                "error": "Заказ должен содержать товары"
            }), 400
        
        # Добавляем timestamp если его нет
        if "created_at" not in data:
            data["created_at"] = datetime.now().isoformat(timespec="seconds")
        
        logger.info(f"1С: получен заказ {data['order_id']} от {data['cashier']}")
        logger.debug(f"Детали: {len(data['items'])} товаров, сумма {data['total']} ₽")
        
        # Сохраняем заказ (если нужно)
        # save_order(data)
        
        return jsonify({
            "success": True,
            "message": "Заказ успешно принят",
            "order_id": data["order_id"],
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"1С: ошибка создания заказа: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/1c/products/sync", methods=["GET"])
def get_products_for_1c():
    """
    GET /api/1c/products/sync
    Получает список товаров для синхронизации с 1С
    """
    try:
        products = load_products()
        
        # Форматируем для 1С
        formatted = []
        for p in products:
            formatted.append({
                "id": p["id"],
                "code": f"000{p['id']}",  # Код для 1С
                "name": p["name"],
                "sub": p.get("sub", ""),
                "price": p["price"],
                "category": p.get("category", "Прочее"),
                "emoji": p.get("emoji", "")
            })
        
        logger.info(f"1С: выдано {len(formatted)} товаров для синхронизации")
        return jsonify({
            "success": True,
            "data": formatted,
            "count": len(formatted)
        }), 200
        
    except Exception as e:
        logger.error(f"1С: ошибка синхронизации товаров: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/1c/reports/sales", methods=["GET"])
def get_sales_report_for_1c():
    """
    GET /api/1c/reports/sales?days=30
    Возвращает отчёт по продажам для 1С
    """
    try:
        days = request.args.get("days", 30, type=int)
        
        orders = load_orders()
        
        # Фильтруем по датам
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        filtered_orders = [
            o for o in orders
            if start_date <= o["created_at"][:10] <= end_date
        ]
        
        # Считаем статистику
        total_amount = sum(o["total"] for o in filtered_orders)
        total_items = sum(len(o["items"]) for o in filtered_orders)
        
        report = {
            "period": {
                "start_date": start_date,
                "end_date": end_date,
                "days": days
            },
            "totals": {
                "orders_count": len(filtered_orders),
                "items_count": total_items,
                "amount": total_amount,
                "average_check": total_amount // len(filtered_orders) if filtered_orders else 0
            },
            "orders": [
                {
                    "order_id": o["order_id"],
                    "date": o["created_at"],
                    "cashier": o["cashier"],
                    "items_count": len(o["items"]),
                    "total": o["total"]
                }
                for o in filtered_orders[-100:]  # Последние 100 заказов
            ]
        }
        
        logger.info(f"1С: выдан отчёт по продажам за {days} дней")
        return jsonify({
            "success": True,
            "data": report
        }), 200
        
    except Exception as e:
        logger.error(f"1С: ошибка получения отчёта: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/1c/discounts/list", methods=["GET"])
def get_discounts_for_1c():
    """
    GET /api/1c/discounts/list
    Возвращает список доступных скидок и промокодов
    """
    try:
        from config import DISCOUNT_CODES
        
        discounts = []
        for code, percent in DISCOUNT_CODES.items():
            discounts.append({
                "code": code,
                "percent": percent * 100,
                "description": f"Скидка {int(percent*100)}%",
                "active": True
            })
        
        logger.info(f"1С: выдано {len(discounts)} кодов скидок")
        return jsonify({
            "success": True,
            "data": discounts
        }), 200
        
    except Exception as e:
        logger.error(f"1С: ошибка получения скидок: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/1c/check-discount", methods=["POST"])
def check_discount_for_1c():
    """
    POST /api/1c/check-discount
    Проверяет код скидки
    
    Тело запроса:
    {
        "code": "SWEET10",
        "subtotal": 1000
    }
    """
    try:
        data = request.get_json()
        code = data.get("code", "").upper()
        subtotal = data.get("subtotal", 0)
        
        from config import DISCOUNT_CODES
        
        if code not in DISCOUNT_CODES:
            return jsonify({
                "success": False,
                "valid": False,
                "message": "Код не найден"
            }), 400
        
        percent = DISCOUNT_CODES[code]
        discount_amount = int(subtotal * percent)
        
        logger.info(f"1С: проверка скидки {code}, размер {discount_amount} ₽")
        
        return jsonify({
            "success": True,
            "valid": True,
            "code": code,
            "percent": int(percent * 100),
            "subtotal": subtotal,
            "discount_amount": discount_amount,
            "new_total": subtotal - discount_amount
        }), 200
        
    except Exception as e:
        logger.error(f"1С: ошибка проверки скидки: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/1c/config", methods=["GET"])
def get_config_for_1c():
    """
    GET /api/1c/config
    Возвращает конфигурацию системы для 1С
    """
    try:
        from config import DEFAULT_PACKAGING, DEFAULT_PAYMENT
        
        config = {
            "version": "1.0.0",
            "api_version": "1.0",
            "app_name": "Ева-Мишлен",
            "currency": "RUB",
            "settings": {
                "default_packaging": DEFAULT_PACKAGING,
                "default_payment_method": DEFAULT_PAYMENT,
                "vat_included": True
            }
        }
        
        return jsonify({
            "success": True,
            "data": config
        }), 200
        
    except Exception as e:
        logger.error(f"1С: ошибка получения конфигурации: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# ОРИГИНАЛЬНЫЕ ENDPOINTS (для Python приложения)
# ============================================================================

@app.route("/", methods=["GET"])
def index():
    """Информация об API"""
    return jsonify({
        "success": True,
        "app": "Ева-Мишлен",
        "version": "1.0.0",
        "endpoints": {
            "products": "/api/products",
            "orders": "/api/orders",
            "reports": "/api/reports/sales",
            "1c_orders": "/api/1c/orders/create",
            "1c_products": "/api/1c/products/sync",
            "1c_discounts": "/api/1c/discounts/list",
        }
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Проверка здоровья сервиса"""
    return jsonify({"status": "ok"}), 200


@app.route("/api/products", methods=["GET"])
def get_products():
    """GET /api/products - Список товаров"""
    try:
        products = load_products()
        category = request.args.get("category")
        
        if category:
            products = [p for p in products if p.get("category") == category]
        
        logger.info(f"Выдано {len(products)} товаров")
        return jsonify({
            "success": True,
            "data": products
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка получения товаров: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/orders", methods=["GET"])
def get_orders():
    """GET /api/orders - Список заказов"""
    try:
        orders = load_orders()
        limit = request.args.get("limit", type=int)
        
        if limit:
            orders = orders[-limit:]
        
        logger.info(f"Выдано {len(orders)} заказов")
        return jsonify({
            "success": True,
            "data": orders
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка получения заказов: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/orders", methods=["POST"])
def create_order():
    """POST /api/orders - Создать заказ"""
    try:
        data = request.get_json()
        
        required_fields = ["order_id", "cashier", "items", "total"]
        if not all(field in data for field in required_fields):
            return jsonify({
                "success": False,
                "error": f"Отсутствуют обязательные поля: {required_fields}"
            }), 400
        
        if "created_at" not in data:
            data["created_at"] = datetime.now().isoformat(timespec="seconds")
        
        logger.info(f"Создан заказ {data['order_id']}")
        
        return jsonify({
            "success": True,
            "message": "Заказ успешно принят",
            "order_id": data["order_id"]
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка создания заказа: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/reports/sales", methods=["GET"])
def sales_report():
    """GET /api/reports/sales - Отчёт по продажам"""
    try:
        days = request.args.get("days", 30, type=int)
        report = get_sales_report()
        
        logger.info(f"Отчёт по продажам за {days} дней")
        return jsonify({
            "success": True,
            "data": report
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка получения отчёта: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# ERROR HANDLING
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint не найден"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Внутренняя ошибка: {error}")
    return jsonify({
        "success": False,
        "error": "Внутренняя ошибка сервера"
    }), 500


@app.before_request
def log_request():
    """Логирует входящие запросы"""
    logger.debug(f"{request.method} {request.path} - {request.remote_addr}")


if __name__ == "__main__":
    logger.info(f"Запуск API с поддержкой 1С на {API_HOST}:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT, debug=API_DEBUG)
