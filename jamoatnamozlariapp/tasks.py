import asyncio

import requests
from celery import shared_task
from celery.utils.log import get_task_logger

from namozvaqtlari.settings import env

logger = get_task_logger(__name__)

loop = asyncio.get_event_loop()


@shared_task(name='send_message_task', soft_time_limit=14400)
def send_message_task(user_id, message, parse_mode='HTML'):
    BOT_TOKEN = env("BOT_TOKEN")
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': user_id, 'text': message, 'parse_mode': parse_mode}
    response = requests.post(url, data=data)
    return {"message": "Product has updated successfully", "response": response.json()}
