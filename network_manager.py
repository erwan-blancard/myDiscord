import random
import hashlib
import mysql.connector
import json


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

        self.__connected = False

    def is_connected(self):
        return self.__connected

    def create_account(self, name, lastname, email, password, picture_index=random.randint(0, 7)):
        hashed_password = hashlib.sha256(password.encode())
        cmnd = "INSERT INTO account (name, lastname, email, password, picture_index) VALUES ('"+name+"', '"+lastname+"', '"+email+"', '"+hashed_password.hexdigest()+"', "+str(picture_index)+");"
        self.__db_cursor.execute(cmnd)
        self.__db.commit()

    def connect_as(self, account_email, password):
        # hashed_password = hashlib.sha256(password.encode())
        # hashed_password.hexdigest()
        pass

    def get_channels(self):
        pass

    def create_channel(self, name, is_private, is_voice_chat, password):
        # hashed_password = hashlib.sha256(password.encode())
        # hashed_password.hexdigest()
        pass

    def is_channel_password_valid(self, channel_id, password):
        # hashed_password = hashlib.sha256(password.encode())
        # hashed_password.hexdigest()
        pass


__net_manager = NetworkManager()


def get_instance():
    return __net_manager
