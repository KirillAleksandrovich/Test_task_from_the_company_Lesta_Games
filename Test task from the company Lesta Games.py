# Импорт необходимых библиотек
from flask import Flask, render_template, request, redirect, url_for  # Flask и его компоненты
import os  # Для работы с файловой системой
import re  # Для регулярных выражений (очистка текста)
import math  # Для математических операций (логарифм для IDF)
from collections import defaultdict  # Для удобного подсчёта частот слов

