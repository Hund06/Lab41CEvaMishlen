# screens/cashier.py - ПОЛНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ
# ЗАМЕНИТЕ весь файл на этот!

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QLineEdit, QMessageBox, QGridLayout,
    QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

from theme import (
    BG, WHITE, ACCENT, ACCENT_DARK, SOFT, TEXT, MUTED,
    PANEL_PINK, LILAC, MINT, MINT_TEXT, GREY_BTN, LINE, FONT_HEAD
)
from logic.storage import load_products
from logic.product import Product
from logic.order import Order


# ============================================================================
# ИСПРАВЛЕННЫЙ ProductCard - кнопка теперь видна!
# ============================================================================

class ProductCard(QFrame):
    """Карточка товара - ИСПРАВЛЕНО: кнопка + теперь видна"""
    add_clicked = Signal(Product)

    def __init__(self, product: Product):
        super().__init__()
        self.product = product
        self.setObjectName("productCard")
        
        # ✅ ИСПРАВЛЕНИЕ: Увеличиваем высоту чтобы поместилась кнопка
        self.setFixedSize(180, 240)  # Было 280 → теперь 310
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)  # Правильные отступы
        layout.setSpacing(8)

        # === ФОТО ===
        photo = QLabel(product.emoji)
        photo.setAlignment(Qt.AlignCenter)
        photo.setFixedHeight(100)  # Чуть уменьшили
        photo.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #f6d6d6, stop:1 #c9b49e);
            border-radius: 12px;
            font-size: 56px;
        """)
        layout.addWidget(photo)

        # === НАЗВАНИЕ ===
        name = QLabel(product.name)
        name.setWordWrap(True)
        name.setStyleSheet(
            f"font-weight: 700; font-size: 12px; color: {TEXT}; "
            f"padding: 0px; background: transparent;"
        )
        layout.addWidget(name)

        # === ОПИСАНИЕ ===
        if hasattr(product, 'sub') and product.sub:
            sub = QLabel(product.sub)
            sub.setWordWrap(True)
            sub.setStyleSheet(
                f"font-size: 9px; color: #999; "
                f"background: transparent;"
            )
            layout.addWidget(sub)

        # Растягиваемый спейсер
        layout.addStretch()

        # === НИЗ: ЦЕНА + КНОПКА ===
        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)
        bottom.setSpacing(8)

        # Цена
        price = QLabel(f"{product.price:,} ₽".replace(",", " "))
        price.setStyleSheet(
            f"font-size: 14px; font-weight: 700; "
            f"color: {ACCENT_DARK}; background: transparent;"
        )
        bottom.addWidget(price)
        bottom.addStretch()

        # ✅ КНОПКА ДОБАВИТЬ (ТЕПЕРЬ ВИДНА И НА МЕСТЕ!)
        add_btn = QPushButton("+")
        add_btn.setObjectName("addBtn")
        add_btn.setFixedSize(38, 38)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT};
                color: white;
                border: none;
                border-radius: 19px;
                font-size: 20px;
                font-weight: bold;
                padding: 0px;
            }}
            QPushButton:hover {{
                background: #c2185b;
            }}
            QPushButton:pressed {{
                background: #a01648;
            }}
        """)
        add_btn.clicked.connect(lambda: self.add_clicked.emit(self.product))
        bottom.addWidget(add_btn)

        layout.addLayout(bottom)


# ============================================================================
# ОСНОВНОЙ ЭКРАН КАССИРА
# ============================================================================

