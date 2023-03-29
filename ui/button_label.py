from ui.button_base import *


class ButtonLabel(BaseButton):

    def __init__(self, label, x, y, width, height, command=None, center_text=True, font=text.font(), color=text.DEFAULT_COLOR):
        super().__init__(x, y, width, height, command)
        self.label = label
        self.font = font
        self.center_text = center_text
        self.color = color

    def render(self, screen: pygame.Surface):
        if self.center_text:
            text.draw_centered_text(self.label, self.x+(self.width/2), self.y+(self.height/2), screen, self.font, color=self.color)
        else:
            text.draw_text(self.label, self.x, self.y + (self.height - self.font.size(self.label)[1])/2, screen, self.font, color=self.color)
        super().render(screen)
