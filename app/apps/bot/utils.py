import logging
import traceback
import requests

from typing import Union
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from .constants import EXCEPTION_CHANNEL_ID, CallbackData, BotUserSteps, BOT_TOKEN
from .loader import bot
from .strings import messages

logger = logging.getLogger(__name__)


def send_exception(error_text, step, user=None):
    try:
        except_message = ''
        if user:
            if user.username:
                except_message = f"{messages.get('person emoji')} @{user.username}\n"
            else:
                except_message = f"{messages.get('person emoji')} <a href='tg://user?id={user.chat_id}'>{user}</a>\n"

        except_message += f"{messages.get('step emoji')} {BotUserSteps(step).label}\n\n" \
                          f"{messages.get('warning emoji')} {error_text[len(error_text) - 1020:]}"

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton(messages.get('condition emoji'), callback_data=CallbackData.EXCEPTION))
        bot.send_message(chat_id=EXCEPTION_CHANNEL_ID,
                         text=except_message,
                         reply_markup=markup,
                         parse_mode='HTML')
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(e)


def generate_telegram_file_url(file_id: str) -> str:
    """
    Returns a direct link to a Telegram file hosted on the Telegram servers.

    Args:
        file_id (str): The unique identifier of the file.

    Returns:
        str: The direct link to the Telegram file.
    """
    file_info = bot.get_file(file_id)
    return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"


def price_formatter(price: Union[int, float]) -> str:
    """
    Formats a price value into a human-readable string with proper commas and decimal point handling.

    Args:
        price (Union[int, float]): The price value to be formatted.

    Returns:
        str: The formatted price string.
    """

    try:
        formatted_price = f"{price:,.2f}"
    except TypeError:
        return str(price)

    # Trim trailing '.00' and replace commas with spaces
    formatted_price = formatted_price.rstrip(".0").replace(",", " ")

    return formatted_price


def get_client_ip(request):
    """
    Retrieves the client's IP address from the request object, accounting for potential proxies.

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        str: The client's IP address as a string.
    """
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    remote_addr = request.META.get('REMOTE_ADDR', None)
    if forwarded_for:
        # Split and take the first address if forwarded
        return forwarded_for.split(",")[0].strip()
    else:
        return remote_addr


def get_ip_location(ip_address):
    """
    Retrieves location information for an IP address using an external API.

    Args:
        ip_address (str): The client's IP address.

    Returns:
        dict or None: Dictionary containing location data if successful, None otherwise.

    Example:
        location = get_ip_location(get_client_ip(request))
        if location:
            print(f"Country: {location['country']}")
            print(f"City: {location['city']}")
    """

    response = requests.get(f"http://ip-api.com/json/{ip_address}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
