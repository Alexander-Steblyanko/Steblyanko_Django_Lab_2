import datetime
# Бібліотека peewee
from peewee import *
from playhouse.mysql_ext import MySQLConnectorDatabase
# Бібліотека для PostgreSQL (БД 2)
import psycopg2
# Бібліотека для  MySQL (БД 3)
import mysql.connector

# Створення об'єкту ДБ (за відсутності файлу створюється новий)
db = SqliteDatabase('C:\Temp\lab2.db')


# Опис моделі таблиці
# Варіант 25: Довідкова інформаційна система обліку телефонних номерів абонентів АТС;
class subscriptions(Model):
    id = IntegerField(primary_key=True)
    telephone_number = TextField()
    tariff_type = TextField()
    paid_for = IntegerField()

    class Meta:
        database = db


# Команда для створення та початкового заповнення таблиці обліку абонентів
# Виконюється один раз до початку роботи з адмінкою
def create_sqlite_table():
    # Створення підключення до бази даних SQLite
    db.connect(reuse_if_open=True)
    # Створення таблиці
    db.create_tables([subscriptions])

    # Заповнення таблиці
    entry_list = [
        (0, '+380 44 102-36-72', 'Unlimited', 1),
        (1, '+380 45 948-92-27', 'Entertainment', 1),
        (2, '+380 44 752-55-22', 'Unlimited', 1),
        (3, '+380 47 222-22-11', 'Budget', 0),
        (4, '+380 48 736-75-39', 'Entertainment', 1),
        (5, '+380 40 948-64-76', 'Entertainment', 1),
        (6, '+380 42 948-65-54', 'Budget', 1),
        (7, '+380 44 675-32-69', 'Unlimited', 0),
    ]
    subscriptions.insert_many(entry_list, fields=[subscriptions.id, subscriptions.telephone_number,
                                                  subscriptions.tariff_type, subscriptions.paid_for]).execute()

    # Закриття підключення
    db.close()


# Функція для створення БД2 postgreSQL, так як peewee не підтримує створення нових БД
# Виконюється один раз до початку роботи з адмінкою
def create_postgres_database():
    # Створення підключення
    postgres_con = psycopg2.connect(user="postgres", password="DjangoLab", host="localhost")
    postgres_con.autocommit = True
    postgres_cur = postgres_con.cursor()
    # Створення БД
    postgres_cur.execute("CREATE DATABASE djangolab2;")
    # Закриття підключення
    postgres_con.close()


# Функція для створення БД3 MySQL, так як peewee не підтримує створення нових БД
# Виконюється один раз до початку роботи з адмінкою
def create_mysql_database():
    # Створення підключення
    mysql_con = mysql.connector.connect(user="Python_app", password="DjangoLab", host="localhost")
    mysql_cur = mysql_con.cursor()
    # Створення БД
    mysql_cur.execute("CREATE DATABASE djangolab2;")
    # Закінчення транзакції
    mysql_con.commit()
    # Закриття підключення
    mysql_con.close()


# Функція для створення нового введення в таблиці
def create(id_val, tel_num, tar_type, paid_for):
    # Створення підключення до бази даних SQLite
    db.connect(reuse_if_open=True)

    # Створення введення
    subscriptions.insert(id=id_val, telephone_number=tel_num, tariff_type=tar_type, paid_for=paid_for).execute()

    # Закриття підключення
    db.close()


# Функція для зчитування значень таблиці
# Можна надати неповний телефониий номер, що поверне всі номери з введеною частиною номера
def read(tel_num=None, tar_type=None, paid_for=None):
    # Створення підключення
    db.connect(reuse_if_open=True)
    # Створення базової команди зчитування
    entry_list = subscriptions.select().tuples()
    # Додання додаткових умов
    if tel_num:
        entry_list = entry_list.where(subscriptions.telephone_number.contains(tel_num))
    if tar_type:
        entry_list = entry_list.where(subscriptions.tariff_type == tar_type)
    if paid_for:
        entry_list = entry_list.where(subscriptions.paid_for == paid_for)
    # Закриття підключення
    db.close()

    print(type(entry_list))
    # Функція повертає вcі отримані значення
    return entry_list


