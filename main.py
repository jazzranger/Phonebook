import re
from datetime import date
from phonebook import PhoneBook


def check_name(value):
    value = re.sub(r'[^a-zA-Zа-яА-Я ]', '', value).split()
    value = ' '.join(value)
    return value


def check_number(number):
    number = re.search(r'[7|8]?[(|-]?(\d{3})[)|-]?(\d{3})-?(\d{2})-?(\d{2})', number)
    if number:
        return '8({}){}-{}-{}'.format(number.group(1), number.group(2), number.group(3), number.group(4))


def check_birthday(value):
    birthday = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', value)
    if birthday:
        day, month, year = birthday.group(1, 2, 3)
        try:
            birthday = date(int(year), int(month), int(day))
        except ValueError:
            birthday = None
    return birthday


def print_conacts(my_list, sort=False):
    for num, item in enumerate(my_list):
        birth_date = item.birthday.strftime('%d-%m-%Y') if item.birthday else ""
        tdelta = 'Дней до дня рождения: {}'.format(item.tdelta.days) if item.tdelta and sort else ""
        print('{}. {} {} {} {}'.format(num + 1, item.number, item.name, birth_date, tdelta))


menu = ('''Меню:
1. Добавление контакта 
2. Удаление контакта
3. Поиск контакта
4. Вывод списка контактов
5. Вывод отсортированного списка контактов
0. Выход из программы''')


phone_book = PhoneBook([])
phone_book.create_phonebook('phonebook_base')

while (True):
    print(menu)
    choice = input('\nВведите номер команды: ')
    if choice.isdigit():
        if choice == '1':
            value = input('Введите имя контакта и телефон: ')
            name = check_name(value)
            number = check_number(value)
            birthday = check_birthday(value)
            if not birthday:
                print('Неверно введена дата')
            if number:
                phone_book.ph_ins(name, number, birthday)
                print('Контакт добавлен')
            else:
                print('Ввод некорректен')

        if choice == '2':
            value = input('Введите имя контакта или телефон: ')
            name = check_name(value)
            number = check_number(value)
            if name or number:
                phone_book.ph_del(name, number)
                print('Контакт удалён')
            else:
                print('Ввод некорректен')

        if choice == '3':
            value = input('Введите имя контакта или телефон: ')
            print('\nНайденные контакты:')
            name = check_name(value)
            number = check_number(value)
            f_list = phone_book.ph_find(name, number)
            print_conacts(f_list)

        if choice == '4':
            print('\nСписок контактов:')
            phone_book.file_reader()
            print_conacts(phone_book.contacts)
            print('Контактов в записной книжке: {}'.format(len(phone_book.contacts)))

        if choice == '5':
            print('\nОтсортированный список контактов:')
            temp_list = phone_book.ph_sort()
            print_conacts(temp_list, sort=True)
            print('Контактов в записной книжке: {}'.format(len(phone_book.contacts)))

        if choice == '0':
            break

    else:
        print('Введено недопустимое значение')

    input('\nНажмите Enter, чтобы продолжить')
    print('\n' * 20)
