"""
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int          | NO   | PRI | NULL    | auto_increment |
| name       | varchar(255) | NO   |     | NULL    |                |
| private    | tinyint(1)   | NO   |     | NULL    |                |
| voice_chat | tinyint(1)   | NO   |     | NULL    |                |
| password   | varchar(255) | YES  |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
"""
import pygame

import text
from message import Message

PRIVATE_ICON = pygame.image.load("res/private.png")
TEXT_CHAT_ICON = pygame.image.load("res/message.png")
VOICE_CHAT_ICON = pygame.image.load("res/voice_chat.png")


class Channel:

    def __init__(self, id: int, name: str, private: int, voice_chat: int):
        self.__id = id
        self.__name = name
        self.__private = private
        self.__voice_chat = voice_chat

        self.__messages = list[Message]

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def is_private(self):
        return self.__private

    def is_voice_chat(self):
        return self.__voice_chat

    def get_messages(self):
        return self.__messages

    def get_rendered_label(self):
        label_size = 192
        surf = pygame.Surface((label_size+32, 32), pygame.SRCALPHA)
        color = (120, 120, 120)
        pygame.draw.circle(surf, color, (16, 16), 16)
        pygame.draw.circle(surf, color, (label_size+16, 16), 16)
        pygame.draw.rect(surf, color, (16, 0, label_size, 32))
        if self.__voice_chat:
            surf.blit(VOICE_CHAT_ICON, (8, surf.get_height()/2-VOICE_CHAT_ICON.get_height()/2))
        else:
            surf.blit(TEXT_CHAT_ICON, (8, surf.get_height() / 2 - TEXT_CHAT_ICON.get_height() / 2))
        if self.__private:
            surf.blit(PRIVATE_ICON, (surf.get_width()-28, surf.get_height() / 2 - PRIVATE_ICON.get_height() / 2))

        label = ""
        font = text.get_font(18)
        if font.size(self.__name)[0] > label_size-45:
            for c in self.__name:
                if font.size(label+c+"...")[0] >= label_size-45:
                    label = label+c+"..."
                    break
                else:
                    label += c
        else:
            label = self.__name
        text.draw_text(label, 38, 4, surf, font)
        return surf
