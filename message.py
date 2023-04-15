"""
+------------+-------------+------+-----+---------+----------------+
| Field      | Type        | Null | Key | Default | Extra          |
+------------+-------------+------+-----+---------+----------------+
| id         | int         | NO   | PRI | NULL    | auto_increment |
| content    | text        | NO   |     | NULL    |                |
| channel_id | int         | NO   |     | NULL    |                |
| sender_id  | int         | NO   |     | NULL    |                |
| time       | varchar(5)  | NO   |     | NULL    |                |
+------------+-------------+------+-----+---------+----------------+
"""
import pygame

import account
from account import PPS
import text
from ui.text_box import TextBox

BOX = pygame.transform.scale(pygame.image.load("res/box.png"), (32, 32))


class Message:

    def __init__(self, id: int, content: str, channel_id: int, sender_id: int, time: str):
        self.__id = id
        self.__content = content
        self.__channel_id = channel_id
        self.__sender_id = sender_id
        self.__time = time

    def get_id(self):
        return self.__id

    def get_sender_id(self):
        return self.__sender_id

    def is_owner(self):
        local_account = account.get_local_account()
        return local_account is not None and local_account.get_id() == self.__sender_id

    def get_rendered_surface_height(self):
        text_box = TextBox(self.__content, 0, 0, 256, text.get_font(20))
        if 16+text_box.get_height() < 64:
            return 64
        return 16+text_box.get_height()

    def get_rendered_surface(self):
        local_account = account.get_local_account()
        pp_index = 0
        if local_account is not None:
            pp_index = local_account.get_picture_index()

        offset = 8
        txtbox_x = 0
        pp_x = 256+(offset*2)
        if not self.is_owner():
            txtbox_x = 64
            pp_x = 0
        text_box = TextBox(self.__content, offset+txtbox_x, offset, 256, text.get_font(20))
        surf_height = (offset*2)+text_box.get_height()
        if surf_height < 64:
            surf_height = 64
        surf = pygame.Surface(((offset*2)+256+64, surf_height), pygame.SRCALPHA)
        if not 0 <= pp_index < len(PPS):
            pp_index = 0

        # middle
        mid = pygame.Surface((offset*2, offset*2), pygame.SRCALPHA)
        mid.blit(BOX, (0, 0), (offset, offset, offset*2, offset*2))
        surf.blit(pygame.transform.scale(mid, (256, text_box.get_height())), (offset+txtbox_x, offset))

        # corners
        surf.blit(BOX, (txtbox_x, 0), (0, 0, offset, offset))
        surf.blit(BOX, (txtbox_x+surf.get_width()-offset-64, 0), (BOX.get_width()-offset, 0, offset, offset))
        surf.blit(BOX, (txtbox_x, offset+text_box.get_height()), (0, BOX.get_height()-offset, offset, offset))
        surf.blit(BOX, (txtbox_x+surf.get_width() - offset-64, offset+text_box.get_height()), (BOX.get_width() - offset, BOX.get_height()-offset, offset, offset))

        # lines
        top_line = pygame.Surface((offset*2, offset), pygame.SRCALPHA)
        top_line.blit(BOX, (0, 0), (offset, 0, offset*2, offset))
        surf.blit(pygame.transform.scale(top_line, (256, offset)), (offset+txtbox_x, 0))

        left_line = pygame.Surface((offset, offset*2), pygame.SRCALPHA)
        left_line.blit(BOX, (0, 0), (0, offset, offset, offset*2))
        surf.blit(pygame.transform.scale(left_line, (offset, text_box.get_height())), (txtbox_x, offset))

        right_line = pygame.Surface((offset, offset * 2), pygame.SRCALPHA)
        right_line.blit(BOX, (0, 0), (BOX.get_width()-offset, offset, offset, offset * 2))
        surf.blit(pygame.transform.scale(right_line, (offset, text_box.get_height())), (offset+txtbox_x+256, offset))

        bot_line = pygame.Surface((offset * 2, offset), pygame.SRCALPHA)
        bot_line.blit(BOX, (0, 0), (offset, BOX.get_height()-offset, offset * 2, offset))
        surf.blit(pygame.transform.scale(bot_line, (256, offset)), (offset+txtbox_x, offset+text_box.get_height()))

        text_box.render(surf)
        surf.blit(PPS[pp_index], (pp_x+(64/2-PPS[pp_index].get_width()/2), offset))
        text.draw_aligned_text(self.__time, pp_x+(64/2), offset*2+PPS[pp_index].get_height(), surf, text.font())
        return surf
