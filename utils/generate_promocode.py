import string
import random
from datetime import datetime


async def create_promocode():
    """
    Takrorlanmaydigan promo-kod yaratish uchun funksiya
    """
    characters = string.ascii_uppercase + string.digits
    promocode = ''.join(random.choice(characters) for _ in range(6))
    print('promocode', promocode)
    return promocode
