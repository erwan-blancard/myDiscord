import account
import network_manager
import ui.button_base
from overlays.overlay import *
from ui.button_text_input import ButtonTextInput


class ProfileOverlay(Overlay):

    def __init__(self):
        super().__init__()
        save_button_img = ui.button_base.create_button_surface(280)
        text.draw_centered_text("Sauvegarder", save_button_img.get_width() / 2, save_button_img.get_height() / 2, save_button_img, text.get_font(24))

        prev_btn_img = create_button_surface(32)
        next_btn_img = create_button_surface(32)
        text.draw_centered_text("<", prev_btn_img.get_width() / 2, prev_btn_img.get_height() / 2, prev_btn_img, text.get_font(24))
        text.draw_centered_text(">", next_btn_img.get_width() / 2, next_btn_img.get_height() / 2, next_btn_img, text.get_font(24))

        back_button_img = create_button_surface(40)
        text.draw_centered_text("«", back_button_img.get_width() / 2, back_button_img.get_height() / 2, back_button_img, text.get_font(24))

        self.buttons = [
            ButtonIcon(100, 400, 280, 40, save_button_img, command=lambda: self.__save_and_close()),
            ButtonIcon(50, 400, 40, 40, back_button_img, command=lambda: self.close()),
            ButtonIcon(170, 300, 32, 40, prev_btn_img, command=lambda: self.prev_pp()),
            ButtonIcon(270, 300, 32, 40, next_btn_img, command=lambda: self.next_pp())
        ]

        self.__cached_local_account = account.get_local_account()
        self.picture_index = self.__cached_local_account.get_picture_index()

        self.__name_button = ButtonTextInput(100, 120 - 32, 280, 32, default_text=self.__cached_local_account.get_name(), lock=True)
        self.__lastname_button = ButtonTextInput(100, 170 - 32, 280, 32, default_text=self.__cached_local_account.get_lastname(), lock=True)
        self.__email_button = ButtonTextInput(100, 220 - 32, 280, 32, default_text=self.__cached_local_account.get_email(), lock=True)

        self.show_error_message = False

    def __save_and_close(self):
        success = network_manager.get_instance().change_profile_picture(self.picture_index)
        if success:
            self.close()
            network_manager.get_instance().get_all_accounts()
        else:
            self.show_error_message = True

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

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        title = "Mon compte"
        text.draw_text("Prénom", 100, 100-32, frame)
        text.draw_text("Nom", 100, 150-32, frame)
        text.draw_text("Email", 100, 200-32, frame)

        text.draw_aligned_text("Changer l'image de profil", OVL_SIZE/2, 272, frame, text.get_font(24))

        frame.blit(account.PPS[self.picture_index], (480/2-4-account.PPS[self.picture_index].get_width()/2, 304))

        text.draw_aligned_text(title, OVL_SIZE / 2, 24-16, frame, text.get_font(48), shadow_color=(80, 80, 80), shadow_offset=6)
        self._render_buttons(frame)
        return frame

    def _render_buttons(self, surface: pygame.Surface):
        super()._render_buttons(surface)
        for button in [self.__name_button, self.__lastname_button, self.__email_button]:
            button.render(surface)

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()
        super().input(event)
        for button in [self.__name_button, self.__lastname_button, self.__email_button]:
            button.mouse_input(event, relative_to=(int(pygame.display.get_window_size()[0]/2 - OVL_SIZE/2), int(pygame.display.get_window_size()[1]/2 - OVL_SIZE/2)))
            button.key_input(event)
