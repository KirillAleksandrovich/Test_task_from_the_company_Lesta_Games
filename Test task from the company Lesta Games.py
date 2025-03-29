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


def vichislit_idf(spisok_slov, tf_slovar):
    """
    Вычисляет обратную частоту документов (IDF - Inverse Document Frequency):
    Показывает, насколько слово редкое во всём тексте

    Аргументы:
        spisok_slov (list): Исходный список всех слов
        tf_slovar (dict): Словарь с частотами слов (результат TF)

    Возвращает:
        dict: Словарь {слово: значение_IDF}
    """
    idf_slovar = {}
    vsego_slov = len(spisok_slov)  # Общее количество слов в тексте
    unikalnye_slova = set(spisok_slov)  # Уникальные слова

    for slovo in unikalnye_slova:
        # Формула IDF: логарифм (общее_число_слов / частота_слова)
        # Чем больше IDF, тем редче слово
        idf_slovar[slovo] = math.log(vsego_slov / tf_slovar[slovo])

    return idf_slovar


@app.route('/', methods=['GET', 'POST'])
def zagruzit_fayl():
    """
    Основная функция обработки запросов:
    1. GET: Показывает форму загрузки
    2. POST: Обрабатывает загруженный файл
    """
    if request.method == 'POST':
        # Проверяем, есть ли файл в запросе
        if 'fayl' not in request.files:
            return redirect(request.url)  # Если нет - перезагружаем страницу

        fayl = request.files['fayl']

        # Проверяем, что файл выбран
        if fayl.filename == '':
            return redirect(request.url)

        # Если файл корректный
        if fayl:
            # Сохраняем файл в папку загрузок
            put_k_faylu = os.path.join(app.config['UPLOAD_FOLDER'], fayl.filename)
            fayl.save(put_k_faylu)

            # Читаем содержимое файла
            with open(put_k_faylu, 'r', encoding='utf-8') as f:
                tekst = f.read()

            # Обрабатываем текст
            slova = obrabotat_tekst(tekst)

            # Вычисляем метрики
            tf = vichislit_tf(slova)
            idf = vichislit_idf(slova, tf)

            # Сортируем слова по IDF (по убыванию) и берём топ-50
            otsortirovannye_slova = sorted(idf.items(), key=lambda x: x[1], reverse=True)[:50]

            # Передаём данные в шаблон result.html
            return render_template('result.html', slova=otsortirovannye_slova, tf=tf)

    # Для GET-запросов показываем форму загрузки
    return render_template('upload.html')


if __name__ == '__main__':
    # Добавляем папку static для логотипа
    app.config['STATIC_FOLDER'] = 'static'
    if not os.path.exists(app.config['STATIC_FOLDER']):
        os.makedirs(app.config['STATIC_FOLDER'])
    # Запускаем сервер в режиме отладки
    app.run(debug=True)