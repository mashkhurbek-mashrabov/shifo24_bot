import requests
from django.core.management import BaseCommand

from bot.constants import BOT_TOKEN, DOMAIN, WEBHOOK_URL_PATH


class Command(BaseCommand):
    help = 'Set Webhook'

    def handle(self, *args, **options):
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={DOMAIN}/{WEBHOOK_URL_PATH}')
        self.stdout.write(self.style.SUCCESS(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={DOMAIN}/{WEBHOOK_URL_PATH}'))
        self.stdout.write(self.style.SUCCESS('Webhook has been set'))