# Функція змінює тариф та/або стан оплати для вказаного номеру телефону
def update(tel_num, tar_type=None, paid_for=None):
    # Створення підключення
    db.connect(reuse_if_open=True)
    # Якщо не обрано значення для зміни, повертає помилку
    if tar_type == '' and paid_for == '':
        raise ValueError("Не вказано змінну, що потребує змін")

    # Отримання введення, потребуючого змін
    entry = subscriptions.get(subscriptions.telephone_number == tel_num)
    # Оновлення даних
    if tar_type:
        entry.tariff_type = tar_type
    if paid_for:
        entry.paid_for = paid_for
    # Збереження змін
    entry.save()

    # Закриття підключення
    db.close()


# Функція для видалення введення в таблиці за певним телефонним номером
def delete(tel_num):
    # Створення підключення
    db.connect(reuse_if_open=True)
    # Виконання команди видалення
    subscriptions.get(subscriptions.telephone_number == tel_num).delete_instance()
    # Закриття підключення
    db.close()


# Функція експорту з БД1 до БД2, та з БД2 до БД3 з виконанням додаткової умови та SQL запиту
def export():
    # Створення об'єктів БД2 та БД3
    db2 = PostgresqlDatabase("djangolab2", host="localhost", user="postgres", password="DjangoLab")
    db3 = MySQLConnectorDatabase("djangolab2", host="localhost", user="Python_app", password="DjangoLab")

    cur_time = datetime.datetime.now()
    # Створення підключення до БД postgreSQL
    db2.connect(reuse_if_open=True)

    # Створення нової таблиці абонентів в postgreSQL
    class subscriptions_db2(Model):
        id = IntegerField(primary_key=True)
        telephone_number = TextField()
        tariff_type = TextField()
        paid_for = IntegerField()

        class Meta:
            database = db2
            table_name = 'subscriptions_' + cur_time.strftime("%d_%m_%Y_%H_%M_%S")

    subscriptions_db2.create_table()

    # Значення з БД1 записуються в БД2
    # Запис в таблицю потребує перетворення об'єкту запиту зчитування в список значень
    entry_list_db1 = []
    for e in read():
        entry_list_db1 += [e]
    # Значення з БД1 записуються в БД2
    subscriptions_db2.insert_many(entry_list_db1, fields=[subscriptions_db2.id, subscriptions_db2.telephone_number,
                                                          subscriptions_db2.tariff_type,
                                                          subscriptions_db2.paid_for]).execute()
    # Створення підключення до БД3 MySQL
    db3.connect(reuse_if_open=True)

    # Створення нової таблиці абонентів в MySQL
    class subscriptions_db3(Model):
        telephone_number = CharField(primary_key=True, max_length=17)
        tariff_type = TextField()
        paid_for = IntegerField()

        class Meta:
            database = db3
            table_name = 'subscriptions_' + cur_time.strftime("%d_%m_%Y_%H_%M_%S")

    subscriptions_db3.create_table()
    # Створення повного списку значень БД2 для текстового виведення
    entry_list_db2 = read()

    # Значення з БД2 (окрім ID) записуються в БД3
    entry_list_db2_for3 = []
    # Значення для БД3 обираються з додатковою умовою - в БД3 йдуть тільки абоненти з оплаченими тарифами
    # Запис в таблицю потребує перетворення об'єкту запиту зчитування в список значень
    for e in subscriptions_db2.select(subscriptions_db2.telephone_number, subscriptions_db2.tariff_type,
                                      subscriptions_db2.paid_for) \
            .where(subscriptions_db2.paid_for == 1).tuples():
        entry_list_db2_for3 += [e]
    # Значення з БД2 записуються в БД3
    subscriptions_db3.insert_many(entry_list_db2_for3, fields=[subscriptions_db3.telephone_number,
                                                               subscriptions_db3.tariff_type,
                                                               subscriptions_db3.paid_for]).execute()
    # Над значеннями БД3 виконується додаткова трасформація
    subscriptions_db3.update({subscriptions_db3.telephone_number:
                                  fn.CONCAT("+381", fn.SUBSTR(subscriptions_db3.telephone_number, 5, 13)),
                              subscriptions_db3.tariff_type: subscriptions_db3.tariff_type.concat(" 2021"),
                              subscriptions_db3.paid_for: 1 - subscriptions_db3.paid_for}).execute()
    # Створення повного списку значень БД3 для текстового виведення
    entry_list_db3 = subscriptions_db3.select().tuples()
    # Закриття підключень
    db2.close()
    db3.close()

    # Виведення результатів в консоль
    print("БД2 - postgreSQL:")
    for i in entry_list_db2:
        print(i)
    print("БД3 - MySQL:")
    for i in entry_list_db3:
        print(i)

    # Повертає значення з БД2 та БД3 для текстового показу
    return entry_list_db2, entry_list_db3
