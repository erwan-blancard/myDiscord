import pygame

from channel import Channel
from message import Message
import network_manager
from overlays.login_overlay import LoginOverlay
from overlays.overlay import *
from ui.scrolling_message_list import ScrollingMessageList

pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("MineDiscord")
pygame.display.set_icon(pygame.image.load("res/icon.png"))

fullscreen = False
prev_size = pygame.display.get_window_size()


def enable_fullscreen():
    global fullscreen
    global prev_size
    prev_size = pygame.display.get_window_size()
    pygame.display.set_mode(flags=pygame.FULLSCREEN)
    fullscreen = True


def disable_fullscreen():
    global screen
    global fullscreen
    screen = pygame.display.set_mode(prev_size)
    fullscreen = False


connected = False

overlays: list[Overlay] = []
channels: list[Channel] = []

CURSOR = pygame.image.load("res/cursor.png")
cursor = pygame.cursors.compile((" "*8," "*8," "*8," "*8," "*8," "*8," "*8," "*8))
pygame.mouse.set_cursor((8, 8), (0, 0), *cursor)

running = True

messagessss = Message(0, "1111", 0, 3, "10:00")
messages = ScrollingMessageList([messagessss]*18+[Message(0, "2d azdad a zdza"*8, 0, -1, "11:00")]+[messagessss]*18+[Message(0, "2d azdad a zdza"*8, 0, -1, "11:00")], 200, 0, 600, 600)

overlays.append(LoginOverlay())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            if fullscreen:
                disable_fullscreen()
            else:
                enable_fullscreen()
        # input
        if len(overlays) > 0:
            overlays[::-1][0].input(event)
        else:
            messages.mouse_input(event)
            pass

    # update
    pass
    for overlay in overlays:
        overlay.update()

    screen.fill((60, 60, 60))

    # render
    channell = Channel(0, "demelmeldazdaqs", 1, 0)
    screen.blit(channell.get_rendered_label(), (0, 0))

    messages.render(screen)
    pass
    for overlay in overlays:
        render_overlay(screen)
        screen.blit(overlay.get_rendered_surface(), (screen.get_width()/2 - OVL_SIZE/2, screen.get_height()/2 - OVL_SIZE/2))

    # draw mouse
    if pygame.mouse.get_focused():
        screen.blit(CURSOR, pygame.mouse.get_pos())

    pygame.display.flip()
