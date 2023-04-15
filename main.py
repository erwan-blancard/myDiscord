import pygame

from channel import Channel
from message import Message
import network_manager
from overlays.login_overlay import LoginOverlay
from overlays.overlay import *
import overlays.overlay
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


overlay_list: list[Overlay] = []
channels: list[Channel] = []

CURSOR = pygame.image.load("res/cursor.png")
cursor = pygame.cursors.compile((" "*8," "*8," "*8," "*8," "*8," "*8," "*8," "*8))
pygame.mouse.set_cursor((8, 8), (0, 0), *cursor)

running = True

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
        if len(overlay_list) > 0:
            overlay_list[::-1][0].input(event)
        else:
            pass

    # update
    pass

    # add overlay (overlays.overlay.next_overlay)
    if overlays.overlay.next_overlay is not None:
        overlay_list.append(overlays.overlay.next_overlay)
        overlays.overlay.next_overlay = None

    if len(overlay_list) == 0 and not network_manager.is_connected():
        overlay_list.append(LoginOverlay())


    for overlay in overlay_list:
        overlay.update()
    for overlay in overlay_list:
        if overlay.can_close:
            overlay_list.remove(overlay)
            break

    screen.fill((60, 60, 60))

    # render
    pass
    for overlay in overlay_list:
        render_overlay(screen)
        screen.blit(overlay.get_rendered_surface(), (screen.get_width()/2 - OVL_SIZE/2, screen.get_height()/2 - OVL_SIZE/2))

    # draw mouse
    if pygame.mouse.get_focused():
        screen.blit(CURSOR, pygame.mouse.get_pos())

    pygame.display.flip()
