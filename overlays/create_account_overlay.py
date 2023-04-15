import random

import account
import network_manager
import overlays.overlay
from overlays.generic_overlay import GenericOverlay
from ui.button_base import create_button_surface
from overlays.overlay import *
from ui.button_text_input import ButtonTextInput


class CreateAccountOverlay(Overlay):
    
    def __init__(self):
        super().__init__()
        create_button_img = create_button_surface(280)
        text.draw_centered_text("Créer un compte", create_button_img.get_width() / 2, create_button_img.get_height() / 2, create_button_img, text.get_font(24))

        back_button_img = create_button_surface(40)
        text.draw_centered_text("«", back_button_img.get_width() / 2, back_button_img.get_height() / 2, back_button_img, text.get_font(24))

        prev_btn_img = create_button_surface(32)
        next_btn_img = create_button_surface(32)
        text.draw_centered_text("<", prev_btn_img.get_width() / 2, prev_btn_img.get_height() / 2, prev_btn_img, text.get_font(24))
        text.draw_centered_text(">", next_btn_img.get_width() / 2, next_btn_img.get_height() / 2, next_btn_img, text.get_font(24))

        self.buttons = [
            ButtonIcon(100, 430, 280, 40, create_button_img, command=lambda: self.create_account()),
            ButtonIcon(50, 430, 40, 40, back_button_img, command=lambda: self.close()),
            ButtonIcon(170, 364-32, 32, 40, prev_btn_img, command=lambda: self.prev_pp()),
            ButtonIcon(270, 364-32, 32, 40, next_btn_img, command=lambda: self.next_pp())
        ]

        self.warning_message = ""

        self.picture_index = random.randint(0, 7)
        self.__name_button = ButtonTextInput(100, 120-32, 280, 32)
        self.__lastname_button = ButtonTextInput(100, 170-32, 280, 32)
        self.__email_button = ButtonTextInput(100, 220-32, 280, 32)
        self.__password_button = ButtonTextInput(100, 270-32, 280, 32, hide_text=True)
        self.__password_confirm_button = ButtonTextInput(100, 320-32, 280, 32, hide_text=True)

    def prev_pp(self):
        if self.picture_index > 0:
            self.picture_index -= 1
        else:
            self.picture_index = len(account.PPS) - 1

    def next_pp(self):
        if self.picture_index < len(account.PPS) - 1:
            self.picture_index += 1
        else:
            self.picture_index = 0

    def create_account(self):
        at_index = self.__email_button.get_text().find("@")
        at_count = self.__email_button.get_text().count("@")
        if len(self.__name_button.get_text()) <= 2:
            self.warning_message = "Prénom trop court !"
        elif len(self.__name_button.get_text()) > 255:
            self.warning_message = "Prénom trop long !"
        elif len(self.__lastname_button.get_text()) <= 2:
            self.warning_message = "Nom trop court !"
        elif len(self.__lastname_button.get_text()) > 255:
            self.warning_message = "Nom trop long !"
        elif at_index == -1 or at_index == len(self.__email_button.get_text())-1 or at_index == 0 or at_count != 1 or len(self.__email_button.get_text()) > 255:
            self.warning_message = "Email non valide !"
        elif network_manager.get_instance().account_exists(self.__email_button.get_text()):
            self.warning_message = "Adresse déjà utilisée !"
        elif len(self.__password_button.get_text()) < 4:
            self.warning_message = "Mot de passe trop court !"
        elif self.__password_button.get_text() != self.__password_confirm_button.get_text():
            self.warning_message = "Les mots de passe ne correspondent pas !"
        else:
            success = network_manager.get_instance().create_account(self.__name_button.get_text(), self.__lastname_button.get_text(), self.__email_button.get_text(), self.__password_button.get_text(), picture_index=self.picture_index)
            if success:
                self.close()
                overlays.overlay.next_overlay = GenericOverlay(title="Compte créé !", message="Le compte a été créé avec succès !")
            else:
                self.warning_message = "Aïe ! Une erreur est survenue !"

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        title = "Créer un compte"
        text.draw_centered_text(self.warning_message, OVL_SIZE / 2, 400, frame, text.get_font(20), color=(255, 0, 0), shadow_color=(100, 0, 0), shadow_offset=2)
        text.draw_text("Prénom", 100, 100-32, frame)
        text.draw_text("Nom", 100, 150-32, frame)
        text.draw_text("Email", 100, 200-32, frame)
        text.draw_text("Mot de passe", 100, 250-32, frame)
        text.draw_text("Confirmer le mot de passe", 100, 300-32, frame)

        frame.blit(account.PPS[self.picture_index], (480/2-4-account.PPS[self.picture_index].get_width()/2, 336))

        text.draw_aligned_text(title, OVL_SIZE / 2, 24-16, frame, text.get_font(48), shadow_color=(80, 80, 80), shadow_offset=6)
        self._render_buttons(frame)
        return frame

    def _render_buttons(self, surface: pygame.Surface):
        super()._render_buttons(surface)
        for button in [self.__name_button, self.__lastname_button, self.__email_button, self.__password_button, self.__password_confirm_button]:
            button.render(surface)

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.warning_message = ""
        super().input(event)
        for button in [self.__name_button, self.__lastname_button, self.__email_button, self.__password_button, self.__password_confirm_button]:
            button.mouse_input(event, relative_to=(int(pygame.display.get_window_size()[0]/2 - OVL_SIZE/2), int(pygame.display.get_window_size()[1]/2 - OVL_SIZE/2)))
            button.key_input(event)
