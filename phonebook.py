from contact import Contact
from datetime import date, datetime
import csv
import os
from phonebook_logger import log_decorator, logger

class PhoneBook:
    def __init__(self, contacts):
        self.contacts = contacts

    def create_phonebook(self, filename):
        if os.path.exists(filename):
            return
        else:
            with open(filename, 'w') as phonebook:
                writer = csv.writer(phonebook, lineterminator='\n')
                writer.writerow('')

    @log_decorator(logger)
    def contact_writer(self, contact, filename='phonebook_base.csv'):
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(contact)

    def file_reader(self, filename='phonebook_base.csv'):
        self.contacts = []
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                birthday = datetime.strptime(row[2], "%Y-%m-%d").date() if row[2] else ''
                self.contacts.append(Contact(row[0], row[1], birthday, row[3]))

    def file_writer(self, filename='phonebook_base.csv'):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            temp_list = []
            c = self.contacts
            for item in c:
                temp_list.append([item.name, item.number, item.birthday, item.tdelta])
            writer.writerows(temp_list)

    def ph_ins(self, name, number, birthday, tdelta=None):
        contact = [name, number, birthday, tdelta]
        self.contact_writer(contact)

    @log_decorator(logger)
    def ph_del(self, name, number):
        self.file_reader()
        for i in list(self.contacts):
            if i.name == name or i.number == number:
                self.contacts.remove(i)
        self.file_writer()

    def ph_find(self, name, number):
        self.file_reader()
        f_contacts = [i for i in list(self.contacts) if i.name == name or i.number == number]
        return f_contacts

    def ph_sort(self):
        self.file_reader()
        list_with_birth = []
        list_without_birth = []
        for i in list(self.contacts):
            if i.birthday:
                list_with_birth.append(i)
            else:
                list_without_birth.append(i)

        for i in range(len(list_with_birth)):
            date_now = date.today()
            birthday = list_with_birth[i].birthday.replace(year=date_now.year)
            if date_now > birthday:
                cur_timedelta = birthday.replace(year=date_now.year + 1) - date_now
            else:
                cur_timedelta = birthday - date_now
            list_with_birth[i].tdelta = cur_timedelta
        list_with_birth = sorted(list_with_birth, key=lambda k: k.tdelta)

        return list_with_birth + list_without_birth
