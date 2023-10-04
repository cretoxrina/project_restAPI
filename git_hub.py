from github import Github
import os
from file import File
import requests
import json


class Push: # Этот класс предназначен для отправки файла в репозиторий
    @staticmethod
    def push(file_path): 
        GITHUB_TOKEN = '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' #Я создал этот токенвгите
        github = Github(GITHUB_TOKEN) 
        repo_owner = 'cretoxrina' # Это имя пользователя 
        repo_name = 'restAPI' # Это имя репозиторий
        repo = github.get_user(repo_owner).get_repo(repo_name) # Передаем через методы 
        commit_message = f'Add {file_path}' # Это коммит выдает сообщение
        branch_name = 'main'   # В какой ветви будет находится файл
        with open(file_path, 'r') as file: # Открываем и читаем файл 
            file_content = file.read()
        repo.create_file(file_path, commit_message, file_content, branch_name) # Создаем файл уже в репозиторий

class Get_Api:

    @staticmethod
    def get_api(fname):
        GITHUB_TOKEN = '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'
        repo_owner = 'cretoxrina'
        repo_name = 'restAPI'
        file_path = fname
        branch_name = 'main'
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={branch_name}' # Это апишка гитхаба, не использовал параметры, все данные в заключены до endpoit 
        headers = {'Authorization': f'token {GITHUB_TOKEN}'} # Это хэдер как мы будем извлекать данные 
        response = requests.get(url, headers=headers) # уже сам респонс, как видите параметра нет key:value, есть только хэдер который будет извлекать 

        if response.status_code == 200: # проверка если пройдет то нам выдадут эти данные
            file_content = response.json()['content']
            import base64
            decoded_content = base64.b64decode(file_content).decode('utf-8') # декодируем

            try:
                data_dict = json.loads(decoded_content) # Перехватые, сериализируем в формат колекшн
                print('File Content as JSON:', data_dict) # и принтуем
            except json.JSONDecodeError as e:
                print('Failed to decode JSON content:', e)
        else:
            print('Invalid request. Status code:', response.status_code)


