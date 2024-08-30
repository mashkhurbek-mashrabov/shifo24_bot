from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models.base import BaseModelV2
from .constants import LanguageChoices, BotUserSteps


class TelegramUser(BaseModelV2):
    """
    Represents a Telegram user interacting with the bot.

    Attributes:
        chat_id (models.CharField): User's unique chat_id in Telegram. (max_length=40)
        username (models.CharField): Username of the user in Telegram. (max_length=40, null=True, blank=True)
        name (models.CharField): Optional full name of the user. (max_length=40, null=True)
        language (models.CharField): User's preferred language based on `bot.constants.LanguageChoices`. (max_length=3, choices=LanguageChoices.choices, default=LanguageChoices.ENGLISH)
        step (models.SmallIntegerField): Current progress of the user within the bot flow based on `bot.constants.BotUserSteps`. (choices=BotUserSteps.choices)

    Methods:
        __str__(self): Returns a string representation of the user for debugging purposes.
    """

    chat_id = models.CharField(_('Chat ID'), max_length=40, unique=True)
    name = models.CharField(_('Name'), max_length=40, null=True)
    username = models.CharField(_('Username'), max_length=40, unique=True, null=True, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=13, null=True, blank=True)
    language = models.CharField(_('Language'),
                                max_length=3,
                                choices=LanguageChoices.choices,
                                default=LanguageChoices.UZBEK)
    step = models.SmallIntegerField(_('Step'), choices=BotUserSteps.choices, default=BotUserSteps.LISTING_LANGUAGE)
    data = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f"{self.chat_id} - {self.name}"

    def clean(self):
        super().clean()
        if self.step not in [step[0] for step in BotUserSteps.choices]:
            raise ValueError("Invalid step value")

        if self.language not in [lang[0] for lang in LanguageChoices.choices]:
            raise ValueError("Invalid language value")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
