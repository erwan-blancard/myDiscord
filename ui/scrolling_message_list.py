import pygame
import text
from message import Message
from ui.button_slider import *


class ScrollingMessageList:

    def __init__(self, message_list: list[Message], x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_bar = ButtonSliderVertical(self.x + self.width - 4, self.y, self.height, 4)
        self.__message_list = message_list
        self.__cached_board_surface = self.create_cached_board_surface()

    def create_cached_board_surface(self):
        space_between_messages = 16
        total_height = 32
        for message in self.__message_list:
            total_height = total_height + message.get_rendered_surface_height() + 32 + space_between_messages

        # create a Surface based of the length of the message_list
        board = pygame.Surface((self.width - 8, total_height), pygame.SRCALPHA)

        y_offset = 0
        for i in range(len(self.__message_list)):
            message_surf = self.__message_list[i].get_rendered_surface()
            surf = pygame.Surface((self.width, message_surf.get_height() + 32), pygame.SRCALPHA)

            pos_x = 0
            if self.__message_list[i].is_owner():
                pos_x = self.width - message_surf.get_width()

            surf.blit(message_surf, (pos_x, 32))
            sender_name = str(self.__message_list[i].get_sender_id())
            text.draw_text(sender_name, pos_x + 16 + (int(self.__message_list[i].is_owner()) * (message_surf.get_width() - text.get_font(20).size(sender_name)[0] - 32)), y_offset + 10, board, text.get_font(20))

            board.blit(surf, (0, y_offset))
            y_offset += message_surf.get_height() + 32 + space_between_messages
        return board

    def set_message_list(self, message_list):
        self.__message_list = message_list
        self.__cached_board_surface = self.create_cached_board_surface()

    def render(self, screen: pygame.Surface):
        scroll_offset = 0
        if self.__cached_board_surface.get_height() > self.height:
            scroll_offset = (self.__cached_board_surface.get_height() - self.height) * self.scroll_bar.get_scroll_pos()
        screen.blit(self.__cached_board_surface, (self.x, self.y), (0, scroll_offset, self.width, self.height))
        self.scroll_bar.render(screen)

    def mouse_input(self, event: pygame.event.Event):
        self.scroll_bar.mouse_input(event)
