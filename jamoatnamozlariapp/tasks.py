import asyncio
from datetime import datetime

import requests
from celery import shared_task
from celery.utils.log import get_task_logger

from jamoatnamozlariapp.models import ChangeDistrictTimeSchedule, TakbirVaqtlari, Subscription
from namozvaqtlari.settings import env

logger = get_task_logger(__name__)

loop = asyncio.get_event_loop()


@shared_task(name='send_message_task', soft_time_limit=14400)
def send_message_task(user_id, message):
    BOT_TOKEN = env("BOT_TOKEN")
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': user_id, 'text': message, 'parse_mode': 'HTML'}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error: {e}")
    return {"message": "Message has sent successfully"}


@shared_task(name='daily_send_message_task', soft_time_limit=14400, queue='my_sequential_queue')
def daily_send_message_task():
    BOT_TOKEN = env("BOT_TOKEN")
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    today = datetime.today().date()
    takbir = TakbirVaqtlari.objects.select_related('district', 'district__region').\
        filter(date=today).order_by('-date').first()
    if takbir:
        subscriptions = Subscription.objects.select_related('user').values_list('user__user_id',
                                                                                'user__lang').distinct()
        unique_user_lang_list = list(subscriptions)
        for subscription in unique_user_lang_list:
            azon = ChangeDistrictTimeSchedule.objects.select_related('district').filter(
                district=takbir.district, date__date__lte=today).order_by('-date').first()
            if subscription[1] == 'uz':
                sana = "Sana"
                tak = 'Takbir'
                az = 'Azon'
                # masjid = subscription.masjid.name_uz
                add = "dagi takbir vaqtlari o'zgardi"
                district = takbir.district.name_uz
                region = takbir.district.region.name_uz
            else:
                sana = "Сана"
                az = 'Азон'
                tak = 'Такбир'
                # masjid = subscription.masjid.name_cyrl
                add = "даги такбир вақтлари ўзгарди"
                district = takbir.district.name_cyrl
                region = takbir.district.region.name_cyrl
            # text = f"<b>🕌 {masjid}</b>\n\n"
            text = f"📍 <b>{region}, {district}{add}</b>\n\n"
            text += f"<b>📅 {sana}: {today.strftime('%d.%m.%Y')}</b>\n\n"
            if azon:
                text += f"<b>📣 {az}</b>: {azon.bomdod} | {azon.peshin} | {azon.asr} | {azon.shom} | {azon.hufton}\n\n"
            if takbir:
                text += f"<b>🕓 {tak}</b>: {takbir.bomdod} | {takbir.peshin} | {takbir.asr} | {takbir.shom} | {takbir.hufton}\n\n"
            send_message_task.apply_async(args=[subscription[0], text], queue='my_sequential_queue',
                                          time_limit=14400)
            # data = {'chat_id': subscription[0], 'text': text, 'parse_mode': 'HTML'}
            # try:
            #     requests.post(url, data=data)
            # except Exception as e:
            #     print(f"Error: {e}")
            # print(f"{subscription[0]} -> Message has sent successfully")
