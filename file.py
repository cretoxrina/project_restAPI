import json
from typing import Any
from sql import DataBase

class File: # Моя самая любимая часть, не использовал дескрипторы или декораторы для доступа к атрибуту класса 
    MAX = 25 # Это константы атрибуты класса так же атрибуты обьекта класса, их ни в коем случае не даю менять 
    MIN = 3
    types = {'name': str}
    dataBase = DataBase()

    def __init__(self, name: str):
        self.name = name

    def __setattr__(self, name, value): # Использовал dunder methods с ними намного легче, в шапке класса есть словарь где есть данные которые могут инициализироваться, проверяю их через это
        if name in self.types and type(value) == self.types[name]:
            super().__setattr__(name, value)# Наследует от суперкласса 
        else:
            raise TypeError('Error inserting')


    def __getattribute__(self, name: str): # Тут просто возвращает атрибут, если мы ссылаемся к нему
        return super().__getattribute__(name)

    def __getattr__(self, name: str): # 3 метод из 4, который действительно полезный, если мы будем ссылаться к несуществующему атрибуту, то возвращает ответ что его не существуют
        return f'there is no such kind of file {name}'

    def get_json_format(self, email): # Это метод который извлекает данные в JSON формате, затем сериализирует в формат Строки
        json_format = self.dataBase.invoke_data(email)
        return json.dumps(json_format, indent=2)

    def create_file(self, data): # Тут мы создаем файл чтобы в дальнейшим постить его 
        fname = self.check_text(self.name) # проверяем через classmethod является ли валидным текст, по сути бесполезный метод, его можно было записать в магическом методе сетаатр
        fname = fname
        try:
            with open(fname, 'w') as file: # открываем файл и затем пишем в виде строки JSON формат
                result = self.get_json_format(data)
                file.write(result)
        except Exception as e:
            print('Error creating file:', e)

    @classmethod
    def check_text(cls, name): # Это тот класс о которым мы говорили, бесполезный но одновременно полезный 
        if len(name) < cls.MIN or len(name) > cls.MAX:
            raise TypeError('Invalid text length, must be between 3 and 20')
        return name


        
        