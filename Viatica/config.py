# import os
# from dotenv import load_dotenv
# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")


import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

mydb = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

