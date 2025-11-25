import sqlite3
conn = sqlite3.connect('journals.db')
cursor = conn.cursor()

#Функция для добавления пользователя
def add_user(name,password,role):
    cursor.execute('INSERT INTO User (Name,Password,User_role_ID) VALUES (?,?,?)', (name,password,role))
    conn.commit()
    print("Вы зарегистрированы")
    quit()

#Функции для входа в систему
#Проверка пароля
def pass_check(passw,name):
    cursor.execute("SELECT Password FROM User WHERE Name = ?", (name,))
    parol = cursor.fetchone()
    if parol and parol[0]== passw:
        return True
    else:
        print('Неверный пароль')
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
    user_name = input('Имя пользователя(не более 15 символов): ')
    if len(user_name)>15:
        print("Слишком длинное имя")
        quit()
    cursor.execute("SELECT COUNT(*) FROM User WHERE Name = ?", (user_name,))
    result = cursor.fetchone()
    if result[0] == 1:
        print('Данное имя уже занято')
        quit()
    user_password = input('Придумайте пароль(не более 15 символов): ')
    if len(user_password)>15:
        print("Слишком длинный пароль")
        quit()
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
    if role[0] == 1:           #Действия читателя
        print('Вы читатель')
        reader_choice= int(input("Выберите действие:\n"
                                "1 - Прочитать статью\n"
                                "2 - Выйти из системы\n"))
        if reader_choice == 2:
            quit()
        if reader_choice!=1 and reader_choice!=2:
            print('Неверный ввод')
            quit()
        if reader_choice ==1:
            cursor.execute("SELECT Name FROM Journal")
            jour = cursor.fetchall()
            print('Выберите журнал:')
            i=0
            for j in jour:
                i+=1
                print(f'{i} - {j}')
            jour_choice = int(input('Выбранный журнал: '))
            if jour_choice>len(jour):
                print('Неверный ввод')
                quit()
            jour_name = jour[jour_choice-1]

            cursor.execute("SELECT Journal_ID FROM Journal WHERE Name = ?", (jour_name[0],))
            j_ID = cursor.fetchone()
            j_ID= j_ID[0]
            cursor.execute('SELECT Name FROM Article WHERE Journal_ID = ? AND Article_status_ID = ?',(j_ID,3))
            art = cursor.fetchall()
            print('Выберите статью:')
            a=0
            for j in art:
                a+=1
                print(f'{a} - {j}')
            art_choice = int(input('Выбранная статья: '))
            if art_choice>len(art):
                print('Неверный ввод')
                quit()
            art_name = art[art_choice-1]
            print(art_name)
            cursor.execute("SELECT Text FROM Article WHERE Name = ?", (art_name[0],))
            text = cursor.fetchall()
            for line in text:
                for i in line:
                    print (i, ' ', end = "")
                print ('\n')
            reader_choice2= int(input('Выберите действие:\n'
                                     '1 - Оценить статью\n'
                                     '2 - Выйти из системы\n'))
            if reader_choice2!=1 and reader_choice2!=2:
                print('Неверный ввод')
                quit()
            if reader_choice2==2:
                quit()
            if reader_choice2==1:
                rate=int(input('Оцените статью (от 1 до 10): '))
                if rate<1 or rate>10:
                    print('Неверный ввод')
                    quit()
                cursor.execute("SELECT Rating FROM Article WHERE Name = ?", (art_name[0],))
                last_rate = cursor.fetchone()
                last_rate= last_rate[0]
                if last_rate==0:
                    new_rate=rate
                else:
                    new_rate= (last_rate+rate)/2
                cursor.execute('UPDATE Article SET Rating = ? WHERE Name = ?', (new_rate, art_name[0]))  #Обновление рейтинга статьи
                conn.commit()
                print('Спасибо за оценку!')
                quit()


    elif role[0] ==2:      #Действия автора
        print('Вы автор')
        autor_choice= int(input("Выберите действие:\n"
              "1 - Подать заявку на публикацию статьи\n"
              "2 - Выйти из системы\n"))
        if autor_choice == 2:
            quit()
        if autor_choice!=1 and autor_choice!=2:
            print('Неверный ввод')
            quit()

        if autor_choice == 1:
            art_name = input('Название вашей статьи (не более 100 символов):')  #Ввод названия статьи
            if len(art_name)>100:
                print('Слишком длинный заголовок')
                quit()
            cursor.execute('SELECT Theme FROM Journal')
            jour_th = cursor.fetchall()
            print('Выберите тематику вашей статьи')
            i=0
            for j in jour_th:
                i+=1
                print(f'{i} - {j}')
            art_th=int(input('Тематика статьи: ')) #Ввод тематики статьи для выбора журнала
            if art_th>len(jour_th):
                print('Неверный ввод')
                quit()
            text = input("Прикрепите файл с текстом (Введите путь к файлу(без кавычек)):")
            with open(text, 'r',encoding='utf-8') as file:           #Чтение файла с текстом
                art_text = file.read()
            cursor.execute("SELECT User_ID FROM User WHERE Name = ?", (name,))
            au_ID = cursor.fetchone()
            #Добавление данных о статье в БД
            cursor.execute('INSERT INTO Article (Journal_ID,Name,Text,Rating,Date,Article_status_ID,User_ID) VALUES (?,?,?,?,?,?,?)', (art_th,art_name,art_text,0,'-',1,au_ID[0]))
            conn.commit()
            print('Заявка успешно подана!')
            quit()

    elif role[0] ==3:
        print('Вы администратор')
        admin_choice = int(input("Выберите действие:\n"
                                 "1 - Проверить заявки\n"
                                 "2 - Выйти из  системы\n"))
        if admin_choice == 2:
            quit()
        if admin_choice!=1 and admin_choice!=2:
            print('Неверный ввод')
            quit()

        if admin_choice==1:
            cursor.execute("SELECT COUNT(*) FROM Article WHERE Article_status_ID = ?", (1,))
            art_count = cursor.fetchone()
            if art_count[0] == 0:
                print('Заявок нет')
                conn.commit()
                quit()
            cursor.execute('SELECT Name FROM Article WHERE Article_status_ID = ?',(1,))
            arts = cursor.fetchall()
            print('Выберите статью на проверку')
            i=0
            for j in arts:
                i+=1
                print(f'{i} - {j}')
            art = int(input('Рассмотреть статью: '))
            art_check = arts[art-1]
            print(f'Название: {art_check}')
            cursor.execute('SELECT Journal_ID FROM Article WHERE Name = ?',(art_check[0],))
            th_ID = cursor.fetchone()
            th_ID= th_ID[0]
            cursor.execute('SELECT Theme FROM Journal WHERE Journal_ID = ?',(th_ID,))
            theme_check = cursor.fetchone()
            print(f'Тематика: {theme_check[0]}')
            cursor.execute('SELECT Text FROM Article WHERE Name = ?',(art_check[0],))
            text_check = cursor.fetchall()
            for line in text_check:
                for i in line:
                    print (i, ' ', end = "")
                print ('\n')
            admin_choice2= int(input('Выберите действие:\n'
                                     '1 - Отклонить статью\n'
                                     '2 - Опубликовать статью\n'))
            if admin_choice2!=1 and admin_choice2!=2:
                print('Неверный ввод')
                quit()
            if admin_choice2 == 1:
                cursor.execute('UPDATE Article SET Article_status_ID = ? WHERE Name = ?', (2, art_check[0]))  #Отклонение статьи
                conn.commit()
                print('Статья отклонена')
                quit()
            if admin_choice2 == 2:
                date = input('Введите сегодняшнюю дату(xx.xx.xxxx): ')
                cursor.execute('UPDATE Article SET Article_status_ID = ? WHERE Name = ?', (3, art_check[0])) #Публикация статьи
                cursor.execute('UPDATE Article SET Date = ? WHERE Name = ?', (date, art_check[0]))
                conn.commit()
                print('Статья опубликована')
                quit()