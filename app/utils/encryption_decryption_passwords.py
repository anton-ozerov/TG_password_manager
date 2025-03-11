import bcrypt


async def hash_password(password: str) -> str:
    """Получает незахэшированный пароль, возвращает хэшированный результат декодированный в str"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def check_password(password: str, hashed_password: str) -> bool:
    """Получает введённый пароль, захэшированный пароль. Возвращает True, если пароль верный. Иначе - False."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
