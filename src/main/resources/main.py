import sqlite3
conn = sqlite3.connect('journals.db')
cursor = conn.cursor()

#Таблица Journals
cursor.execute('''
CREATE TABLE IF NOT EXISTS Journal (
    journal_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Theme TEXT NOT NULL
)
''')
#Таблица User_role
cursor.execute('''
CREATE TABLE IF NOT EXISTS User_role (
    User_role_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Comment TEXT NOT NULL
)
''')
#Таблица User
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    User_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Password TEXT NOT NULL,
    User_role_ID INTEGER NOT NULL,
    FOREIGN KEY(User_role_ID) REFERENCES User_role (User_role_ID)
)
''')

#Таблица Article_status
cursor.execute('''
CREATE TABLE IF NOT EXISTS Article_status (
    Article_status_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Comment TEXT NOT NULL
)
''')

#Таблица Article
cursor.execute('''
CREATE TABLE IF NOT EXISTS Article (
    Article_ID INTEGER PRIMARY KEY,
    Journal_ID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    User_ID INTEGER NOT NULL,
    Rating REAL NOT NULL,
    Date TEXT NOT NULL,
    Article_status_ID INTEGER NOT NULL,
    FOREIGN KEY(Journal_ID) REFERENCES Journal (journal_ID),
    FOREIGN KEY(User_ID) REFERENCES User (User_ID),
    FOREIGN KEY(Article_status_ID) REFERENCES Article_status (Article_status_ID)
)
''')


#cursor.execute('INSERT INTO User_role (Name,Comment) VALUES (?, ?)', ('Читатель', 'Чтение и оценка статей'))
#cursor.execute('INSERT INTO User_role (Name,Comment) VALUES (?, ?)', ('Автор', 'Отправление статей'))
#cursor.execute('INSERT INTO User_role (Name,Comment) VALUES (?, ?)', ('Администратор', 'Проверка статей'))
#cursor.execute('SELECT * FROM User_role')
#users = cursor.fetchall()
#print(users)
#conn.commit()



#Функция для добавления пользователя
def add_user(name,password,role):
    cursor.execute('INSERT INTO User (Name,Password,User_role_ID) VALUES (?,?,?)', (name,password,role))
    conn.commit()



#Функции для входа в систему
#Проверка пароля
def pass_check(passw,name):
    cursor.execute("SELECT Password FROM User WHERE Name = ?", (name,))
    parol = cursor.fetchone()
    if parol and parol[0]== passw:
        return True
    else:
        print(parol,passw)
        return False
#Проверка имени пользователя
def login(name):
    cursor.execute("SELECT COUNT(*) FROM User WHERE Name = ?", (name,))
    result = cursor.fetchone()
    if result[0]>0:
        password = input('Введите пароль: ')
        if pass_check(password,name)==True:
            return True
        else:
            quit()

    else:
        print("Пользователь не найден")
        quit()




choice1 = int(input("Выберите действие:\n"
          "1. Создание аккаунта\n"
          "2. Вход в систему\n"))
if choice1 == 1:
    user_name = input('Имя пользователя: ')
    user_password = input('Придумайте пароль: ')
    user_role = int(input('Кто вы?\n'
                      '1 - Читатель\n'
                      '2 - Автор\n'
                      '3 - Администратор\n'))
    if user_role !=1 and user_role!=2 and user_role!=3:
        print('Неверный ввод')
        quit()
    add_user(user_name,user_password,user_role)
elif choice1 == 2:
    name = input("Введите имя пользователя: ")
    verif = login(name)
else:
    print("Неверный ввод")
    quit()

if verif ==True:
    cursor.execute("SELECT User_role_ID FROM User WHERE Name = ?", (name,))
    role = cursor.fetchone()
    if role[0] == 1:
        print('Вы читатель')
    elif role[0] ==2:
        print('Вы автор')
    elif role[0] ==3:
        print('Вы администратор')

