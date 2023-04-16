import pygame
import text
from channel import Channel
from ui.button_slider import *
import account


class ScrollingChannelList:

    def __init__(self, channel_list: list[Channel], x, y, height, scroll_pos=0.0, scroll_bar_focus=False):
        self.x = x
        self.y = y
        self.width = 248
        self.height = height
        self.scroll_bar = ButtonSliderVertical(self.x + self.width - 4, self.y, self.height, 4)
        self.scroll_bar.set_scroll_pos(scroll_pos)
        self.scroll_bar.mouse_focus = scroll_bar_focus
        self.__channel_list = channel_list
        self.__cached_board_surface = self.create_cached_board_surface()
        self.__selected_channel_id = -1

    def get_selected_channel_id(self):
        channel_id = self.__selected_channel_id
        self.__selected_channel_id = -1
        return channel_id

    def create_cached_board_surface(self):
        total_height = 0
        for channel in self.__channel_list:
            total_height = total_height + channel.get_label_height()

        # create a Surface based of the length of the channel_list
        board = pygame.Surface((self.width - 8, total_height), pygame.SRCALPHA)

        y_offset = 0
        for i in range(len(self.__channel_list)):
            channel_surf = self.__channel_list[i].get_rendered_label()
            board.blit(channel_surf, (0, y_offset))
            y_offset += channel_surf.get_height()
        return board

    def set_channel_list(self, channel_list):
        self.__channel_list = channel_list
        self.__cached_board_surface = self.create_cached_board_surface()

    def get_channel_list(self):
        return self.__channel_list

    def render(self, screen: pygame.Surface):
        scroll_offset = 0
        if self.__cached_board_surface.get_height() > self.height:
            scroll_offset = (self.__cached_board_surface.get_height() - self.height) * self.scroll_bar.get_scroll_pos()
        screen.blit(self.__cached_board_surface, (self.x, self.y), (0, scroll_offset, self.width, self.height))
        self.scroll_bar.render(screen)

    def mouse_input(self, event: pygame.event.Event):
        self.scroll_bar.mouse_input(event)
        if not self.scroll_bar.mouse_focus:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                scroll_offset = 0
                if self.__cached_board_surface.get_height() > self.height:
                    scroll_offset = (self.__cached_board_surface.get_height() - self.height) * self.scroll_bar.get_scroll_pos()
                relative_mouse_pos = (pygame.mouse.get_pos()[0]-self.x+scroll_offset, pygame.mouse.get_pos()[1]-self.y)
                i = 0
                while i < len(self.__channel_list):
                    if (0 <= relative_mouse_pos[0] <= self.width) and (i*self.__channel_list[i].get_label_height() <= relative_mouse_pos[1] <= i*self.__channel_list[i].get_label_height() + self.__channel_list[i].get_label_height()):
                        self.__selected_channel_id = self.__channel_list[i].get_id()
                        break
                    i += 1

