import pygame


class ButtonSliderVertical:

    def __init__(self, x, y, length, stroke, color=(255, 255, 255), release_command=None):
        self.x = x
        self.y = y
        self.length = length
        self.stroke = stroke
        self.scroll_pos: float = 0.0
        self.mouse_inside = False
        self.mouse_clicked = False
        self.mouse_focus = False
        self.color = color
        self.release_command = release_command

    def render(self, screen: pygame.Surface):
        # bar
        screen.fill(self.color, (self.x, self.y, self.stroke, self.length))

        # slider
        pygame.draw.circle(screen, self.color, (self.x + self.stroke / 2, self.y + self.length * self.scroll_pos), self.stroke * 2)

    def get_scroll_pos(self):
        return self.scroll_pos

    def set_scroll_pos(self, value: float):
        if value < 0.0:
            self.scroll_pos = 0.0
        elif value > 1.0:
            self.scroll_pos = 1.0
        else:
            self.scroll_pos = value

    def mouse_input(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if (self.x <= mouse_pos[0] <= self.x + self.stroke) and (self.y <= mouse_pos[1] <= self.y + self.length):
            self.mouse_inside = True
        else:
            self.mouse_inside = False

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            self.mouse_clicked = True
            if self.mouse_inside:
                self.mouse_focus = True
        else:
            self.mouse_clicked = False

        if event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[0]:
            if self.mouse_focus:
                self.execute()
            self.mouse_focus = False

        if self.mouse_focus:
            if self.y <= mouse_pos[1] <= self.y + self.length:
                self.scroll_pos = (mouse_pos[1] - self.y) / self.length

    def execute(self):
        if self.release_command is not None:
            self.release_command()
