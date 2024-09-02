from typing import Optional, Union, List

import telebot
from telebot.types import (
    Message,
    KeyboardButton,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    ReactionType,
    ReplyKeyboardRemove
)

from ..models import TelegramUser
from ..strings import messages
from ..constants import BotUserSteps, CallbackData, LanguageChoices, EXCEPTION_CHANNEL_ID


class BaseController:
    def __init__(self, message: Message, bot: telebot.TeleBot) -> None:
        self.bot = bot
        self.message = message
        self.user = TelegramUser.objects.get_or_create(chat_id=self.chat_id)[0]
        self.step = self.user.step

    @property
    def chat_id(self):
        return self.message.from_user.id

    @property
    def message_id(self):
        return self.message.message_id

    @property
    def message_text(self):
        return self.message.text

    @property
    def callback_query_id(self):
        return self.message.message.message_id

    @property
    def callback_data(self):
        return self.message.data if hasattr(self.message, 'data') else None

    @property
    def main_menu_reply_button(self):
        return KeyboardButton(text=self.t('main menu'))

    @property
    def main_menu_inline_button(self):
        return InlineKeyboardButton(self.t('main menu'), callback_data=CallbackData.MAIN_MENU_BUTTON)

    @property
    def back_reply_button(self):
        return KeyboardButton(text=self.t('back button'))

    @property
    def back_inline_button(self):
        return InlineKeyboardButton(self.t('back button'), callback_data=CallbackData.BACK_BUTTON)

    @property
    def skip_reply_button(self):
        return KeyboardButton(text=self.t('skip button'))

    @property
    def skip_inline_button(self):
        return InlineKeyboardButton(text=self.t('skip button'), callback_data=CallbackData.SKIP)

    @property
    def continue_reply_button(self):
        return KeyboardButton(text=self.t('continue button'))

    @property
    def continue_inline_button(self):
        return InlineKeyboardButton(text=self.t('continue button'), callback_data=CallbackData.CONTINUE)

    @property
    def cancel_reply_button(self):
        return KeyboardButton(text=self.t('cancel button'))

    @staticmethod
    def messages(code: str) -> str:
        return messages[code]

    @staticmethod
    def inline_markup(row_width=2) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(row_width=row_width)

    @staticmethod
    def reply_markup(row_width=2, one_time_keyboard=False) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=one_time_keyboard, resize_keyboard=True)

    def sync_user(self) -> None:
        if self.message.from_user.last_name:
            self.user.name = f"{self.message.from_user.first_name} {self.message.from_user.last_name}"
        else:
            self.user.name = self.message.from_user.first_name
        self.user.username = self.message.from_user.username
        self.user.save()

    def t(self, code: str, language: LanguageChoices = None) -> str:
        if language:
            return messages.get(language).get(code)
        if self.user.language:
            return messages.get(self.user.language).get(code)
        else:
            return code

    def set_step(self, step: BotUserSteps) -> None:
        user = self.user
        user.step = step
        user.save()

    def send_message(self, message_code: str = None,
                     message_text: str = None,
                     reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None,
                     chat_id: Union[int, str] = None,
                     message_arguments: list = None,
                     reply_to_message_id: int = None,
                     as_reply: bool = False,
                     disable_web_page_preview: bool = True,
                     parse_mode: str = 'HTML',
                     **kwargs) -> Message:

        if not chat_id:
            chat_id = self.chat_id

        if message_code:
            message_text = self.t(message_code)

        if message_arguments:
            message_text = message_text.format(*message_arguments)

        if as_reply:
            reply_to_message_id = reply_to_message_id if reply_to_message_id else self.message_id

        return self.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            disable_web_page_preview=disable_web_page_preview,
            parse_mode=parse_mode,
            **kwargs
        )

    def edit_message(self, message_code: str = None,
                     message_text: str = None,
                     reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None,
                     chat_id: Union[int, str] = None,
                     message_id: int = None,
                     message_arguments: list = None,
                     disable_web_page_preview: bool = True,
                     parse_mode: str = 'HTML',
                     **kwargs) -> Union[Message, bool]:

        if not message_id:
            message_id = self.message_id

        if not chat_id:
            chat_id = self.chat_id

        if message_code:
            message_text = self.t(message_code)

        if message_arguments:
            message_text = message_text.format(*message_arguments)

        return self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=message_text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            **kwargs
        )

    def delete_message(self,
                       chat_id: Union[int, str] = None,
                       message_id: int = None,
                       **kwargs) -> bool:

        if not message_id:
            message_id = self.message_id

        if not chat_id:
            chat_id = self.chat_id

        return self.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id,
            **kwargs
        )

    def answer_callback(self, message_id: int = None,
                        message_code: str = None,
                        message_text: str = None,
                        show_alert: bool = False,
                        **kwargs) -> bool:
        if not message_id:
            message_id = self.message.id

        if message_code:
            message_text = self.t(message_code)

        return self.bot.answer_callback_query(
            callback_query_id=message_id,
            text=message_text,
            show_alert=show_alert,
            **kwargs
        )

    def set_message_reaction(self,
                             reaction: Optional[List[ReactionType]] = None,
                             is_big: Optional[bool] = None,
                             chat_id: Union[int, str] = None,
                             message_id: int = None) -> bool:

        if not message_id:
            message_id = self.message_id

        if not chat_id:
            chat_id = self.chat_id

        return self.bot.set_message_reaction(chat_id, message_id, reaction, is_big)

    def remove_keyboard(self, message_code: str = None,
                        message_text: str = None) -> Message:
        if message_code:
            message_text = self.t(message_code)

        return self.send_message(message_text=message_text, reply_markup=ReplyKeyboardRemove())

    def bug_fixed(self) -> Union[Message, bool]:
        markup = self.inline_markup()
        markup.add(InlineKeyboardButton(self.messages('true icon'), callback_data='None'))
        return self.bot.edit_message_text(chat_id=EXCEPTION_CHANNEL_ID,
                                          text=self.message.message.text,
                                          reply_markup=markup,
                                          message_id=self.callback_query_id)

    def clear_order(self) -> None:
        self.user.data["order"] = {}
        self.user.save()

    @property
    def order(self) -> dict:
        try:
            return self.user.data["order"]
        except KeyError:
            self.clear_order()
            return {}

    def update_order(self, data: dict) -> None:
        try:
            self.user.data["order"].update(data)
        except KeyError:
            self.user.data["order"] = data
        self.user.save()

    def delete_item_from_order(self, item_key: str) -> None:
        try:
            del self.user.data["order"][item_key]
            self.user.save()
        except KeyError:
            self.clear_order()
