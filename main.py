from github import Github
import requests
from file import File
from typing import Any
from sql import DataBase
from git_hub import Push
from git_hub import Get_Api


MIN_CHOICE = 1
MAX_CHOICE = 4
SEND = 1
SHOW_EMAIL = 2
JOKE = 3
EXIT = 4


def main():
    url = 'https://icanhazdadjoke.com/'  # Шутки с интернета 
    db = DataBase() # создаю Таблицу базы данных 
    db.create_table()
    choice = 0
    while choice != EXIT: # Цикл будет идти пока вы не захотите выйти с меню
        display_menu()
        choice = get_choice()
        if choice == SEND:
            to = str(input('Enter an email you want to send: '))
            subject = str(input('Enter a subject: '))
            message = str(input('Enter a message: '))
            to = check_email(to)
            if to is not None:
                db.insert_data(to,subject,message)
                fname = to.split('@')
                file_name = fname[0] + '.txt'
                fname = File(file_name)
                fname.create_file(to)
                Push.push(file_name)
                print(f'File - {file_name} was succesfully sended to github')
            else:
                print('It is None')
        elif choice == SHOW_EMAIL:
            email = str(input('Enter an email to see what you sent: '))
            email = check_email(email)
            if email:
                output = email.split('@')
                output_get = output[0] 
                output_get = output_get + '.txt'
                print(Get_Api.get_api(output_get))
            else:
                print('Invalid email')
                

        elif choice == JOKE:
            print('---- ---- ----')
            joke = get(url)
            print(joke)
            print('---- ---- ----')

            
                






def display_menu(): # Меню, изначально думал что буду использовать для меню структуру данных Stack, но структура меню не сложная
    print('1 - Send a message')
    print('2 - Show messages')
    print('3 - Show me joke') 
    print('4 - Exit')

def get_choice(): # здесь идет валидация выбора, как видите у нас есть константы, взяв их проверяем
    choice = int(input('Enter your choice: '))
    while choice < MIN_CHOICE or choice > MAX_CHOICE:
        print('Possible variants are between {} and {}'.format(MIN_CHOICE,MAX_CHOICE))
        choice = int(input('Enter your choice: '))
    return choice 

def check_email(email): # здесь мы проверяем сам почту
    if email.count('@') == 1:
        new_email = email.split('@')
        if 3 < len(new_email[0]) < 20 and 5 < len(new_email[1]) < 15:
            return email
    return None

def requestURL(baseurl, d={}): # ЭТО БОНУС, как вы заметили есть третий пункт, где если нажать вам генерирует шутку с сайта. Использую его апишку я сдела такой вот маленький презент
    req = requests.Request(method='GET', url=baseurl,params=d) # тут есть параметр но он пустой
    prepped = req.prepare()
    return prepped.url # мы просто возвращаем ссылку чтобы проверить что он сгенерировал

def get(baseurl):
    if isinstance(baseurl,str): # здесь мы проверям является ли стрингом ссылка
        page = requestURL(baseurl) # если да то рекуестим
        response = requests.get(page, headers={'Accept': 'text/plain'})
    
    
    if response.status_code == 200:
        joke = response.text
        return joke


if __name__ == "__main__":
    main()