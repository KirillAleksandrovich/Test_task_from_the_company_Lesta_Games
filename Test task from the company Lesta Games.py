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


def obrabotat_tekst(tekst):
    """
    Обрабатывает исходный текст:
    1. Приводит к нижнему регистру
    2. Удаляет все символы, кроме букв и цифр
    3. Разбивает на отдельные слова

    Аргументы:
        tekst (str): Исходный текст из файла

    Возвращает:
        list: Список очищенных слов в нижнем регистре
    """
    # \b - граница слова, \w+ - одно или больше букв/цифр
    slova = re.findall(r'\b\w+\b', tekst.lower())
    return slova


def vichislit_tf(spisok_slov):
    """
    Вычисляет частоту терминов (TF - Term Frequency):
    Сколько раз каждое слово встречается в тексте

    Аргументы:
        spisok_slov (list): Список слов из текста

    Возвращает:
        defaultdict: Словарь {слово: количество_повторений}
    """
    # defaultdict автоматически инициализирует счётчик для новых слов
    chastota_slov = defaultdict(int)

    for slovo in spisok_slov:
        chastota_slov[slovo] += 1  # Увеличиваем счётчик для каждого слова

    return chastota_slov