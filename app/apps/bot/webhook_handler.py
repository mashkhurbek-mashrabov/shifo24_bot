import logging
import telebot

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .loader import bot

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