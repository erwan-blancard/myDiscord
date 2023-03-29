import pygame
import text


class BaseButton:

    def __init__(self, x, y, width, height, command=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__command = command
        self.__mouse_inside = False
        self.__mouse_clicked = False

    def render(self, screen: pygame.Surface):
        if self.__mouse_inside:
            self.__render_hover(screen)

    def __render_hover(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), width=1)

    def mouse_input(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if (self.x <= mouse_pos[0] <= self.x + self.width) and (self.y <= mouse_pos[1] <= self.y + self.height):
            self.__mouse_inside = True
        else:
            self.__mouse_inside = False

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            self.__mouse_inside = True
        else:
            self.__mouse_inside = False

        if self.__mouse_inside and self.__mouse_clicked:
            self.execute()

    def execute(self):
        if self.__command is not None:
            self.__command()


def create_button_surfaces(width: int):
    button_img = pygame.image.load("res/buttons.png")
    button_surf = pygame.Surface((width, button_img.get_height()/2))
