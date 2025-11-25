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
    Text TEXT NOT NULL,
    Article_status_ID INTEGER NOT NULL,
    FOREIGN KEY(Journal_ID) REFERENCES Journal (journal_ID),
    FOREIGN KEY(User_ID) REFERENCES User (User_ID),
    FOREIGN KEY(Article_status_ID) REFERENCES Article_status (Article_status_ID)
)
''')
#cursor.execute('INSERT INTO User_role (Name,Comment) VALUES (?, ?)', ('Читатель', 'Чтение и оценка статей'))
#cursor.execute('INSERT INTO User_role (Name,Comment) VALUES (?, ?)', ('Автор', 'Отправление статей'))
#cursor.execute('DELETE FROM Journal WHERE Name="Фактограф"')
#cursor.execute('SELECT * FROM User')
#users = cursor.fetchall()
#print(users)
'''
cursor.execute('INSERT INTO Journal (Name,Theme) VALUES (?, ?)', ('Арт-навигатор', 'Культура и искусство'))
cursor.execute('INSERT INTO Journal (Name,Theme) VALUES (?, ?)', ('Чемпион', 'Спорт'))
cursor.execute('INSERT INTO Journal (Name,Theme) VALUES (?, ?)', ('Хиханьки-хаханьки', 'Развлекательное'))
cursor.execute('INSERT INTO Journal (Name,Theme) VALUES (?, ?)', ('В мире науки', 'Научно-популярное'))
cursor.execute('INSERT INTO Journal (Name,Theme) VALUES (?, ?)', ('Фактограф', 'Общественно-политическое'))
'''
'''
cursor.execute('INSERT INTO Article_status (Name,Comment) VALUES (?, ?)', ('На рассмотрении', 'Статья передана на рассмотрение'))
cursor.execute('INSERT INTO Article_status (Name,Comment) VALUES (?, ?)', ('Статья отклонена', 'Статья не прошла проверку'))
cursor.execute('INSERT INTO Article_status (Name,Comment) VALUES (?, ?)', ('Статья опубликована', 'Статья прошла проверку и опубликована'))
'''

cursor.execute('SELECT * FROM Article ')
text  = cursor.fetchall()
print(text)
conn.commit()