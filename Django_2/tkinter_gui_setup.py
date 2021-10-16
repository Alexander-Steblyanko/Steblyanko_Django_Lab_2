import tkinter as tk
import db_connection as db_c

# Створення основного вікна програми
window_base = tk.Tk()
window_base.geometry("400x350")
window_base.title("Стеблянко О. - ІС-93 - Лаб №2 - Вар №25")
# Створення обгортки, що додає відступів від країв вікна
frame = tk.Frame(master=window_base, borderwidth=5)
# Створення елементів вікна
intro_label = tk.Label(text="CRUD Адмінка для SQLite", master=frame)
# Створення кнопок, що викликатимуть вікна специфічних функцій
button_create = tk.Button(text="CREATE", width=10, height=1, master=frame)
button_read = tk.Button(text="READ", width=10, height=1, master=frame)
button_update = tk.Button(text="UPDATE", width=10, height=1, master=frame)
button_delete = tk.Button(text="DELETE", width=10, height=1, master=frame)
button_export = tk.Button(text="EXPORT", width=10, height=1, master=frame)
# Створення поля текстової демонстрації результатів
read_label = tk.Label(text="Результати зчитування", master=frame)
text_read = tk.Text(master=frame, height=12)
text_read.insert('1.0', 'Нічого нема \nпоки що')
# Поле не піддається редагуванню користувачем
text_read.config(state='disabled')

# Вставка обьєктів
intro_label.pack()
button_create.pack()
button_read.pack()
button_update.pack()
button_delete.pack()
button_export.pack()
read_label.pack()
text_read.pack()

frame.pack()


# Команда запуску основного вікна
def launch():
    window_base.mainloop()


# Функція для показу зчитаного стану БД в полі демонстрації
def show_reading(reading):
    text_read.config(state='normal')
    text_read.delete('0.0', tk.END)
    for i in range(len(reading)):
        text_read.insert(str(i+1) + '.0', str(reading[i]) + '\n')
    text_read.config(state='disabled')


# Функція для відкриття нового вікна введення
def open_create_window():
    # Створення вікна
    window_create = tk.Toplevel(window_base)
    window_create.geometry("225x250")
    # Створення обгортки
    frame_create = tk.Frame(master=window_create, borderwidth=5)
    intro_label_create = tk.Label(text="Вікно створення - введіть значення", master=frame_create)

    # Створення полів введення - числові значення використовують spinbox, текстові - entry
    id_label = tk.Label(text="ID", master=frame_create)
    id_entry = tk.Entry(master=frame_create)

    telnum_label = tk.Label(text="Номер телефону", master=frame_create)
    telnum_entry = tk.Entry(master=frame_create)

    tariff_label = tk.Label(text="Тариф абонента", master=frame_create)
    tariff_entry = tk.Entry(master=frame_create)

    pay_label = tk.Label(text="Оплаченість (0 або 1)", master=frame_create)
    pay_entry = tk.Entry(master=frame_create)

    # Створення кнопки, що викликає функцію створення нового введення в БД
    # Команда повинна виражатися черел лямбда-функцію
    # or використовується для виклику двох функцій з одної лямбда-функції
    button_create_execute = tk.Button(text="CREATE", width=10, height=1, master=frame_create,
                                      command=lambda: db_c.create(id_val=id_entry.get(), tel_num=telnum_entry.get(),
                                                                  tar_type=tariff_entry.get(), paid_for=pay_entry.get())
                                                      or show_reading(db_c.read()))

    # Вставка елементів у вікно
    intro_label_create.pack()
    id_label.pack()
    id_entry.pack()
    telnum_label.pack()
    telnum_entry.pack()
    tariff_label.pack()
    tariff_entry.pack()
    pay_label.pack()
    pay_entry.pack()
    button_create_execute.pack()

    frame_create.pack()

    # Відкриття вікна
    window_create.mainloop()


# Функція для відкриття нового вікна введення
def open_read_window():
    # Створення вікна
    window_read = tk.Toplevel(window_base)
    window_read.geometry("225x250")
    # Створення обгортки
    frame_read = tk.Frame(master=window_read, borderwidth=5)
    intro_label_read = tk.Label(text="Вікно зчитування - введіть умови\nПусте значення - пропуск", master=frame_read)

    # Створення полів введення
    telnum_label = tk.Label(text="Номер телефону\n(Може бути неповний)", master=frame_read)
    telnum_entry = tk.Entry(master=frame_read)

    tariff_label = tk.Label(text="Тариф абонента", master=frame_read)
    tariff_entry = tk.Entry(master=frame_read)

    pay_label = tk.Label(text="Оплаченість (0 або 1)", master=frame_read)
    pay_entry = tk.Entry(master=frame_read)

    # Створення кнопки, що викликає функцію зчитування даних з БД
    # Команда повинна виражатися черел лямбда-функцію
    button_read_execute = tk.Button(text="READ", width=10, height=1, master=frame_read,
                                    command=lambda: show_reading(db_c.read(tel_num=telnum_entry.get(),
                                                                           tar_type=tariff_entry.get(),
                                                                           paid_for=pay_entry.get())))

    # Вставка елементів у вікно
    intro_label_read.pack()
    telnum_label.pack()
    telnum_entry.pack()
    tariff_label.pack()
    tariff_entry.pack()
    pay_label.pack()
    pay_entry.pack()
    button_read_execute.pack()

    frame_read.pack()

    # Відкриття вікна
    window_read.mainloop()


