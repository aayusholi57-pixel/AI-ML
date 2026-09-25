import os
from dotenv import load_dotenv

load_dotenv()
print("Redis URL:", os.getenv("redis_url"))
print("port:", os.getenv("PORT"))