import pygame
import text
from ui.button_base import *
from ui.button_icon import *
from ui.button_label import *


def render_overlay(screen: pygame.Surface):
    rect_over = pygame.Surface((pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]))
    rect_over.set_alpha(180)
    rect_over.fill((40, 40, 40))
    screen.blit(rect_over, (0, 0))


OVL_SIZE = 480


# base class for overlays with basic button support
class Overlay:

    def __init__(self):
        self.can_close = False
        self.buttons: list[BaseButton] = []

    def _render_buttons(self, surface: pygame.Surface):
        for button in self.buttons:
            button.render(surface)

    def update(self):
        pass

    def close(self):
        self.can_close = True

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        self._render_buttons(frame)
        return frame

    def input(self, event: pygame.event.Event):
        for button in self.buttons:
            button.mouse_input(event, relative_to=(int(pygame.display.get_window_size()[0]/2 - OVL_SIZE/2), int(pygame.display.get_window_size()[1]/2 - OVL_SIZE/2)))


# used to add a new overlay (in main.py)
next_overlay: Overlay = None
