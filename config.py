# -*- coding: utf-8 -*-
import json
import os
import re

from termcolor import colored

token = input('Введите "Vk Admin" токен: ')
prefix_input = input('Введите префиксы, перечисленные через запятую (если хотите чтобы команды работали «Нд пинг», то вводите "Нд " с пробелом, если же без, то «Нд», и чтобы команды работали с "Нд" и "нд", то укажите префиксы в двух регистрах.): ')
file_name = 'token.json'
file_name2 = 'prefixes.json'

prefixes = re.findall(r'[^\s,][^,]*', prefix_input)

if not os.path.exists(file_name):
    with open(file_name, 'w') as f:
        json.dump({}, f)
        print(colored('Файл для токена создан.', 'green'))

with open(file_name, "w") as fh:
    json.dump(f"{token}", fh)
    print(colored('Токен записан.', 'red'))

if not os.path.exists(file_name2):
    with open(file_name2, 'w') as f:
        json.dump(None, f)
        print(colored('Файл для префиксов создан.', 'green'))

with open(file_name2, "w") as fh:
    json.dump(prefixes, fh)
    print(colored('Префиксы записаны.', 'red'))