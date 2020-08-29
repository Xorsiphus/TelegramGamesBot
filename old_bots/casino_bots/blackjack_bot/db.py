import mysql.connector

# Импортируем библиотеку для работы с .env файлом
import os
from dotenv import load_dotenv

# Указываем путь к .env файлу
env_path = '../../.env'
# Считываем токен из .env файла
load_dotenv(dotenv_path=env_path)
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

mydb = mysql.connector.connect(
    host="localhost",
    user=db_user,
    passwd=db_password,
    auth_plugin='mysql_native_password'
)

# class CasinoDatabase:
#    def __init__(self):
#       self.__hz = 1