# Функція для відкриття нового вікна оновлення
def open_update_window():
    # Створення вікна
    window_update = tk.Toplevel(window_base)
    window_update.geometry("225x250")
    # Створення обгортки
    frame_update = tk.Frame(master=window_update, borderwidth=5)
    intro_label_update = tk.Label(text="Вікно оновлення\nВведіть номер телефону та нові \nзначення змінної/змінних",
                                  master=frame_update)

    # Створення полів введення
    telnum_label = tk.Label(text="Номер телефону, що оновлюється", master=frame_update)
    telnum_entry = tk.Entry(master=frame_update)

    tariff_label = tk.Label(text="Тариф абонента", master=frame_update)
    tariff_entry = tk.Entry(master=frame_update)

    pay_label = tk.Label(text="Оплаченість (0 або 1)", master=frame_update)
    pay_entry = tk.Entry(master=frame_update)

    # Створення кнопки, що викликає функцію оновлення введення в БД
    # Команда повинна виражатися черел лямбда-функцію
    # or використовується для виклику двох функцій з одної лямбда-функції
    button_update_execute = tk.Button(text="UPDATE", width=10, height=1, master=frame_update,
                                      command=lambda: db_c.update(tel_num=telnum_entry.get(),
                                                                  tar_type=tariff_entry.get(), paid_for=pay_entry.get())
                                                      or show_reading(db_c.read()))

    # Вставка елементів у вікно
    intro_label_update.pack()
    telnum_label.pack()
    telnum_entry.pack()
    tariff_label.pack()
    tariff_entry.pack()
    pay_label.pack()
    pay_entry.pack()
    button_update_execute.pack()

    frame_update.pack()

    # Відкриття вікна
    window_update.mainloop()


# Функція для відкриття нового вікна видалення
def open_delete_window():
    # Створення вікна
    window_delete = tk.Toplevel(window_base)
    window_delete.geometry("225x125")
    # Створення обгортки
    frame_delete = tk.Frame(master=window_delete, borderwidth=5)
    intro_label_update = tk.Label(text="Вікно видалення",
                                  master=frame_delete)

    # Створення поля введення
    telnum_label = tk.Label(text="Номер телефону, що видаляється", master=frame_delete)
    telnum_entry = tk.Entry(master=frame_delete)

    # Створення кнопки, що викликає функцію видалення введення в БД
    # Команда повинна виражатися черел лямбда-функцію
    # or використовується для виклику двох функцій з одної лямбда-функції
    button_delete_execute = tk.Button(text="DELETE", width=10, height=1, master=frame_delete,
                                      command=lambda: db_c.delete(tel_num=[telnum_entry.get()])
                                                      or show_reading(db_c.read()))

    # Вставка елементів у вікно
    intro_label_update.pack()
    telnum_label.pack()
    telnum_entry.pack()
    button_delete_execute.pack()

    frame_delete.pack()

    # Відкриття вікна
    window_delete.mainloop()


# Функція для відкриття нового вікна видалення
def open_export_window():
    db2, db3 = db_c.export()

    # Створення вікна
    window_export = tk.Toplevel(window_base)
    window_export.geometry("400x400")
    # Створення обгортки
    frame_export = tk.Frame(master=window_export, borderwidth=5)

    # Створення полів для текстового виведення значень в інших БД після експорту
    intro_label_db2 = tk.Label(text="БД2 - postgreSQL", master=frame_export)
    text_db2 = tk.Text(master=frame_export, height=10)
    for i in range(len(db2)):
        text_db2.insert(str(i+1) + '.0', str(db2[i]) + '\n')
    text_db2.config(state='disabled')

    intro_label_db3 = tk.Label(text="БД3 - MySQL\nЗначення взяті з додатковою умовою, \nзмінені після імпорту",
                               master=frame_export)
    text_db3 = tk.Text(master=frame_export, height=10)
    for i in range(len(db3)):
        text_db3.insert(str(i+1) + '.0', str(db3[i]) + '\n')
    text_db3.config(state='disabled')

    # Вставка елементів у вікно
    intro_label_db2.pack()
    text_db2.pack()
    intro_label_db3.pack()
    text_db3.pack()

    frame_export.pack()

    # Відкриття вікна
    window_export.mainloop()


# Підключення кнопок основного меню до функцій створення вікон
button_create.bind("<Button>", lambda a: open_create_window())
button_read.bind("<Button>", lambda a: open_read_window())
button_update.bind("<Button>", lambda a: open_update_window())
button_delete.bind("<Button>", lambda a: open_delete_window())
button_export.bind("<Button>", lambda a: open_export_window())
