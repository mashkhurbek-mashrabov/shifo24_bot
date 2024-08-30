import os

from django.db import models
from django.utils.translation import gettext_lazy as _

BOT_TOKEN = os.environ.get('BOT_TOKEN')
DOMAIN = os.environ.get('DOMAIN')
EXCEPTION_CHANNEL_ID = os.environ.get('EXCEPTION_CHANNEL_ID')
WEBHOOK_URL_PATH = 'bot'


class LanguageChoices(models.TextChoices):
    UZBEK = 'uz', _('Uzbek 🇺🇿')
    ENGLISH = 'en', _('English 🇬🇧')
    RUSSIAN = 'ru', _('Russian 🇷🇺')


class BotUserSteps(models.IntegerChoices):
    LISTING_LANGUAGE = 1, _('Listing language')
    EDIT_LANGUAGE = 2, _('Edit language')
    MAIN_MENU = 3, _('Main menu')


class CallbackData:
    MAIN_MENU_BUTTON = 'MAIN_MENU_BUTTON'
    BACK_BUTTON = 'BACK_BUTTON'
    SKIP = 'SKIP'
    CONTINUE = 'CONTINUE'
    EXCEPTION = 'EXCEPTION'
