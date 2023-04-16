import network_manager
import ui.button_base
from overlays.overlay import *
from ui.text_box import TextBox


class LoginFailOverlay(Overlay):

    def __init__(self, message):
        super().__init__()
        self.message = message

        button_img = ui.button_base.create_button_surface(240)
        text.draw_centered_text("Réessayer", button_img.get_width() / 2, button_img.get_height() / 2, button_img, text.get_font(24))
        quit_button_img = ui.button_base.create_button_surface(240)
        text.draw_centered_text("Quitter", quit_button_img.get_width() / 2, quit_button_img.get_height() / 2, quit_button_img, text.get_font(24))

        self.buttons = [
            ButtonIcon(120, 370, 240, 40, button_img, command=lambda: self.reconnect()),
            ButtonIcon(120, 420, 240, 40, quit_button_img, command=lambda: exit(0))
        ]

    def reconnect(self):
        network_manager.new_instance()
        self.close()

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        text.draw_aligned_text("Erreur !", OVL_SIZE / 2, 32, frame, text.get_font(48), shadow_color=(80, 80, 80), shadow_offset=6)

        message_box = TextBox(self.message, 80, 160, 320, text.get_font(24), line_limit=9)
        message_box.render(frame)

        self._render_buttons(frame)
        return frame
