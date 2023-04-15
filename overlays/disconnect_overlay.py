import network_manager
import ui.button_base
from overlays.overlay import *
from ui.text_box import TextBox


class DisconnectOverlay(Overlay):

    def __init__(self):
        super().__init__()
        yes_button_img = ui.button_base.create_button_surface(160)
        text.draw_centered_text("Oui", yes_button_img.get_width() / 2, yes_button_img.get_height() / 2, yes_button_img, text.get_font(24))
        no_button_img = ui.button_base.create_button_surface(160)
        text.draw_centered_text("Non", no_button_img.get_width() / 2, no_button_img.get_height() / 2, no_button_img, text.get_font(24))

        self.buttons = [
            ButtonIcon(160, 340, 160, 40, yes_button_img, command=lambda: self.disconnect()),
            ButtonIcon(160, 400, 160, 40, no_button_img, command=lambda: self.close())
        ]

    def disconnect(self):
        network_manager.disconnect()
        self.close()

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        text.draw_aligned_text("Confirmer", OVL_SIZE / 2, 32, frame, text.get_font(48), shadow_color=(80, 80, 80), shadow_offset=6)

        message_box = TextBox("Voulez-vous vous déconnecter ?", 80, 200, 320, text.get_font(24))
        message_box.render(frame)

        self._render_buttons(frame)
        return frame