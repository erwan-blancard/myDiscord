import pygame
import text

BUTTON = pygame.transform.scale(pygame.image.load("res/button.png"), (400, 40))


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
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), width=2)

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

        if self.__mouse_inside and self.__mouse_clicked:
            self.execute()

    def execute(self):
        if self.__command is not None:
            self.__command()


def create_button_surface(width: int):
    offset = 4
    if width < offset*2:
        width = offset*2
    if width > BUTTON.get_width():
        width = BUTTON.get_width()
    button_surf = pygame.Surface((width, BUTTON.get_height()))

    button_surf.blit(BUTTON, (0, 0), (0, 0, offset, BUTTON.get_height()))
    button_surf.blit(BUTTON, (button_surf.get_width()-offset, 0), (BUTTON.get_width()-offset, 0, offset, BUTTON.get_height()))

    button_surf.blit(BUTTON, (offset, 0), (offset, 0, width-offset*2, BUTTON.get_height()))

    return button_surf
