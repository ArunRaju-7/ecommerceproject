import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('DB_NAME'))
print(os.getenv('DB_USER'))
print(os.getenv('DB_PASSWORD'))
print(os.getenv('DB_HOST'))