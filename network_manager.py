import random
import hashlib
from datetime import datetime

import mysql.connector
import json

import account
from channel import Channel
from message import Message

TIME_FORMAT = "{:02d}:{:02d}"


class NetworkManager:

    def __init__(self):
        file = open("target_server.json", "r")
        target_server = json.load(file)
        file.close()
        self.__db = mysql.connector.connect(
            host=target_server["host"], user=target_server["user"],
            password=target_server["password"],
            database=target_server["database"]
        )
        self.__db_cursor = self.__db.cursor()

    def create_account(self, name, lastname, email, password, picture_index=random.randint(0, 7)):
        try:
            hashed_password = hashlib.sha256(password.encode())
            cmnd = "INSERT INTO account (name, lastname, email, password, picture_index) VALUES ('"+name+"', '"+lastname+"', '"+email+"', '"+hashed_password.hexdigest()+"', "+str(picture_index)+");"
            self.__db_cursor.execute(cmnd)
            self.__db.commit()
            return True
        except Exception as e:
            print("CREATE_ACCOUNT: Impossible d\'exécuter la requête:", e)
            return False

    def account_exists(self, email):
        try:
            cmnd = "SELECT email FROM account WHERE email='"+email+"'"
            self.__db_cursor.execute(cmnd)
            records = self.__db_cursor.fetchall()
            if len(records) > 0:
                return True
        except Exception as e:
            print("ACCOUNT_EXISTS: Impossible d\'exécuter la requête:", e)
            return True
        return False

    def connect_as(self, account_email, password):
        """
        0 = not connected or already connected
        1 = connect success
        -1 = account doesn't exist
        -2 = request fail
        """
        global _connected
        if not _connected:
            hashed_password = hashlib.sha256(password.encode())
            cmnd = "SELECT id, name, lastname, email, picture_index FROM account WHERE email='"+account_email+"' AND password='"+hashed_password.hexdigest()+"';"
            try:
                self.__db_cursor.execute(cmnd)
                records = self.__db_cursor.fetchall()
                if len(records) < 1:
                    return -1
                for acc in records:
                    account.set_local_account(account.Account(acc[0], acc[1], acc[2], acc[3], acc[4]))
                    _connected = True
                    return 1
            except Exception as e:
                print("CONNECT_AS: Impossible d\'exécuter la requête:", e)
                return -2
        return 0

    def get_all_accounts(self):
        """
        Returns a list of accounts to account._accounts
        """
        accounts: list[account.Account] = []
        cmnd = "SELECT id, name, lastname, email, picture_index FROM account;"
        try:
            self.__db_cursor.execute(cmnd)
            records = self.__db_cursor.fetchall()
            for row in records:
                accounts.append(account.Account(row[0], row[1], row[2], row[3], row[4]))
            account.set_accounts(accounts)
        except Exception as e:
            print("GET_ALL_ACCOUNTS: Impossible d\'exécuter la requête:", e)

    def get_channels(self):
        channels: list[Channel] = []
        cmnd = "SELECT id, name, private, voice_chat FROM channel;"
        try:
            self.__db_cursor.execute(cmnd)
            records = self.__db_cursor.fetchall()
            for row in records:
                channels.append(Channel(row[0], row[1], row[2], row[3]))
        except Exception as e:
            print("GET_CHANNELS: Impossible d\'exécuter la requête:", e)

        return channels

    def create_channel(self, name, is_private, is_voice_chat, password):
        hashed_password = hashlib.sha256(password.encode())
        cmnd = "INSERT INTO channel (name, private, voice_chat, password) VALUES ('" + name + "', '" + str(int(is_private)) + "', '" + str(int(is_voice_chat)) + "', '" + hashed_password.hexdigest() + "');"
        if len(password) < 1:
            cmnd = "INSERT INTO channel (name, private, voice_chat, password) VALUES ('"+name+"', '"+str(int(is_private))+"', '"+str(int(is_voice_chat))+"', '');"
        try:
            self.__db_cursor.execute(cmnd)
            self.__db.commit()
            return True
        except Exception as e:
            print("CREATE_CHANNEL: Impossible d\'exécuter la requête:", e)
            return False

    def is_channel_password_valid(self, channel_id, password):
        hashed_password = hashlib.sha256(password.encode())
        cmnd = "SELECT password FROM channel WHERE id = "+str(channel_id)+";"
        try:
            self.__db_cursor.execute(cmnd)
            records = self.__db_cursor.fetchall()
            for passwd in records:
                if passwd[0] == hashed_password.hexdigest():
                    return True
                break
        except Exception as e:
            print("IS_CHANNEL_PASSWORD_VALID: Impossible d\'exécuter la requête:", e)

        return False

    def get_channel_messages(self, channel_id):
        messages: list[Message] = []
        cmnd = "SELECT * FROM message WHERE channel_id = "+str(channel_id)+";"
        try:
            self.__db_cursor.execute(cmnd)
            records = self.__db_cursor.fetchall()
            for row in records:
                messages.append(Message(row[0], row[1], row[2], row[3], row[4]))
        except Exception as e:
            print("GET_CHANNEL_MESSAGES: Impossible d\'exécuter la requête:", e)

        return messages

    def send_message(self, channel_id, content):
        if account.get_local_account() is not None:
            cmnd = "INSERT INTO message (content, channel_id, sender_id, time) VALUES ('"+content+"', "+str(channel_id)+", "+str(account.get_local_account().get_id())+", '"+TIME_FORMAT.format(datetime.now().hour, datetime.now().minute)+"');"
            try:
                self.__db_cursor.execute(cmnd)
                self.__db.commit()
                return True
            except Exception as e:
                print("SEND_MESSAGE: Impossible d\'exécuter la requête:", e)

        return False

    def change_profile_picture(self, new_pp: int):
        if account.get_local_account() is not None and 0 <= new_pp < len(account.PPS):
            cmnd = "UPDATE account SET picture_index="+str(new_pp)+" WHERE id="+str(account.get_local_account().get_id())+";"
            try:
                self.__db_cursor.execute(cmnd)
                self.__db.commit()
                return True
            except Exception as e:
                print("CHANGE_PROFILE_PICTURE: Impossible d\'exécuter la requête:", e)
        return False


def disconnect():
    global _connected
    account._accounts = None
    account._local_account = None
    _connected = False


_net_manager = NetworkManager()

_connected = False


def is_connected():
    return _connected


def get_instance():
    return _net_manager
