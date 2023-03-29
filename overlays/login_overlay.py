from overlays.overlay import *


class LoginOverlay(Overlay):
    
    def __init__(self):
        super().__init__()
        self.buttons = [

        ]

    def get_rendered_surface(self):
        frame = pygame.Surface((OVL_SIZE, OVL_SIZE), pygame.SRCALPHA)
        frame.fill((120, 120, 120))
        text.draw_aligned_text("Se connecter", OVL_SIZE/2, 32, frame, text.get_font(48), shadow_color=(80, 80, 80), shadow_offset=6)
        self._render_buttons(frame)
        return frame

    def input(self, event: pygame.event.Event):
        super().input(event)
