"""
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int          | NO   | PRI | NULL    | auto_increment |
| name          | varchar(255) | NO   |     | NULL    |                |
| lastname      | varchar(255) | NO   |     | NULL    |                |
| email         | varchar(255) | NO   |     | NULL    |                |
| password      | varchar(255) | NO   |     | NULL    |                |
| picture_index | int          | YES  |     | 0       |                |
+---------------+--------------+------+-----+---------+----------------+
"""


class Account:

    def __init__(self, id, name, lastname, email, picture_index):
        self.__id = id
        self.__name = name
        self.__lastname = lastname
        self.__email = email
        self.__picture_index = picture_index

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_lastname(self):
        return self.__lastname

    def get_fullname(self):
        return self.get_name() + " " + self.get_lastname()

    def get_email(self):
        return self.__email

    def get_picture_index(self):
        return self.__picture_index


local_account: Account = None


def get_local_account():
    return local_account
