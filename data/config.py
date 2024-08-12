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
IP = os.getenv("BOT_IP", "localhost")

# for database
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
# DB_HOST = env.str("DB_HOST")
