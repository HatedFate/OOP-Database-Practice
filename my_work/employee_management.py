import sqlite3
import pytz
import datetime


db = sqlite3.connect("C:\\Users\\13473\\Documents\\Python Scripts\\employee.sqlite3")
db.execute("CREATE TABLE IF NOT EXISTS employee (_id INTEGER PRIMARY KEY, name TEXT NOT NULL,"
           "phone INTEGER NOT NULL, email TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS checkins (ID INTEGER, name TEXT NOT NULL, time TIMESTAMP NOT NULL)")


class Employee:

    salaries_emp = 30000

    @staticmethod
    def _get_time():
        return pytz.utc.localize(datetime.datetime.utcnow()).astimezone

    @classmethod
    def _get_salary(cls, self):
        if self._raises:
            self._raises = False
            return cls.salaries_emp * 1.04
        return cls.salaries_emp

    def __init__(self, name: str, phone: int, email: str = ""):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employee WHERE name = ? AND phone = ?", (name, phone))
        row = cursor.fetchone()
        if row:
            if len(name.split()) == 3:
                self.f_name, self.m_name, self.l_name = name.split()
            else:
                self.f_name, self.l_name = name.split()
            self.phone = phone
            self.email = email
        else:
            cursor.execute("INSERT INTO employee (name, phone, email) VALUES (?, ?, ?)",
                           (name, phone, email))
            cursor.connection.commit()
        self._raises = False
        cursor.close()

    def check_in(self):
        cursor = db.cursor()
        cursor.execute("SELECT _id, name FROM employee WHERE (phone = ?) AND (email = ?)", (self.phone, self.email,))
        emp_id, name = cursor.fetchone()
        cursor.execute("INSERT INTO checkins VALUES (?, ?, ?)", (emp_id, name, Employee._get_time()))
        print("You have checked in at {}".format(Employee._get_time()))

    def __str__(self):
        cursor = db.cursor()
        cursor.execute("SELECT name, phone FROM employee WHERE phone = ? AND email = ?", (self.phone, self.email))
        name, phone = cursor.fetchone()
        return "Name: {} | Phone: {}".format(name, phone)


class Manager(Employee):

    salaries_emp = 60000

    @classmethod
    def _get_salary(cls, self):
        if self._raises:
            self._raises = False
            return cls.salaries_emp * 1.1
        return cls.salaries_emp


if __name__ == "__main__":
    john = Employee("john jones", 9999999)
    brian = Employee("brains smith", 999123)
    joe = Employee("joe john smith", 1999292)
    joe.check_in()
    print(joe)
    print(brian)
    print(john)

db.commit()
db.close()
