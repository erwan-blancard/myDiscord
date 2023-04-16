import ui.button_base
from overlays.overlay import *
from ui.text_box import TextBox


class GenericOverlay(Overlay):

    def __init__(self, title="Hello World!", message="Je suis un Overlay générique !"):
        super().__init__()
        self.title = title
        self.message = message

        button_img = ui.button_base.create_button_surface(160)
        text.draw_centered_text("OK", button_img.get_width() / 2, button_img.get_height() / 2, button_img, text.get_font(24))

        self.buttons = [
            ButtonIcon(160, 400, 160, 40, button_img, command=lambda: self.close())
        ]

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        text.draw_aligned_text(self.title, OVL_SIZE / 2, 32, frame, text.get_font(48), shadow_color=(80, 80, 80), shadow_offset=6)

        message_box = TextBox(self.message, 80, 160, 320, text.get_font(24), line_limit=9)
        message_box.render(frame)

        self._render_buttons(frame)
        return frame
