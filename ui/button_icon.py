import pygame

from ui.button_base import *


class ButtonIcon(BaseButton):

    def __init__(self, x, y, width, height, icon, command=None):
        super().__init__(x, y, width, height, command)
        icon = pygame.transform.scale(icon, (self.width, self.height))
        self.__icon = icon

    def set_icon(self, icon: pygame.Surface):
        if icon.get_width() == self.__icon.get_width() and icon.get_height() == self.__icon.get_height():
            self.__icon = icon

    def render(self, screen):
        screen.blit(self.__icon, (self.x, self.y))
        super().render(screen)
