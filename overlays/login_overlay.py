import json

import pygame

import network_manager
import overlays.overlay
import text
import ui.button_base
from overlays.create_account_overlay import CreateAccountOverlay
from overlays.overlay import *

import threading

from ui.button_text_input import ButtonTextInput


class LoginOverlay(Overlay):
    
    def __init__(self):
        super().__init__()
        login_button_img = ui.button_base.create_button_surface(280)
        text.draw_centered_text("Se connecter", login_button_img.get_width()/2, login_button_img.get_height()/2, login_button_img, text.get_font(24))

        create_acc_txt = "Créer un compte"
        create_acc_font = text.get_font(20)
        create_acc_img = pygame.Surface((create_acc_font.size(create_acc_txt)[0], create_acc_font.size(create_acc_txt)[1]), pygame.SRCALPHA)
        text.draw_text(create_acc_txt, 0, 0, create_acc_img, create_acc_font, color=(50, 50, 255))

        self.buttons = [
            ButtonIcon(OVL_SIZE/2-int(create_acc_img.get_width()/2), 380-create_acc_img.get_height(), create_acc_img.get_width(), create_acc_img.get_height(), create_acc_img, command=lambda: self.set_create_account_overlay()),
            ButtonIcon(100, 400, 280, 40, login_button_img, command=lambda: self.login())
        ]

        back_button_img = ui.button_base.create_button_surface(280)
        text.draw_centered_text("Retour", back_button_img.get_width()/2, back_button_img.get_height()/2, back_button_img, text.get_font(24))
        self.__back_button = ButtonIcon(100, 400, 280, 40, back_button_img, command=lambda: self.__back())

        last_email = ""
        try:
            file = open("last_profile.json", "r")
            json_dict = json.load(file)
            file.close()
            last_email = str(json_dict["email"])
        except Exception as e:
            print(e)

        self.warning_message = ""
        self.pending_connect = False
        self.connection_state = 0

        self.__email_button = ButtonTextInput(100, 140, 280, 48, default_text=last_email, font=text.get_font(24))
        self.__password_button = ButtonTextInput(100, 240, 280, 48, font=text.get_font(24), hide_text=True)

    def set_create_account_overlay(self):
        self.__back()
        self.close()
        overlays.overlay.next_overlay = CreateAccountOverlay()

    def update(self):
        if self.pending_connect:
            self.can_close = self.connection_state == 1

    def __back(self):
        self.connection_state = 0
        self.warning_message = ""
        self.pending_connect = False

    def __thread_login(self):
        self.connection_state = network_manager.get_instance().connect_as(self.__email_button.get_text(), self.__password_button.get_text())
        if self.connection_state == -1:
            self.warning_message = "L'email ou le mot de passe est incorrect !"
        elif self.connection_state == -2:
            self.warning_message = "Impossible d'exécuter la requête !"
        else:
            self.warning_message = ""

    def login(self):
        login_thread = threading.Thread(group=None, target=lambda: self.__thread_login(), name="LoginThread")
        login_thread.start()
        self.pending_connect = True

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        title = "Se connecter"
        if self.pending_connect:
            if self.connection_state < 0:
                title = "Oups !"
                text.draw_centered_text(self.warning_message, OVL_SIZE / 2, OVL_SIZE / 2, frame, text.get_font(20), color=(255, 0, 0), shadow_color=(100, 0, 0), shadow_offset=2)
            else:
                title = "Connexion..."
        else:
            text.draw_text("Email", 100, 120, frame)
            text.draw_text("Mot de passe", 100, 220, frame)

        text.draw_aligned_text(title, OVL_SIZE / 2, 32, frame, text.get_font(48), shadow_color=(80, 80, 80), shadow_offset=6)
        self._render_buttons(frame)
        return frame

    def _render_buttons(self, surface: pygame.Surface):
        if not self.pending_connect:
            super()._render_buttons(surface)
            self.__email_button.render(surface)
            self.__password_button.render(surface)
        elif self.connection_state < 0:  # errors -1 and -2 of connect_as()
            self.__back_button.render(surface)

    def input(self, event: pygame.event.Event):
        if not self.pending_connect:
            super().input(event)
            for button in [self.__email_button, self.__password_button]:
                button.mouse_input(event, relative_to=(int(pygame.display.get_window_size()[0]/2 - OVL_SIZE/2), int(pygame.display.get_window_size()[1]/2 - OVL_SIZE/2)))
                button.key_input(event)
        elif self.connection_state < 0:     # errors -1 and -2 of connect_as()
            self.__back_button.mouse_input(event, relative_to=(int(pygame.display.get_window_size()[0]/2 - OVL_SIZE/2), int(pygame.display.get_window_size()[1]/2 - OVL_SIZE/2)))
