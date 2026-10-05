
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal

from theme import BG, WHITE, ACCENT, ACCENT_DARK, SOFT, TEXT, MUTED, FONT_HEAD
from logic.storage import load_users


class LoginScreen(QWidget):
    logged_in = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setObjectName("loginScreen")     # ← ИСПРАВЛЕНО
        self.selected_role = "cashier"
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedSize(420, 520)
        card.setStyleSheet(f"QFrame {{ background: {WHITE}; border-radius: 28px; }}")
        outer.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(14)

        logo = QLabel("🍰")
        logo.setAlignment(Qt.AlignCenter)
        logo.setMinimumHeight(90)
        logo.setStyleSheet("font-size: 64px; background: transparent;"
                           "padding-bottom: 36px;"
                           )
        layout.addWidget(logo)

        title = QLabel("Ева-Мишлен")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            f'font-family: "{FONT_HEAD}"; font-size: 28px; font-weight: 700; '
            f'color: {ACCENT_DARK}; background: transparent;'
        )
        layout.addWidget(title)

        subtitle = QLabel("Войдите в систему")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 13px; background: transparent;")
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        role_label = QLabel("Роль:")
        role_label.setStyleSheet(f"color: {TEXT}; font-weight: 700; background: transparent;")
        layout.addWidget(role_label)

        role_row = QHBoxLayout()
        role_row.setSpacing(8)
        self.role_buttons = {}
        for role_key, role_text in [("cashier", "🧑‍🍳 Кассир"), ("admin", "👑 Админ")]:
            btn = QPushButton(role_text)
            btn.setCheckable(True)
            btn.setStyleSheet(self._role_style(role_key == self.selected_role))
            btn.clicked.connect(lambda checked, r=role_key: self._select_role(r))
            role_row.addWidget(btn)
            self.role_buttons[role_key] = btn
        layout.addLayout(role_row)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        layout.addSpacing(10)

        login_btn = QPushButton("Войти")
        login_btn.setObjectName("accent")
        login_btn.setFixedHeight(50)
        login_btn.clicked.connect(self._try_login)
        layout.addWidget(login_btn)

        layout.addStretch()

        hint = QLabel("Демо-доступ:\ncashier / 123\nadmin / admin")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"color: {MUTED}; font-size: 11px; background: transparent;")
        layout.addWidget(hint)

    def _role_style(self, active):
        if active:
            return (f"QPushButton {{ background: {ACCENT}; color: {WHITE}; "
                    f"border-radius: 999px; padding: 10px; font-weight: 700; font-size: 13px; }}")
        return (f"QPushButton {{ background: {SOFT}; color: {TEXT}; "
                f"border-radius: 999px; padding: 10px; font-weight: 700; font-size: 13px; }}")

    def _select_role(self, role):
        self.selected_role = role
        for key, btn in self.role_buttons.items():
            btn.setStyleSheet(self._role_style(key == role))

    def _try_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        users = load_users()
        for user in users:
            if user["login"] == login and user["password"] == password:
                if user["role"] != self.selected_role:
                    QMessageBox.warning(
                        self, "Ошибка",
                        f"Пользователь {login} не имеет роли «{self.selected_role}»"
                    )
                    return
                self.logged_in.emit(user)
                return
        QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
