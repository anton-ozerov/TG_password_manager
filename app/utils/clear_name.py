from html import escape


def clean_text(text: str) -> str:
    """Экранируем обратный апостроф ` и применяем escape() для форматирования HTML"""
    return escape(text).replace('`', '&#96;')
