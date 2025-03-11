import secrets
import string


async def generate_password(length: int = 15, uppercase: bool = True,
                            digits: bool = True, punctuation: bool = True) -> str:
    """Генерация пароля. Максимальная длина - 50 символов, минимальная - 1"""
    if length > 50:
        length = 50
    elif length < 1:
        length = 1

    alphabet = string.ascii_lowercase
    alphabet += string.ascii_uppercase if uppercase else ''
    alphabet += string.digits if digits else ''
    alphabet += string.punctuation if punctuation else ''

    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password
