# logic/order.py (исправленная версия)
from config import DEFAULT_PACKAGING, DISCOUNT_CODES
from logic.storage import next_order_number, now_iso, save_order
from logic.logger import logger


class OrderItem:
    """Элемент заказа (товар + количество)"""
    def __init__(self, product):
        self.product = product
        self.qty = 1

    @property
    def sum(self):
        """Стоимость позиции"""
        return self.product.price * self.qty

    def to_dict(self):
        """Для сериализации"""
        return {
            "product_id": self.product.id,
            "name": self.product.name,
            "qty": self.qty,
            "price": self.product.price,
            "sum": self.sum
        }


class Order:
    """Заказ (корзина)"""
    def __init__(self, cashier_name):
        self.order_id = next_order_number()
        self.cashier = cashier_name
        self.items = []
        self.discount = 0
        self.packaging = DEFAULT_PACKAGING
        self.payment_method = "card"
        logger.info(f"Создан новый заказ {self.order_id} для {cashier_name}")

    def add_product(self, product):
        """Добавляет товар или увеличивает количество"""
        for item in self.items:
            if item.product.id == product.id:
                item.qty += 1
                logger.info(f"Товар {product.name} количество {item.qty}")
                return
        
        self.items.append(OrderItem(product))
        logger.info(f"Добавлен товар {product.name}")

    def remove_item(self, product_id):
        """Удаляет товар из заказа"""
        old_len = len(self.items)
        self.items = [i for i in self.items if i.product.id != product_id]
        
        if len(self.items) < old_len:
            logger.info(f"Товар {product_id} удален из заказа")

    def change_qty(self, product_id, delta):
        """Изменяет количество товара на delta"""
        for item in self.items:
            if item.product.id == product_id:
                item.qty += delta
                logger.info(f"Товар {product_id}: новое кол-во {item.qty}")
                
                if item.qty <= 0:
                    self.remove_item(product_id)
                return

    @property
    def subtotal(self):
        """Сумма товаров без учета упаковки и скидки"""
        return sum(i.sum for i in self.items)

    @property
    def total(self):
        """Итоговая сумма"""
        return max(0, self.subtotal + self.packaging - self.discount)

    def apply_discount(self, code):
        """Применяет код скидки"""
        if code.upper() not in DISCOUNT_CODES:
            logger.warning(f"Неверный код скидки: {code}")
            return False, "Код не найден"
        
        percent = DISCOUNT_CODES[code.upper()]
        self.discount = int(self.subtotal * percent)
        
        logger.info(f"Скидка {percent*100}% применена, размер: {self.discount}")
        return True, f"Скидка {int(percent * 100)}% применена"

    def to_dict(self):
        """Сериализует заказ в dict"""
        return {
            "order_id": self.order_id,
            "cashier": self.cashier,
            "created_at": now_iso(),
            "items": [i.to_dict() for i in self.items],
            "subtotal": self.subtotal,
            "packaging": self.packaging,
            "discount": self.discount,
            "total": self.total,
            "payment_method": self.payment_method,
        }

    def save(self):
        """Сохраняет заказ"""
        if not self.items:
            logger.warning("Попытка сохранить пустой заказ")
            return False
        
        result = save_order(self.to_dict())
        if result:
            logger.info(f"Заказ {self.order_id} успешно проведён")
        return result
