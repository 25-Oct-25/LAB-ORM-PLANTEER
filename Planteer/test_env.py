import os
from dotenv import load_dotenv

load_dotenv()  # تحميل المتغيرات من .env

print("EMAIL_HOST_USER =", os.getenv("EMAIL_HOST_USER"))
print("EMAIL_HOST_PASSWORD =", os.getenv("EMAIL_HOST_PASSWORD"))
print("DEBUG =", os.getenv("DEBUG"))
