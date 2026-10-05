
# theme.py
BG = "#fcc6d9"
PANEL_PINK = "#f8bbd0"
WHITE = "#ffffff"
ACCENT = "#e91e63"
ACCENT_DARK = "#a3104f"
SOFT = "#ffe4ee"
TEXT = "#5a3a36"
MUTED = "#9a7f80"
LILAC = "#cdb4ee"
MINT = "#a8dcd6"
MINT_TEXT = "#3b8a85"
GREY_BTN = "#e8e1de"
LINE = "#dcd2d2"

FONT_HEAD = "Comfortaa"
FONT_BODY = "Nunito"


def get_stylesheet():
    return f"""
    QWidget {{
        font-family: "{FONT_BODY}";
        color: {TEXT};
        font-size: 14px;
    }}
    QMainWindow, QDialog {{ background: {WHITE}; }}

    QLabel#h1 {{ font-family: "{FONT_HEAD}"; font-size: 26px; font-weight: 700; color: {ACCENT_DARK}; }}
    QLabel#h2 {{ font-family: "{FONT_HEAD}"; font-size: 24px; font-weight: 500; color: {ACCENT_DARK}; }}
    QLabel#h3 {{ font-family: "{FONT_HEAD}"; font-size: 17px; font-weight: 500; color: {ACCENT_DARK}; }}
    QLabel#muted {{ color: {MUTED}; font-size: 12px; }}
    QLabel#total {{ font-family: "{FONT_HEAD}"; font-size: 40px; font-weight: 700; color: {ACCENT_DARK}; }}

    /* Фоны экранов */
    QWidget#cashierScreen {{ background: {BG}; }}
    QWidget#loginScreen   {{ background: {BG}; }}
    QWidget#adminScreen   {{ background: {BG}; }}

    /* Шапка и подвал */
    QFrame#header {{ background: {WHITE}; border: none; }}
    QFrame#footer {{ background: {WHITE}; border: none; }}

    /* Панели */
    QFrame#orderPanel   {{ background: {WHITE};      border-radius: 28px; }}
    QFrame#summaryPanel {{ background: {PANEL_PINK}; border-radius: 28px; }}
    QFrame#productCard  {{ background: {WHITE};      border-radius: 16px; }}

    /* Кнопки */
    QPushButton {{
        background: {WHITE}; color: {TEXT}; border: none;
        border-radius: 999px; padding: 10px 18px;
        font-weight: 700; font-size: 14px;
    }}
    QPushButton:hover {{ background: {SOFT}; }}
    QPushButton#accent {{ background: {ACCENT}; color: {WHITE}; }}
    QPushButton#accent:hover {{ background: {ACCENT_DARK}; }}
    QPushButton#lilac {{ background: {LILAC}; color: {WHITE}; }}
    QPushButton#mint {{ background: {MINT}; color: {MINT_TEXT}; }}
    QPushButton#grey {{ background: {GREY_BTN}; color: {TEXT}; }}
    QPushButton#addBtn {{
        background: {ACCENT}; color: {WHITE}; border-radius: 20px;
        min-width: 40px; min-height: 40px; font-size: 22px; padding: 0;
    }}
    QPushButton#addBtn:hover {{ background: {ACCENT_DARK}; }}
    QPushButton#qtyMinus {{
        background: {SOFT}; color: {ACCENT}; border-radius: 14px;
        min-width: 28px; min-height: 28px; padding: 0; font-size: 15px;
    }}
    QPushButton#qtyPlus {{
        background: {ACCENT}; color: {WHITE}; border-radius: 14px;
        min-width: 28px; min-height: 28px; padding: 0; font-size: 16px;
    }}
    QPushButton#del {{
        background: {SOFT}; color: {ACCENT}; border-radius: 14px;
        min-width: 28px; min-height: 28px; padding: 0; font-size: 12px;
    }}
    QLineEdit {{
        background: {WHITE}; border: 1px solid {LINE};
        border-radius: 14px; padding: 10px 14px; font-size: 14px;
    }}
    QLineEdit:focus {{ border: 2px solid {ACCENT}; }}

    QPushButton#tab {{
        background: {WHITE}; color: {TEXT}; border-radius: 999px;
        padding: 10px 18px; font-weight: 700; font-size: 12px;
    }}
    QPushButton#tabActive {{
        background: {ACCENT}; color: {WHITE}; border-radius: 999px;
        padding: 10px 18px; font-weight: 700; font-size: 12px;
    }}
    QPushButton#pm {{
        background: {SOFT}; color: {TEXT}; border-radius: 999px;
        padding: 10px; font-weight: 700; font-size: 12px;
    }}
    QPushButton#pmSel {{
        background: {WHITE}; color: {ACCENT_DARK};
        border: 2px solid {ACCENT}; border-radius: 999px;
        padding: 8px; font-weight: 700; font-size: 12px;
    }}
    QScrollArea {{ border: none; background: transparent; }}
    QScrollBar:vertical {{ background: transparent; width: 8px; border-radius: 4px; }}
    QScrollBar::handle:vertical {{ background: {ACCENT}; border-radius: 4px; min-height: 30px; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    """
