# Импорт необходимых библиотек
from flask import Flask, render_template, request, redirect, url_for  # Flask и его компоненты
import os  # Для работы с файловой системой
import re  # Для регулярных выражений (очистка текста)
import math  # Для математических операций (логарифм для IDF)
from collections import defaultdict  # Для удобного подсчёта частот слов

# Создаём основное приложение Flask
app = Flask(__name__)

# Конфигурация: папка для загрузки файлов
app.config['UPLOAD_FOLDER'] = 'zagruzki'

# Создаём папку для загрузок, если её нет
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])