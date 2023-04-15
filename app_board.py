import threading
import time

import pygame

import network_manager
import overlays.overlay
import text
import ui.button_base
from channel import Channel
from overlays.add_channel_overlay import AddChannelOverlay
from overlays.disconnect_overlay import DisconnectOverlay
from ui.button_base import BaseButton
from ui.button_icon import ButtonIcon
from ui.button_text_input import ButtonTextInput
from ui.scrolling_message_list import ScrollingMessageList
from ui.scrolling_channel_list import ScrollingChannelList

NEXT_UPDATE = 7    # in seconds

MESSAGE_LIST_POS = (256, 48)
MESSAGE_LIST_Y_OFFSET = 96


class AppBoard:

    def __init__(self):
        self.channels: list[Channel] = []
        self.__last_update_time = 0
        self.__update_pending = False
        self.__current_channel_id = -1
        self.__cached_channel_index = -1

        self.__cached_message_list: ScrollingMessageList = None
        self.__cached_channel_list: ScrollingChannelList = None

        add_channel_img = ui.button_base.create_button_surface(192)
        text.draw_centered_text("Ajouter...", add_channel_img.get_width() / 2, add_channel_img.get_height() / 2, add_channel_img, text.get_font(24))
        self.__add_channel_button = ButtonIcon(8, 8, 192, 40, add_channel_img, command=lambda: self.open_add_channel_overlay())

        self.__message_input = ButtonTextInput(MESSAGE_LIST_POS[0], pygame.display.get_window_size()[1]-(MESSAGE_LIST_Y_OFFSET)/2, pygame.display.get_window_size()[0]-MESSAGE_LIST_POS[0]-128, 48)
        self.__pending_message = False

        self.warning_message = ""

        self.send_message_img = ui.button_base.create_button_surface(128)
        text.draw_centered_text("Envoyer", self.send_message_img.get_width() / 2, self.send_message_img.get_height() / 2, self.send_message_img, text.get_font(24))
        self.__send_message_button = ButtonIcon(MESSAGE_LIST_POS[0]+pygame.display.get_window_size()[0]-MESSAGE_LIST_POS[0]-128, pygame.display.get_window_size()[1]-(MESSAGE_LIST_Y_OFFSET)/2, 128, 48, self.send_message_img, command=lambda: self.__send_message())

        self.__pending_password_check = False       # used when entering a password protected channel
        self.__password_input = ButtonTextInput(MESSAGE_LIST_POS[0]+32, pygame.display.get_window_size()[1]/2, 284, 40, hide_text=True)

        self.validate_password_img = ui.button_base.create_button_surface(128)
        text.draw_centered_text("Valider", self.validate_password_img.get_width() / 2, self.validate_password_img.get_height() / 2, self.validate_password_img, text.get_font(24))
        self.__validate_password = ButtonIcon(MESSAGE_LIST_POS[0]+32+284, pygame.display.get_window_size()[1]/2, 128, 40, self.validate_password_img, command=lambda: self.__validate_channel_password())

        self.disconnect_img = ui.button_base.create_button_surface(200)
        text.draw_centered_text("Se déconnecter", self.disconnect_img.get_width() / 2, self.disconnect_img.get_height() / 2, self.disconnect_img, text.get_font(24))
        self.__disconnect_button = ButtonIcon(pygame.display.get_window_size()[0]-8-200, 8, 200, 40, self.disconnect_img, command=lambda: self.open_disconnect_menu())

        self.update_client()

    def open_disconnect_menu(self):
        overlays.overlay.next_overlay = DisconnectOverlay()

    def __validate_channel_password(self):
        if self.__pending_password_check and len(self.__password_input.get_text()) > 0:
            if network_manager.get_instance().is_channel_password_valid(self.__current_channel_id, self.__password_input.get_text()):
                self.__pending_password_check = False
                self.__password_input.clear_text()

    def __thread_send_message(self, message):
        success = network_manager.get_instance().send_message(self.__current_channel_id, message)
        if not success:
            self.warning_message = "Impossible d'envoyer le dernier message."
        else:
            self.update_client()
        self.__pending_message = False

    def __send_message(self):
        if not self.__pending_message and len(self.__message_input.get_text().strip()) > 0:
            send_message_thread = threading.Thread(group=None, target=lambda message=self.__message_input.get_text(): self.__thread_send_message(message), name="SendMessageThread")
            send_message_thread.start()
            self.__message_input.clear_text()
            self.__pending_message = True
            self.warning_message = ""

    def open_add_channel_overlay(self):
        overlays.overlay.next_overlay = AddChannelOverlay()
        self.__last_update_time = 0

    def set_channel(self, channel_id, erase_message_list=False):
        """Sets the current channel to view."""
        if erase_message_list:
            self.__cached_message_list = None

        self.__current_channel_id = -1
        self.__cached_channel_index = -1
        i = 0
        while i < len(self.channels):
            if self.channels[i].get_id() == channel_id:
                self.__current_channel_id = self.channels[i].get_id()
                self.__cached_channel_index = i
                if erase_message_list and self.channels[self.__cached_channel_index].is_private():
                    self.__pending_password_check = True
                break
            i += 1
        if self.__current_channel_id != -1:
            scroll_pos = 1.0
            if self.__cached_message_list is not None:
                scroll_pos = self.__cached_message_list.scroll_bar.get_scroll_pos()
            self.__cached_message_list = ScrollingMessageList(network_manager.get_instance().get_channel_messages(self.__current_channel_id), MESSAGE_LIST_POS[0], MESSAGE_LIST_POS[1], pygame.display.get_window_size()[0] - MESSAGE_LIST_POS[0], pygame.display.get_window_size()[1] - MESSAGE_LIST_Y_OFFSET, scroll_pos=scroll_pos)

    def __thread_update(self):
        channels = network_manager.get_instance().get_channels()    # fetch channels
        network_manager.get_instance().get_all_accounts()           # fetch accounts

        self.channels = channels
        self.__cached_channel_list = ScrollingChannelList(self.channels, 8, 56, pygame.display.get_window_size()[1]-56)
        if self.__current_channel_id != -1:
            self.set_channel(self.__current_channel_id)

        self.__last_update_time = time.time()
        self.__update_pending = False

    def update_client(self):
        update_thread = threading.Thread(group=None, target=lambda: self.__thread_update(), name="UpdateThread")
        update_thread.start()
        self.__update_pending = True

    def update_channel_and_message_list_size(self):
        self.__disconnect_button = ButtonIcon(pygame.display.get_window_size()[0] - 8 - 200, 8, 200, 40, self.disconnect_img, command=lambda: self.open_disconnect_menu())
        self.__password_input = ButtonTextInput(MESSAGE_LIST_POS[0] + 32, pygame.display.get_window_size()[1] / 2, 284, 40, default_text=self.__password_input.get_text(), hide_text=True)
        self.__validate_password = ButtonIcon(MESSAGE_LIST_POS[0] + 32+284, pygame.display.get_window_size()[1] / 2, 128, 40, self.validate_password_img, command=lambda: self.__validate_channel_password())
        if self.__cached_message_list is not None:
            self.__cached_message_list = ScrollingMessageList(self.__cached_message_list.get_message_list(), MESSAGE_LIST_POS[0], MESSAGE_LIST_POS[1], pygame.display.get_window_size()[0]-MESSAGE_LIST_POS[0], pygame.display.get_window_size()[1]-MESSAGE_LIST_Y_OFFSET, scroll_pos=self.__cached_message_list.scroll_bar.get_scroll_pos())
            self.__message_input = ButtonTextInput(MESSAGE_LIST_POS[0], pygame.display.get_window_size()[1]-(MESSAGE_LIST_Y_OFFSET)/2, pygame.display.get_window_size()[0]-MESSAGE_LIST_POS[0]-128, 48, default_text=self.__message_input.get_text())
            self.__send_message_button = ButtonIcon(MESSAGE_LIST_POS[0]+pygame.display.get_window_size()[0]-MESSAGE_LIST_POS[0]-128, pygame.display.get_window_size()[1]-(MESSAGE_LIST_Y_OFFSET)/2, 128, 48, self.send_message_img, command=lambda: self.__send_message())
        if self.__cached_channel_list is not None:
            self.__cached_channel_list = ScrollingChannelList(self.__cached_channel_list.get_channel_list(), 8, 56, pygame.display.get_window_size()[1]-56, scroll_pos=self.__cached_channel_list.scroll_bar.get_scroll_pos())

    def update(self):
        if time.time() > self.__last_update_time + NEXT_UPDATE and not self.__update_pending:
            self.update_client()
        if self.__cached_channel_list is not None:
            channel_id = self.__cached_channel_list.get_selected_channel_id()
            if channel_id != -1:
                self.set_channel(channel_id, erase_message_list=True)

    def render(self, screen: pygame.Surface):
        def render_messages():
            if not self.channels[self.__cached_channel_index].is_voice_chat():  # text chat
                self.__cached_message_list.render(screen)
                self.__message_input.render(screen)
                self.__send_message_button.render(screen)
                if self.__pending_message:
                    text.draw_text("Envoi...", MESSAGE_LIST_POS[0], MESSAGE_LIST_POS[1] + pygame.display.get_window_size()[1] - (MESSAGE_LIST_Y_OFFSET) / 2 - 48, screen, text.get_font(24))
                text.draw_text(self.warning_message, MESSAGE_LIST_POS[0], MESSAGE_LIST_POS[1] + pygame.display.get_window_size()[1] - (MESSAGE_LIST_Y_OFFSET) / 2 - 48, screen, text.get_font(24), color=(255, 0, 0))
            else:  # voice chat
                text.draw_aligned_text("Bienvenue dans un channel vocal!", screen.get_width() / 2 + 250 / 2, screen.get_height()/2 - 24, screen, text.get_font(24))
                text.draw_aligned_text("(pas implémenté)", screen.get_width() / 2 + 250 / 2, screen.get_height()/2 + 24, screen, text.get_font(24))

        self.__add_channel_button.render(screen)
        self.__disconnect_button.render(screen)
        if self.__current_channel_id != -1 and self.__cached_message_list is not None:     # render channel chat
            if self.channels[self.__cached_channel_index].is_private():
                if not self.__pending_password_check:
                    render_messages()
                else:
                    text.draw_text("Mot de passe:", MESSAGE_LIST_POS[0]+32, screen.get_height()/2 - 24, screen, text.get_font(24))
                    self.__password_input.render(screen)
                    self.__validate_password.render(screen)
            else:
                render_messages()
        if self.__cached_channel_list is not None:          # render channel list
            self.__cached_channel_list.render(screen)

    def input(self, event: pygame.event.Event):
        self.__add_channel_button.mouse_input(event)
        self.__disconnect_button.mouse_input(event)
        if self.__pending_password_check:
            self.__password_input.mouse_input(event)
            self.__password_input.key_input(event)
            self.__validate_password.mouse_input(event)

        if not self.channels[self.__cached_channel_index].is_voice_chat() and self.__current_channel_id != -1 and self.__cached_message_list is not None:  # input for message list
            self.__cached_message_list.mouse_input(event)
            self.__message_input.mouse_input(event)
            if not self.__pending_message:
                self.__message_input.key_input(event)
            self.__send_message_button.mouse_input(event)
        if self.__cached_channel_list is not None:      # input for channel list
            self.__cached_channel_list.mouse_input(event)