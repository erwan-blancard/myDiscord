import pygame

from ui.button_base import BaseButton


class TrueFalseButton(BaseButton):

    def __init__(self, x, y, size, false_icon: pygame.Surface, true_icon: pygame.Surface, activated=False, false_command=None, true_command=None):
        super().__init__(x, y, size, size)
        self.activated = activated
        self.true_command = true_command
        self.false_command = false_command
        false_icon = pygame.transform.scale(false_icon, (self.width, self.height))
        true_icon = pygame.transform.scale(true_icon, (self.width, self.height))
        self.icons = [false_icon, true_icon]

    def render(self, screen: pygame.Surface):
        img_index = 0
        if self.activated:
            img_index = 1
        screen.blit(self.icons[img_index], (self.x, self.y))
        super().render(screen)

    def execute(self):
        if self.activated:
            self.activated = False
            self.exec_false_command()
        else:
            self.activated = True
            self.exec_true_command()

    def exec_false_command(self):
        if self.false_command is not None:
            self.false_command()

    def exec_true_command(self):
        if self.true_command is not None:
            self.true_command()