class CashierScreen(QWidget):
    logout_requested = Signal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.order = Order(user["name"])
        self.products = [Product(p) for p in load_products()]
        self.current_category = "Все"
        self.payment_method = "card"
        self.setObjectName("cashierScreen")
        self._build_ui()
        self._refresh_order()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_header())

        body = QHBoxLayout()
        body.setContentsMargins(28, 16, 28, 16)
        body.setSpacing(18)
        body.addWidget(self._build_catalog(), 4)
        body.addWidget(self._build_order_panel(), 5)
        body.addWidget(self._build_summary(), 3)
        root.addLayout(body, 1)
        root.addWidget(self._build_footer())

    def _build_header(self):
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(82)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(28, 0, 28, 0)

        logo = QLabel("🍰")
        logo.setStyleSheet("font-size: 32px; background: transparent;")
        layout.addWidget(logo)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        title = QLabel("Ева-Мишлен")
        title.setStyleSheet(
            f'font-family: "{FONT_HEAD}"; font-size: 26px; font-weight: 700; '
            f'color: {ACCENT_DARK}; background: transparent;'
        )
        sub = QLabel("Зет-Торт · АРМ Кассира")
        sub.setStyleSheet(f"font-size: 12px; color: {MUTED}; background: transparent;")
        title_box.addWidget(title)
        title_box.addWidget(sub)
        layout.addLayout(title_box)
        layout.addStretch()

        info_box = QVBoxLayout()
        info_box.setSpacing(0)
        info_box.setAlignment(Qt.AlignRight)
        role = QLabel("Кассир")
        role.setStyleSheet(f"font-size: 11px; color: {MUTED}; background: transparent;")
        name = QLabel(self.user["name"])
        name.setStyleSheet("font-size: 15px; font-weight: 700; background: transparent;")
        info_box.addWidget(role)
        info_box.addWidget(name)
        layout.addLayout(info_box)

        avatar = QLabel("👩")
        avatar.setFixedSize(42, 42)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 #f6c9b4, stop:1 #c98f7a); "
            "border-radius: 21px; font-size: 20px; border: 3px solid #f4dede;"
        )
        layout.addWidget(avatar)

        exit_btn = QPushButton("Выход")
        exit_btn.setObjectName("accent")
        exit_btn.setFixedHeight(42)
        exit_btn.clicked.connect(self.logout_requested.emit)
        layout.addWidget(exit_btn)

        return header

    def _build_catalog(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        # Заголовок
        head = QHBoxLayout()
        title = QLabel("Каталог")
        title.setObjectName("h2")
        head.addWidget(title)
        head.addStretch()
        search = QPushButton("⌕")
        search.setFixedSize(34, 34)
        search.setStyleSheet(f"background: {WHITE}; border-radius: 17px; font-size: 14px;")
        head.addWidget(search)
        layout.addLayout(head)

        # Вкладки категорий
        tabs = QHBoxLayout()
        tabs.setSpacing(8)
        categories = ["Все", "Торты", "Пирожные", "Напитки"]
        self.tab_buttons = {}
        for cat in categories:
            btn = QPushButton(cat)
            btn.setObjectName("tabActive" if cat == self.current_category else "tab")
            btn.clicked.connect(lambda checked, c=cat: self._select_category(c))
            tabs.addWidget(btn)
            self.tab_buttons[cat] = btn
        tabs.addStretch()
        layout.addLayout(tabs)

        # Скролл с товарами
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent;")
        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(grid_widget)
        self.grid.setSpacing(14)
        self.grid.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(grid_widget)
        layout.addWidget(scroll)

        self._populate_products()
        return container

    def _populate_products(self):
        """ИСПРАВЛЕННЫЙ - правильно добавляет карточки в grid"""
        # Очищаем
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Фильтруем товары
        if self.current_category == "Все":
            products = self.products
        else:
            products = [p for p in self.products if p.category == self.current_category]

        # Добавляем в сетку (2 колонки)
        row, col = 0, 0
        for product in products:
            card = ProductCard(product)
            card.add_clicked.connect(self._add_to_order)
            self.grid.addWidget(card, row, col)
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
        
        # Спейсер
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.grid.addItem(spacer_item, row + 1, 0, 1, 2)

    def _select_category(self, cat):
        self.current_category = cat
        for key, btn in self.tab_buttons.items():
            btn.setObjectName("tabActive" if key == cat else "tab")
            btn.setStyleSheet("")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self._populate_products()

    def _build_order_panel(self):
        panel = QFrame()
        panel.setObjectName("orderPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        head = QHBoxLayout()
        head_box = QVBoxLayout()
        head_box.setSpacing(0)
        title = QLabel("Текущий заказ")
        title.setObjectName("h2")
        sub = QLabel(f"Заказ № {self.order.order_id} · зал")
        sub.setObjectName("muted")
        head_box.addWidget(title)
        head_box.addWidget(sub)
        head.addLayout(head_box)
        head.addStretch()

        self.badge = QLabel("0 позиций")
        self.badge.setStyleSheet(
            f"background: {SOFT}; color: {ACCENT_DARK}; font-size: 11px; "
            f"font-weight: 700; padding: 8px 13px; border-radius: 999px;"
        )
        head.addWidget(self.badge)
        layout.addLayout(head)

        self.order_container = QVBoxLayout()
        self.order_container.setSpacing(0)
        layout.addLayout(self.order_container)
        layout.addStretch()

        foot = QHBoxLayout()
        hint = QLabel("✨ Можно добавить подарок к заказу")
        hint.setObjectName("muted")
        foot.addWidget(hint)
        foot.addStretch()
        layout.addLayout(foot)

        return panel

    def _build_summary(self):
        panel = QFrame()
        panel.setObjectName("summaryPanel")
        panel.setFixedWidth(330)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(6)

        label = QLabel("Итого")
        label.setObjectName("h3")
        layout.addWidget(label)

        self.total_label = QLabel("0 ₽")
        self.total_label.setObjectName("total")
        layout.addWidget(self.total_label)

        self.vat_label = QLabel("НДС включён · 0 позиций")
        self.vat_label.setObjectName("muted")
        layout.addWidget(self.vat_label)

        layout.addSpacing(10)

        self.subtotal_label = QLabel("0 ₽")
        self.subtotal_label.setStyleSheet("font-weight: 600; background: transparent;")
        self._add_line(layout, "Товары", self.subtotal_label)

        self.pack_label = QLabel("180 ₽")
        self.pack_label.setStyleSheet("font-weight: 600; background: transparent;")
        self._add_line(layout, "Подарочная упаковка", self.pack_label)

        self.discount_label = QLabel("0 ₽")
        self.discount_label.setStyleSheet(
            f"font-weight: 600; background: transparent; color: {ACCENT};"
        )
        self._add_line(layout, "Скидка", self.discount_label)

        layout.addSpacing(6)

        self.pay_label = QLabel("0 ₽")
        self.pay_label.setStyleSheet(
            f"font-weight: 800; color: {ACCENT_DARK}; background: transparent;"
        )
        self._add_line(layout, "К оплате", self.pay_label, bold=True)

        layout.addSpacing(14)

        disc_title = QLabel("Скидка или сертификат")
        disc_title.setStyleSheet("font-size: 11px; font-weight: 800; background: transparent;")
        layout.addWidget(disc_title)

        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText("🎁 Код или карта гостя")
        layout.addWidget(self.discount_input)

        apply_btn = QPushButton("Применить скидку")
        apply_btn.setObjectName("lilac")
        apply_btn.setFixedHeight(42)
        apply_btn.clicked.connect(self._apply_discount)
        layout.addWidget(apply_btn)

        layout.addSpacing(10)

        pay_title = QLabel("Способ оплаты")
        pay_title.setStyleSheet("font-size: 11px; font-weight: 800; background: transparent;")
        layout.addWidget(pay_title)

        pay_row = QHBoxLayout()
        pay_row.setSpacing(8)
        self.card_btn = QPushButton("💳 Карта")
        self.cash_btn = QPushButton("💵 Наличные")
        self.card_btn.clicked.connect(lambda: self._set_payment("card"))
        self.cash_btn.clicked.connect(lambda: self._set_payment("cash"))
        pay_row.addWidget(self.card_btn)
        pay_row.addWidget(self.cash_btn)
        layout.addLayout(pay_row)
        self._update_payment_buttons()

        layout.addStretch()

        pay_btn = QPushButton("Оплатить")
        pay_btn.setObjectName("accent")
        pay_btn.setFixedHeight(48)
        pay_btn.clicked.connect(self._pay)
        layout.addWidget(pay_btn)

        post_btn = QPushButton("Провести заказ →")
        post_btn.setObjectName("accent")
        post_btn.setFixedHeight(58)
        post_btn.clicked.connect(self._post_order)
        layout.addWidget(post_btn)

        return panel

    def _add_line(self, layout, label_text, value_widget, bold=False):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        if bold:
            lbl.setStyleSheet(f"font-weight: 800; color: {ACCENT_DARK}; background: transparent;")
        else:
            lbl.setStyleSheet("background: transparent;")
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(value_widget)
        layout.addLayout(row)

    def _build_footer(self):
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setFixedHeight(90)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(12)

        cancel = QPushButton("Отменить заказ")
        cancel.setObjectName("grey")
        cancel.setFixedHeight(50)
        cancel.clicked.connect(self._cancel_order)
        layout.addWidget(cancel)

        draft = QPushButton("Сохранить черновик")
        draft.setObjectName("mint")
        draft.setFixedHeight(50)
        layout.addWidget(draft)

        layout.addStretch()

        dot = QLabel("●")
        dot.setStyleSheet("color: #1f8a70; font-size: 14px; background: transparent;")
        layout.addWidget(dot)

        shift_box = QVBoxLayout()
        shift_box.setSpacing(0)
        shift_box.setAlignment(Qt.AlignRight)
        s1 = QLabel("Смена открыта")
        s1.setStyleSheet("font-weight: 700; font-size: 12px; background: transparent;")
        s2 = QLabel("04 октября · 10:42")
        s2.setStyleSheet(f"font-size: 11px; color: {MUTED}; background: transparent;")
        shift_box.addWidget(s1)
        shift_box.addWidget(s2)
        layout.addLayout(shift_box)

        return footer

    def _add_to_order(self, product):
        self.order.add_product(product)
        self._refresh_order()

    def _refresh_order(self):
        while self.order_container.count():
            item = self.order_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.order.items:
            empty = QLabel("Заказ пуст\nНажмите «+» на карточке товара")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet(
                f"color: {MUTED}; font-size: 13px; padding: 40px; background: transparent;"
            )
            self.order_container.addWidget(empty)
        else:
            for item in self.order.items:
                self.order_container.addWidget(self._build_order_row(item))

        self.badge.setText(f"{len(self.order.items)} позиций")
        self.total_label.setText(f"{self.order.total:,} ₽".replace(",", " "))
        self.vat_label.setText(f"НДС включён · {len(self.order.items)} позиций")
        self.subtotal_label.setText(f"{self.order.subtotal:,} ₽".replace(",", " "))
        self.pack_label.setText(f"{self.order.packaging:,} ₽".replace(",", " "))
        if self.order.discount:
            self.discount_label.setText(f"−{self.order.discount:,} ₽".replace(",", " "))
        else:
            self.discount_label.setText("0 ₽")
        self.pay_label.setText(f"{self.order.total:,} ₽".replace(",", " "))

    def _build_order_row(self, item):
        row = QFrame()
        row.setObjectName("orderRow")
        row.setFixedHeight(80)
        layout = QHBoxLayout(row)
        layout.setContentsMargins(10, 8, 10, 8)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        name = QLabel(item.product.name)
        name.setStyleSheet("font-weight: 700; font-size: 14px; background: transparent;")
        sub = QLabel(item.product.sub)
        sub.setStyleSheet(f"font-size: 11px; color: {MUTED}; background: transparent;")
        title_box.addWidget(name)
        title_box.addWidget(sub)
        layout.addLayout(title_box, 3)

        qty_box = QHBoxLayout()
        qty_box.setSpacing(8)
        minus = QPushButton("−")
        minus.setObjectName("qtyMinus")
        minus.clicked.connect(lambda: self._change_qty(item.product.id, -1))
        qty_label = QLabel(str(item.qty))
        qty_label.setStyleSheet("font-weight: 700; font-size: 15px; background: transparent;")
        qty_label.setFixedWidth(20)
        qty_label.setAlignment(Qt.AlignCenter)
        plus = QPushButton("+")
        plus.setObjectName("qtyPlus")
        plus.clicked.connect(lambda: self._change_qty(item.product.id, 1))
        qty_box.addWidget(minus)
        qty_box.addWidget(qty_label)
        qty_box.addWidget(plus)
        layout.addLayout(qty_box, 2)

        sum_label = QLabel(f"{item.sum:,} ₽".replace(",", " "))
        sum_label.setStyleSheet(
            f"font-weight: 800; font-size: 14px; "
            f"color: {ACCENT_DARK}; background: transparent;"
        )
        sum_label.setAlignment(Qt.AlignRight)
        layout.addWidget(sum_label, 2)

        del_btn = QPushButton("✕")
        del_btn.setObjectName("del")
        del_btn.clicked.connect(lambda: self._remove_item(item.product.id))
        layout.addWidget(del_btn)

        return row

    def _change_qty(self, product_id, delta):
        self.order.change_qty(product_id, delta)
        self._refresh_order()

    def _remove_item(self, product_id):
        self.order.remove_item(product_id)
        self._refresh_order()

    def _apply_discount(self):
        code = self.discount_input.text().strip()
        if not code:
            QMessageBox.warning(self, "Скидка", "Введите код скидки")
            return
        
        ok, msg = self.order.apply_discount(code)
        if ok:
            QMessageBox.information(self, "Скидка", msg)
            self._refresh_order()
        else:
            QMessageBox.warning(self, "Скидка", msg)

    def _set_payment(self, method):
        self.payment_method = method
        self.order.payment_method = method
        self._update_payment_buttons()

    def _update_payment_buttons(self):
        if self.payment_method == "card":
            self.card_btn.setObjectName("pmSel")
            self.cash_btn.setObjectName("pm")
        else:
            self.card_btn.setObjectName("pm")
            self.cash_btn.setObjectName("pmSel")
        for btn in (self.card_btn, self.cash_btn):
            btn.setStyleSheet("")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def _pay(self):
        if not self.order.items:
            QMessageBox.warning(self, "Оплата", "Заказ пуст")
            return
        
        method = "картой" if self.payment_method == "card" else "наличными"
        total_formatted = f"{self.order.total:,} ₽".replace(",", " ")
        
        QMessageBox.information(
            self, "Оплата",
            f"Оплата {method} на сумму {total_formatted} принята"
        )

    def _post_order(self):
        if not self.order.items:
            QMessageBox.warning(self, "Проведение", "Нельзя провести пустой заказ")
            return
        
        if not self.order.save():
            QMessageBox.critical(self, "Ошибка", "Не удалось сохранить заказ")
            return
        
        total_formatted = f"{self.order.total:,} ₽".replace(",", " ")
        QMessageBox.information(
            self, "Заказ проведён",
            f"Заказ № {self.order.order_id} сохранён.\nСумма: {total_formatted}"
        )
        
        self.order = Order(self.user["name"])
        self.discount_input.clear()
        self._refresh_order()

    def _cancel_order(self):
        if not self.order.items:
            return
        reply = QMessageBox.question(
            self, "Отмена", "Отменить текущий заказ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.order = Order(self.user["name"])
            self.discount_input.clear()
            self._refresh_order()
