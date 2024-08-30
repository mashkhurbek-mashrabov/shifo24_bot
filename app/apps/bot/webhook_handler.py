import logging
import traceback

import telebot

from telebot import types
from telebot.util import content_type_media
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .loader import bot
from .utils import send_exception
from .controllers.main import BotController
from .constants import BotUserSteps, CallbackData

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@csrf_exempt
def process_webhook(request):
    """
        Process webhook calls from Telegram.
    """

    if request.method == 'POST':
        bot.process_new_updates(
            [telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )]
        )
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    controller = BotController(message, bot)
    try:
        controller.greeting()
        controller.list_language()
    except Exception as e:
        controller.main_menu(text=controller.t('exception message'))
        send_exception(traceback.format_exc(), controller.step, controller.user)


@bot.message_handler(content_types=['text'])
def message_handler(message: types.Message):
    controller = BotController(message, bot)
    user_step = controller.step
    message_text = message.text
    try:
        if message_text == controller.t('main menu'):
            controller.main_menu()
        elif message_text == controller.t('back button'):
            controller.back_reply_button_handler()
        elif message_text == controller.t('settings'):
            controller.settings()
        elif user_step == BotUserSteps.SETTINGS and message_text == f"{controller.t('language flag')} {controller.t('change language')}":
            controller.list_language(edit=True)
        elif user_step == BotUserSteps.SETTINGS and message_text == controller.t('change number button'):
            controller.get_phone_number(edit=True)
        elif user_step in [BotUserSteps.EDIT_PHONE_NUMBER, BotUserSteps.GET_PHONE_NUMBER]:
            controller.set_phone_number()
        elif user_step in [BotUserSteps.LISTING_LANGUAGE, BotUserSteps.EDIT_LANGUAGE]:
            controller.set_language()
        else:
            controller.send_exception_message_to_user()
    except Exception as e:
        controller.main_menu(text=controller.t('exception message'))
        send_exception(traceback.format_exc(), controller.step, controller.user)


@bot.callback_query_handler(func=None)
def callback_handler(message: types.CallbackQuery):
    controller = BotController(message, bot)
    user_step = controller.step
    callback_data = message.data
    try:
        if callback_data == CallbackData.MAIN_MENU_BUTTON:
            controller.main_menu(edit=True)
        elif callback_data.startswith(CallbackData.BACK_BUTTON):
            controller.back_inline_button_handler()
        elif callback_data == CallbackData.EXCEPTION:
            controller.bug_fixed()
    except Exception as e:
        controller.main_menu(text=controller.t('exception message'), edit=True)
        send_exception(traceback.format_exc(), controller.step, controller.user)


@bot.message_handler(func=lambda message: True, content_types=["contact"])
def contact_handler(message):
    controller = BotController(message, bot)
    user_step = controller.step
    try:
        if user_step in [BotUserSteps.EDIT_PHONE_NUMBER, BotUserSteps.GET_PHONE_NUMBER]:
            controller.set_phone_number()
    except Exception as e:
        controller.main_menu(text=controller.t('exception message'))
        send_exception(traceback.format_exc(), controller.step, controller.user)


@bot.message_handler(func=lambda message: True, content_types=content_type_media)
def handle_all_message(message):
    controller = BotController(message, bot)
    user_step = controller.step
    try:
        controller.send_exception_message_to_user()
    except Exception as e:
        controller.main_menu(text=controller.t('exception message'))
        send_exception(traceback.format_exc(), controller.step, controller.user)
