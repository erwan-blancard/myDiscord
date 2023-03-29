import pygame

import text


class TextBox:

    def __init__(self, message: str, x, y, lenght, font: pygame.font.Font = text.font(), line_limit=-1):
        self.__message = message
        self.x = x
        self.y = y
        self.__lenght = lenght
        self.__font = font
        self.__lines = []
        self.__line_limit = line_limit
        self.parse_lines()

    def get_lenght(self):
        return self.__lenght

    def get_height(self):
        if self.__line_limit > 0:
            return self.__font.size(self.__message)[1]*self.__line_limit
        else:
            return self.__font.size(self.__message)[1]*len(self.__lines)

    def change_font(self, font: pygame.font.Font):
        self.__font = font
        self.parse_lines()

    def change_text(self, message: str):
        if message != self.__message:
            self.__message = message
            self.parse_lines()

    def parse_lines(self):
        words = self.__message.split()
        lines: list[str] = [""]
        current_line = 0
        for word in words:
            if len(lines[current_line]) != 0 and self.__font.size(lines[current_line])[0] + self.__font.size(" "+word)[0] >= self.__lenght:
                current_line += 1
                lines.append("")
            if len(lines[current_line]) != 0:
                lines[current_line] += " "
            lines[current_line] += word

        self.__lines = lines

    def render(self, screen: pygame.Surface, color=text.DEFAULT_COLOR):
        # draw the lines
        char_height = self.__font.size(self.__message)[1]
        for i in range(len(self.__lines)):
            if i == self.__line_limit-1:
                text.draw_text(self.__lines[i][:-3] + "...", self.x, self.y + char_height * i, screen, self.__font, color=color)
                break
            else:
                text.draw_text(self.__lines[i], self.x, self.y + char_height*i, screen, self.__font, color=color)
