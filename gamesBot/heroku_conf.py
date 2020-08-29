"""
Настройка для Heroku.
"""
import os

if_heroku = ""

if os.environ.get('HEROKU'):
    if_heroku = "gamesBot/"
