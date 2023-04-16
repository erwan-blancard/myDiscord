import pygame

from ui.button_base import *


class ButtonTextInput(BaseButton):

    def __init__(self, x, y, width, height, default_text="", font=text.font(), color=text.DEFAULT_COLOR, hide_text: bool = False, lock=False):
        super().__init__(x, y, width, height, None)
        self.__text = default_text
        self.font = font
        self.color = color
        self.__focused = False
        self.__hide_text = hide_text
        self.__mouse_inside = False
        self.__mouse_clicked = False
        self.__locked = lock

    def clear_text(self):
        self.__text = ""

    def set_lock(self, val: bool):
        self.__locked = val

    def get_text(self):
        return self.__text

    def set_hide_text(self, condition: bool):
        self.__hide_text = condition

    def mouse_input(self, event: pygame.event.Event, relative_to: tuple[int, int] = (0, 0)):
        mouse_pos = (pygame.mouse.get_pos()[0]-relative_to[0], pygame.mouse.get_pos()[1]-relative_to[1])
        if (self.x <= mouse_pos[0] <= self.x + self.width) and (self.y <= mouse_pos[1] <= self.y + self.height):
            self.__mouse_inside = True
        else:
            self.__mouse_inside = False

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            self.__mouse_clicked = True
        else:
            self.__mouse_clicked = False

        if not self.__locked and self.__mouse_inside and self.__mouse_clicked:
            self.__focused = True

        if self.__mouse_clicked and not self.__mouse_inside:
            self.__focused = False

    def key_input(self, event: pygame.event.Event):
        if not self.__locked and event.type == pygame.KEYDOWN and self.__focused:
            if event.key == pygame.K_RETURN:
                self.__focused = False
            elif event.key == pygame.K_BACKSPACE:
                self.__text = self.__text[:-1]
            elif event.key != pygame.K_TAB and event.key != pygame.K_KP_ENTER and event.key != pygame.K_ESCAPE:
                self.__text += event.unicode

    def render(self, screen: pygame.Surface):
        offset = 8
        text_surf = pygame.Surface((self.width - offset*2, self.height), pygame.SRCALPHA)
        if self.__hide_text:
            display_text = "*"*len(self.__text)
        else:
            display_text = self.__text

        if self.__focused:
            display_text += "_"
        if self.font.size(display_text)[0] > text_surf.get_width():
            text.draw_text(display_text, text_surf.get_width()-self.font.size(display_text)[0], (self.height - self.font.size(display_text)[1]) / 2, text_surf, self.font, color=self.color)
        else:
            text.draw_text(display_text, 0, (self.height - self.font.size(display_text)[1]) / 2, text_surf, self.font, color=self.color)
        pygame.draw.rect(screen, (30, 30, 30), (self.x, self.y, self.width, self.height))
        if self.__focused or self.__mouse_inside:
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), width=2)
        else:
            pygame.draw.rect(screen, (90, 90, 90), (self.x, self.y, self.width, self.height), width=2)
        screen.blit(text_surf, (self.x + offset, self.y))
