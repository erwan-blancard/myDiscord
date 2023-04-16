import network_manager
from overlays.overlay import *
from ui.button_text_input import ButtonTextInput
from ui.truefalse_button import TrueFalseButton


class AddChannelOverlay(Overlay):

    def __init__(self):
        super().__init__()
        create_button_img = create_button_surface(280)
        text.draw_centered_text("Créer", create_button_img.get_width() / 2, create_button_img.get_height() / 2, create_button_img, text.get_font(24))

        back_button_img = create_button_surface(40)
        text.draw_centered_text("«", back_button_img.get_width() / 2, back_button_img.get_height() / 2, back_button_img, text.get_font(24))

        self.warning_message = ""

        self.__channel_type_button = TrueFalseButton(100, 220, 40, pygame.image.load("res/button_chat.png"), pygame.image.load("res/button_voice_chat.png"))
        self.__is_private_button = TrueFalseButton(340, 220, 40, pygame.image.load("res/button_unlocked.png"), pygame.image.load("res/button_locked.png"))

        self.buttons = [
            ButtonIcon(100, 400, 280, 40, create_button_img, command=lambda: self.create_channel()),
            ButtonIcon(50, 400, 40, 40, back_button_img, command=lambda: self.close()),
            self.__is_private_button,
            self.__channel_type_button
        ]
        self.__channel_name_button = ButtonTextInput(100, 160, 280, 40)
        self.__channel_password_button = ButtonTextInput(100, 300, 280, 40)

    def create_channel(self):
        if len(self.__channel_name_button.get_text()) < 1 or len(self.__channel_name_button.get_text()) > 255:
            self.warning_message = "Nom invalide !"
        elif self.__is_private_button.activated and len(self.__channel_password_button.get_text()) < 3:
            self.warning_message = "Mot de passe trop court !"
        else:
            success = network_manager.get_instance().create_channel(self.__channel_name_button.get_text(), self.__is_private_button.activated, self.__channel_type_button.activated, self.__channel_password_button.get_text())
            if success:
                self.close()
            else:
                self.warning_message = "Une erreur est survenue !"

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        title = "Nouveau channel"
        text.draw_centered_text(self.warning_message, OVL_SIZE / 2, 360, frame, text.get_font(20), color=(255, 0, 0), shadow_color=(100, 0, 0), shadow_offset=2)
        text.draw_text("Nom", 100, 140, frame)
        if self.__is_private_button.activated:
            text.draw_text("Mot de passe", 100, 280, frame)

        text.draw_aligned_text(title, OVL_SIZE / 2, 32, frame, text.get_font(48), shadow_color=(80, 80, 80), shadow_offset=6)
        self._render_buttons(frame)
        return frame

    def _render_buttons(self, surface: pygame.Surface):
        super()._render_buttons(surface)
        self.__channel_name_button.render(surface)
        if self.__is_private_button.activated:
            self.__channel_password_button.render(surface)

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.warning_message = ""
            if event.key == pygame.K_ESCAPE:
                self.close()
        super().input(event)
        self.__channel_name_button.mouse_input(event, relative_to=(int(pygame.display.get_window_size()[0]/2 - OVL_SIZE/2), int(pygame.display.get_window_size()[1]/2 - OVL_SIZE/2)))
        self.__channel_name_button.key_input(event)
        if self.__is_private_button.activated:
            self.__channel_password_button.mouse_input(event, relative_to=(int(pygame.display.get_window_size()[0] / 2 - OVL_SIZE / 2), int(pygame.display.get_window_size()[1] / 2 - OVL_SIZE / 2)))
            self.__channel_password_button.key_input(event)
