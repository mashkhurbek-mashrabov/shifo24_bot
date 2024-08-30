import os
import requests
from pyngrok import ngrok, conf

from django.core.management import BaseCommand
from bot.constants import BOT_TOKEN, WEBHOOK_URL_PATH


class Command(BaseCommand):
    help = 'Run ngrok'

    def handle(self, *args, **options):
        conf_path = os.environ.get("NGROK_CONFIG_PATH")
        tunnel_name = os.environ.get("NGROK_TUNNEL_NAME", "bot")

        try:
            # Set up ngrok with config path and authentication token
            conf.get_default().config_path = conf_path
            ngrok.set_auth_token(os.environ.get("NGROK_AUTH_TOKEN"))

            def log_event_callback(log):
                self.style.SUCCESS(str(log))

            conf.get_default().log_event_callback = log_event_callback

            conf.get_default().monitor_thread = False

            # Connect ngrok and retrieve public URL
            tunnel = ngrok.connect("8000", bind_tls=True, name=tunnel_name)
            public_url = tunnel.public_url
            self.stdout.write(self.style.SUCCESS(f'Public url: {public_url}'))

            # Set DOMAIN environment variable
            os.environ["DOMAIN"] = public_url

            # Set Telegram webhook
            requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={public_url}/{WEBHOOK_URL_PATH}')
            self.stdout.write(self.style.SUCCESS('Webhook has been set'))

            self.stdout.write(self.style.SUCCESS('Click CTRL+C to kill the tunnel'))

            ngrok_process = ngrok.get_ngrok_process()

            # Block until CTRL-C or some other terminating event
            ngrok_process.proc.wait()

        except ngrok.PyngrokError as e:
            self.stdout.write(self.style.ERROR(f'Ngrok error: {e}'))
            self.stdout.write(self.style.WARNING('Troubleshooting tips:'))
            requests.delete(f"http://127.0.0.1:4040/api/tunnels/{tunnel_name}")
            self.handle()
            # Provide troubleshooting guidance based on error messages
        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR("\nShutting down server."))
            ngrok.kill()