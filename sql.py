import sqlite3


# это класс ДБ здесь не полноценная CRUD система, но для задачи он полностью выполняет 
class DataBase:

    def create_table(self):
        try: 
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            # cur.execute('''drop table if exists Data''')
            cur.execute(''' 
                create table if not exists Data (id integer primary key, Email text, Subject text, Message text)
            ''')
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print('Invalid creation:', err)

    def insert_data(self, Email, Subject, Message=''): # Здесь мы вставляем данные в БД
        try:
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute('''
                insert into Data (Email, Subject, Message)
                values (?, ?, ?)
            ''', (Email, Subject, Message))
            con.commit()
            con.close()
        except sqlite3.Error as err:
            print('Invalid insertion:', err) # Использовал Трай и Эксепт чтобы ловить ошибки и оттуда решать саму задачу
    
    def invoke_data(self, Email):
        try:
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute('''
                select Email, Subject, Message from Data where Email = ?
            ''', (Email,))
            data = cur.fetchone() # Самая интересная часть это СЕЛЕКТ
            con.close()
            if data is not None:# Проверяю данные не пусты, затем их превращаю в кортеж, затем в словарь для будущей сериализаций
                email, subject, message = data
                json_format = {
                    "to": email,
                    "subject": subject,
                    "message": message
                }
                return json_format # Возвращаю в формате словаря 
            else:
                print('No data was invoked for Email:', Email)
                return None

        except sqlite3.Error as err:
            print('Failed to select data:', err)

# db = DataBase()  ЗДЕСЬ Я ПРОСТО ПРОВЕРЯЛ РАБОТАЕТ ИЛИ НЕТ
# db.create_table()
# db.insert_data('sa@gmail.com', 'hello', 'hello mommy')
# result = db.invoke_data('sa@gmail.com')
# print(result)
