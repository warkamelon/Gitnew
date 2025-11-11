"""
import json
import csv
import xml.etree.ElementTree as ET
import yaml
import os

def export_user_data(db_path='journals.db'):
    # Создаем папку out если ее нет
    if not os.path.exists('out'):
        os.makedirs('out')

    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
    cursor = conn.cursor()

    # Выполняем SQL-запрос


    cursor.execute("""
    SELECT
        u.Name,
        u.Password,
        ur.Name as role_name,
        ur.Comment as role_comment
    FROM User u
    LEFT JOIN User_role ur ON u.User_role_ID = ur.User_role_ID
    """)
    rows = cursor.fetchall()

    # Преобразуем в список словарей
    users = []
    for row in rows:
        user = dict(row)

        # Создаем вложенную структуру для роли пользователя
        role_data = {}
        if user.get('role_name'):
            role_data = {
                'role_name': user.get('role_name'),
                'role_comment': user.get('role_comment')
            }

            # Удаляем отдельные поля роли из основной структуры
            for field in ['role_name', 'role_comment']:
                if field in user:
                    del user[field]

            # Добавляем вложенную роль
            user['user_role'] = role_data

        users.append(user)

    # Экспорт в JSON
    with open('out/data.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    # Экспорт в CSV
    with open('out/data.csv', 'w', newline='', encoding='utf-8') as f:
        if users:
            # Собираем все возможные поля для CSV
            fieldnames = set()
            for user in users:
                fieldnames.update(user.keys())

            writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
            writer.writeheader()

            for user in users:
                # Для CSV преобразуем вложенные структуры в строки
                row_data = user.copy()
                if 'user_role' in row_data and isinstance(row_data['user_role'], dict):
                    row_data['user_role'] = json.dumps(row_data['user_role'], ensure_ascii=False)
                writer.writerow(row_data)

    # Экспорт в XML
    root = ET.Element('users')

    for user in users:
        user_elem = ET.SubElement(root, 'user')

        for key, value in user.items():
            if key == 'user_role' and isinstance(value, dict):
                # Вложенный элемент для роли пользователя
                role_elem = ET.SubElement(user_elem, 'user_role')
                for role_key, role_value in value.items():
                    role_field = ET.SubElement(role_elem, role_key)
                    role_field.text = str(role_value) if role_value is not None else ''
            else:
                field_elem = ET.SubElement(user_elem, key)
                field_elem.text = str(value) if value is not None else ''

    tree = ET.ElementTree(root)
    tree.write('out/data.xml', encoding='utf-8', xml_declaration=True)

    # Экспорт в YAML
    with open('out/data.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(users, f, default_flow_style=False, allow_unicode=True, indent=2)

    # Закрываем соединение
    conn.close()

    print("Файлы успешно созданы в папке out:")
    print("- data.json")
    print("- data.csv")
    print("- data.xml")
    print("- data.yaml")

# Запуск функции
if __name__ == "__main__":
    export_user_data()
"""