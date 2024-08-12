import os

from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
# BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
# ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# SUPERADMINS = env.list("SUPERADMINS")  # adminlar ro'yxati

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Bot toekn
ADMINS = os.getenv("ADMINS")  # adminlar ro'yxati
SUPERADMINS = os.getenv("SUPERADMINS")  # adminlar ro'yxati

# IP = env.str("ip")  # Xosting ip manzili
IP = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# for database
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
