import logging
import re
import telebot
from telebot.types import KeyboardButton

from ..constants import BotUserSteps, LanguageChoices
from .base import BaseController

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


class BotController(BaseController):
    def greeting(self):
        self.sync_user()
        self.send_message(message_text=self.messages('greeting'))

    def send_exception_message_to_user(self):
        step = self.step

        if step in [BotUserSteps.LISTING_LANGUAGE, BotUserSteps.EDIT_LANGUAGE]:
            self.list_language(text=self.t('press one button'))
        elif step == BotUserSteps.MAIN_MENU:
            self.main_menu(text=self.t('press one button'))
        elif step in [BotUserSteps.EDIT_PHONE_NUMBER, BotUserSteps.GET_PHONE_NUMBER]:
            self.get_phone_number()
        elif step == BotUserSteps.SETTINGS:
            self.settings(text=self.t('press one button'))


    def back_reply_button_handler(self):
        step = self.step

        if step in [BotUserSteps.EDIT_LANGUAGE, BotUserSteps.EDIT_PHONE_NUMBER]:
            self.settings()
        elif step == BotUserSteps.GET_PHONE_NUMBER:
            self.list_language()
        elif step == BotUserSteps.SETTINGS:
            self.main_menu()

    def back_inline_button_handler(self):
        pass

    def list_language(self, text: str = None, edit: bool = False):
        edit = edit or self.step == BotUserSteps.EDIT_LANGUAGE
        uzbek = KeyboardButton(text=self.messages('uzbek'))
        english = KeyboardButton(text=self.messages('english'))
        russian = KeyboardButton(text=self.messages('russian'))
        markup = self.reply_markup()
        markup.add(uzbek)
        markup.add(english, russian)
        if edit:
            markup.add(self.back_reply_button)
        self.send_message(message_text=text or self.messages('select the language'), reply_markup=markup)
        self.set_step(BotUserSteps.EDIT_LANGUAGE if edit else BotUserSteps.LISTING_LANGUAGE)

    def set_language(self):
        edit = self.step == BotUserSteps.EDIT_LANGUAGE
        languages = {
            self.messages('english'): LanguageChoices.ENGLISH,
            self.messages('uzbek'): LanguageChoices.UZBEK,
            self.messages('russian'): LanguageChoices.RUSSIAN
        }
        try:
            self.user.language = languages[self.message_text]
            self.user.save()
            if edit:
                self.settings(text=self.t('saved your language'))
            else:
                self.get_phone_number()
        except KeyError:
            self.list_language(text=self.messages("selected language doesn't exist"))

    def get_phone_number(self, edit: bool = False, text: str = None):
        if self.user.step == BotUserSteps.SETTINGS:
            self.send_message(message_text=self.t('your phone number').format(self.user.phone_number))

        edit = edit or self.step == BotUserSteps.EDIT_PHONE_NUMBER

        markup = self.reply_markup()
        markup.add(KeyboardButton(text=self.t('send number button'), request_contact=True))
        if edit:
            markup.add(self.main_menu_reply_button, self.back_reply_button)
        else:
            markup.add(self.back_reply_button)
        self.send_message(message_text=text or self.t('enter phone number or click button'),
                          reply_markup=markup)
        self.set_step(BotUserSteps.EDIT_PHONE_NUMBER if edit else BotUserSteps.GET_PHONE_NUMBER)

    def set_phone_number(self):
        if self.message.contact:
            phone_number = self.message.contact.phone_number
            phone_number = "+" + phone_number if not phone_number.startswith("+") else phone_number
        else:
            phone_number = self.message.text
            pattern =r'\+998\d{9}$'
            match = re.match(pattern, phone_number)
            if not match:
                self.get_phone_number(text=self.t('enter correct phone number'))
                return

        self.user.phone_number = phone_number
        self.user.save()
        if self.step == BotUserSteps.EDIT_PHONE_NUMBER:
            self.settings(text=self.t('saved'))
        else:
            self.main_menu(text=self.t('guide'))

    def send_guide(self):
        self.send_message(message_text=self.t('guide'))

    def main_menu(self, text: str = None, edit: bool = False):
        self.sync_user()
        markup = self.reply_markup()
        markup.add(KeyboardButton(text=self.t('settings')))
        if edit:
            self.delete_message(message_id=self.callback_query_id)
        self.send_message(message_text=text or self.t('main menu'), reply_markup=markup)
        self.set_step(BotUserSteps.MAIN_MENU)

    def settings(self, text: str = None):
        markup = self.reply_markup()
        markup.add(KeyboardButton(text=f"{self.t('language flag')} {self.t('change language')}"),
                   KeyboardButton(text=self.t('change number button')))
        markup.add(self.main_menu_reply_button)
        self.send_message(message_text=text or self.t('settings'), reply_markup=markup)
        self.set_step(BotUserSteps.SETTINGS)
