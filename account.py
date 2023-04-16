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
import json

import pygame

PPS = []
for i in range(8):
    PPS.append(pygame.image.load("res/styles/pp_"+str(i)+".png"))


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


_local_account: Account = None

_accounts: list[Account] = []


def set_local_account(account: Account):
    global _local_account
    _local_account = account
    try:
        file = open("last_profile.json", "w")
        json.dump({"email": account.get_email()}, file, indent=4)
        file.close()
    except IOError as e:
        print(e)


def get_local_account():
    return _local_account


def get_accounts():
    return _accounts


def get_picture_index(account_id):
    for account in _accounts:
        if account.get_id() == account_id:
            return account.get_picture_index()
    return 0


def set_accounts(accounts: list[Account]):
    global _accounts
    global _local_account
    _accounts = accounts
    if _local_account is not None:
        _local_account = get_account_by_id(_local_account.get_id())


def get_name_by_id(id: int):
    for account in _accounts:
        if account.get_id() == id:
            return account.get_fullname()
    return "User#"+str(id)


def get_account_by_id(id: int):
    for account in _accounts:
        if account.get_id() == id:
            return account
    return None
